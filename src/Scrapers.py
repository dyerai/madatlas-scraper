from bs4 import BeautifulSoup as Soup, Tag
from html import unescape
from tqdm import tqdm
import re
import requests
import csv
import unicodedata

from src.Models import Subject, Course, Credits

titlePattern = re.compile('(\D+)\s(\d+)')  # group 1 = abbrev | group 2 = course number
creditPattern = re.compile('\d+')


def scrapeSubjects(session):
    response = requests.get("https://registrar.wisc.edu/subjectarea/")
    soup = Soup(response.content, "html.parser")

    subjectTable = soup.find("tbody")

    for item in tqdm(subjectTable.find_all("tr")):
        if isinstance(item, Tag):
            data = item.find_all("td")
            code = data[0].text
            abbrev = data[1].text
            name = data[2].text
            s = Subject(name, abbrev, code)

            exists = session.query(Subject).filter(Subject.name == name).first()
            if not exists:
                session.add(s)
    return


def scrapeCourses(session):
    # get subject paths
    subjectpaths = []
    with open('data/subjectpaths.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            subjectpaths = row

    # crawl subject pages and parse courses
    for path in tqdm(subjectpaths):
        response = requests.get("https://guide.wisc.edu" + path)
        formattedText = unicodedata.normalize("NFKD", response.text)
        soup = Soup(formattedText, "html.parser")

        for c in soup.find_all("div", {"class": "courseblock"}):
            if isinstance(c, Tag):
                shortTitle = unescape(c.find("span", {"class": "courseblockcode"})
                                      .getText(strip=True)).replace(u'\u200B', '')
                longTitle = c.find("p", {"class": "courseblocktitle"}).getText().split("— ")[1].replace(u'\u200B', '')
                credits = __parseCredits(c.find("p", {"class": "courseblockcredits"}).getText())
                subjects, courseNumber = __parseTitle(unescape(shortTitle))  # [0] = abbrev | [1] = course number
                description = c.find("p", {"class": "courseblockdesc"}).getText()

                # get requisites, course designation, repeatable, and last taught
                requisites = None
                designation = ""
                repeatable = None
                lasttaught = None
                for extras in c.find_all("p", {"class": "courseblockextra"}):
                    line = extras.getText().split(': ')
                    if line[0] == "Requisites":
                        requisites = line[1]
                    elif line[0] == "Course Designation":
                        designation = line[1]
                    elif line[0] == "Repeatable for Credit":
                        repeatable = line[1]
                        if repeatable == "No":
                            repeatable = False
                        else:
                            repeatable = True
                    elif line[0] == "Last Taught":
                        lasttaught = line[1]

                d = __parseDesignation(designation)

                exists = session.query(Course).filter(Course.name == longTitle).first()
                if not exists:
                    course = Course(shortTitle, longTitle, courseNumber, description, requisites, d['L&S'], d['breadth'],
                                    d['level'], d['gen_ed'], d['ethnic_studies'], d['grad'], repeatable, lasttaught)

                    # fetch course subjects
                    cSubj = []
                    for s in subjects:
                        cSubj.append(session.query(Subject).filter_by(abbrev=s).first())
                    for numCredits in credits:
                        session.add(Credits(course, numCredits))
                    course.subjects = cSubj


def __parseTitle(t):
    m = titlePattern.match(t)
    abbrev = m.group(1)
    code = m.group(2)
    if '/' in abbrev:
        abbrev = abbrev.split('/')
        abbrev = frozenset([s.replace(u'\u200b', '').replace('\xa0', ' ').strip() for s in abbrev])
        return abbrev, code

    return frozenset({unicodedata.normalize("NFKD", abbrev).strip()}), code


def __parseCredits(c):
    res = []
    if '-' in c:
        for num in c.split('-'):
            res.append(int(creditPattern.match(num).group()))
    else:
        res.append(int(creditPattern.match(c).group()))
    return res


def __parseDesignation(d):
    """
       L&S Credit - Counts as Liberal Arts and Science credit in L&S
       Breadth - (Biological Science|Humanities|Literature|Natural Science|Physical Science|Social Science)
       Level - (Elementary|Intermediate|Advanced)
       Gen Ed - (Communication Part A|Communication Part B|Quantitative Reasoning Part A|Quantitative Reasoning Part B)
       Ethnic St - Counts toward Ethnic Studies requirement
       Grad 50% - Counts toward 50% graduate coursework requirement
    """
    LS_regex = r'L\&S Credit - Counts as Liberal Arts and Science credit in L\&S'
    breadth_regex = r'Breadth - (Biological Science|Humanities|Literature|Natural Science|Physical Science|Social Science)'
    level_regex = r'Level - (Elementary|Intermediate|Advanced)'
    GE_regex = r'Gen Ed - (Communication Part A|Communication Part B|Quantitative Reasoning Part A|Quantitative Reasoning Part B)'
    ES_regex = r'Ethnic St - Counts toward Ethnic Studies requirement'
    grad_regex = r'Grad 50% - Counts toward 50% graduate coursework requirement'

    breadth = None
    gen_ed = None
    level = None

    # check if course counts for L&S credit:
    LS_credit = bool(re.search(LS_regex, d))

    # check if course counts for breadth:
    if re.search(breadth_regex, d):
        breadth = re.search(breadth_regex, d).group(1)

    # get course level
    if re.search(level_regex, d):
        level = re.search(level_regex, d).group(1)

    # check if course counts for any gen ed requirements:
    if re.search(GE_regex, d):
        gen_ed = re.search(GE_regex, d).group(1)

    # check if course counts toward ethnic studies requirement
    counts_for_ethnic = bool(re.search(ES_regex, d))

    # check if course counts for 50% grad coursework requirement
    grad = bool(re.search(grad_regex, d))

    return {
        'L&S': LS_credit,
        'breadth': breadth,
        'level': level,
        'gen_ed': gen_ed,
        'ethnic_studies': counts_for_ethnic,
        'grad': grad
    }
