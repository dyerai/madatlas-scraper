import json
from bs4 import BeautifulSoup as Soup, Tag
from html import unescape
from src.models.Subject import Subject
from src.models.Course import Course
import re
import requests
import csv
import unicodedata

titlePattern = re.compile('(\D+)\s(\d+)')  # group 1 = abbrev | group 2 = course number
creditPattern = re.compile('\d+')


def scrapeSubjects():
    response = requests.get("https://registrar.wisc.edu/subjectarea/")
    soup = Soup(response.content, "html.parser")

    subjectTable = soup.find("tbody")
    subjects = {}

    for item in subjectTable.find_all("tr"):
        if isinstance(item, Tag):
            data = item.find_all("td")
            code = data[0].text
            abbrev = data[1].text
            name = data[2].text
            s = Subject(name, abbrev, code)
            subjects[abbrev] = s

    return subjects


def scrapeCourses():
    allSubjects = scrapeSubjects()
    courses = {}

    # get subject paths
    subjectpaths = []
    with open('\\\wsl$\\Ubuntu\\home\\dyerai\\madatlas-scraper\\src\\data\\subjectpaths.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            subjectpaths = row

    # crawl subject pages and parse courses
    for path in subjectpaths:
        response = requests.get("https://guide.wisc.edu" + path)
        soup = Soup(response.content, "html.parser")

        for course in soup.find_all("div", {"class": "courseblock"}):
            if isinstance(course, Tag):
                shortTitle = unescape(course.find("span", {"class": "courseblockcode"}).getText(strip=True))
                longTitle = course.find("p", {"class": "courseblocktitle"}).getText().split("— ")[1]
                credits = __parseCredits(course.find("p", {"class": "courseblockcredits"}).getText())
                subjects, courseNumber = __parseTitle(unescape(shortTitle))  # [0] = abbrev | [1] = course number
                description = course.find("p", {"class": "courseblockdesc"}).getText()

                # get requisites, course designation, repeatable, and last taught
                requisites = None
                designation = None
                repeatable = None
                lasttaught = None
                for extras in course.find_all("p", {"class": "courseblockextra"}):
                    line = extras.getText().split(': ')
                    # TODO: streamline requisites
                    if line[0] == "Requisites":
                        requisites = line[1]
                    elif line[0] == "Course Designation":
                        designation = line[1]
                    elif line[0] == "Repeatable for Credit":
                        repeatable = line[1]
                    elif line[0] == "Last Taught":
                        lasttaught = line[1]

                # map allSubjects to Subject objects
                cSubj = []
                for s in subjects:
                    cSubj.append(allSubjects[s].__dict__)

                # TODO: construct Course objects
                c = Course(shortTitle, cSubj, longTitle, courseNumber, credits, description, requisites, designation,
                           repeatable, lasttaught)
                key = frozenset({subjects, courseNumber})
                if not courses.get(key):
                    courses[key] = c


def __parseTitle(t):
    m = titlePattern.match(t)
    abbrev = m.group(1)
    code = m.group(2)
    if '/' in abbrev:
        abbrev = abbrev.split('/')
        abbrev = frozenset([s.replace('\u200b', '').replace('\xa0', ' ').strip() for s in abbrev])
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



scrapeCourses()
