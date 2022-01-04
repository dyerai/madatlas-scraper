import re

"""
Cases in requisite string:
    [ ] () and () or x
    [ ] () or x
    [ ] () and () or x
    [ ] n,n,n,n or n or x
    [ ] x and () or
    [ ] n or n, x
    [X] None
    [X] n (and/or) x
    [X] Consent of instructor
    [X] n
    [ ] n. Not open for students with credit for n or n
    [X] class standing
    [X] Graduate/professional standing
    [ ] Graduate standing or special student
    
    CHECK FOR \w BEFORE \d, IF FALSE, COURSES ARE OF THE SAME SUBJECT
    
    
    
    regex subject string = ('A F AERO', 'AFRICAN', 'AFROAMER', 'A A E', 'BSE', 'LSC', 'AGROECOL', 'AGRONOMY', 'AMER IND', 'ANATOMY', 'ANAT\&PHY', 'ANESTHES', 'ANTHRO', 'ABT', 'ART', 'ART ED', 'ART HIST', 'ASIAN AM', 'ASIAN', 'ASIALANG', 'ASTRON', 'MICROBIO', 'RP \& SE', 'BIOCHEM', 'BIOLOGY', 'BIOCORE', 'B M E', 'BOTANY', 'B M I', 'CRB', 'CBE', 'CHEM', 'CHICLA', 'DERM', 'HDFS', 'GEN BUS', 'ACCT I S', 'FINANCE', 'INFO SYS', 'INTL BUS', 'M H R', 'MARKETNG', 'OTM', 'REAL EST', 'CIV ENGR', 'R M I', 'ACT SCI', 'CLASSICS', 'CSCS', 'COM ARTS', 'CS\&D', 'COMP LIT', 'COMP SCI', 'COUN PSY', 'CNSR SCI', 'CURRIC', 'DY SCI', 'E ASIAN', 'ECON', 'E A STDS', 'ELPA', 'ED POL', 'ED PSYCH', 'E C E', 'EMER MED', 'E M A', 'E P', 'E P D', 'ESL', 'ENGL', 'ENTOM', 'DS', 'ENVIR ST', 'M\&ENVTOX', 'FAM MED', 'FISC', 'FOLKLORE', 'FOOD SCI', 'F\&W ECOL', 'FRENCH', 'GENETICS', 'GEOG', 'G L E', 'GEOSCI', 'GERMAN', 'GNS', 'GREEK', 'OBS\&GYN', 'HEBR-BIB', 'HEBR-MOD', 'HISTORY', 'MED HIST', 'HIST SCI', 'HORT', 'H ONCOL', 'I SY E', 'INTER-AG', 'INTEGART', 'INTEREGR', 'INTER-HE', 'ILS', 'INTER-LS', 'INTEGSCI', 'INTL ST', 'ITALIAN', 'JEWISH', 'JOURN', 'LAND ARC', 'LCA', 'LCA LANG', 'LATIN', 'LACIS', 'LAW', 'LEGAL ST', 'L I S', 'LINGUIS', 'LITTRANS', 'MATH', 'AN SCI', 'M E', 'MD GENET', 'M M \& I', 'MED PHYS', 'MED SC-M', 'MED SC-V', 'MEDICINE', 'MEDIEVAL', 'M S \& E', 'ATM OCN', 'MIL SCI', 'MOL BIOL', 'MUSIC', 'MUS PERF', 'NAV SCI', 'NEUROL', 'NEURSURG', 'NEURODPT', 'NTP', 'N E', 'CNP', 'NURSING', 'NUTR SCI', 'OCC THER', 'ONCOLOGY', 'OPHTHALM', 'PATH-BIO', 'PATH', 'PEDIAT', 'PHM SCI', 'PHMCOL-M', 'PHARMACY', 'PHM PRAC', 'S\&A PHM', 'PHILOS', 'DANCE', 'KINES', 'PHY THER', 'PHY ASST', 'PHYSICS', 'BMOLCHEM', 'PHYSIOL', 'PL PATH', 'POLI SCI', 'PORTUG', 'POP HLTH', 'PSYCHIAT', 'PSYCH', 'PUB AFFR', 'PUBLHLTH', 'RADIOL', 'RHAB MED', 'RELIG ST', 'C\&E SOC', 'SCAND ST', 'STS', 'SR MED', 'SLAVIC', 'SOC WORK', 'SOC', 'SOIL SCI', 'SPANISH', 'STAT', 'COMP BIO', 'SURGERY', 'SURG SCI', 'THEATRE', 'URB R PL', 'GEN\&WS', 'ZOOLOGY')
    
    commonReqs = ['Freshman standing', 'Sophomore standing', 'Junior standing', 'Senior standing', 'Consent of instructor', 'Graduate/professional standing']
"""

commonReqs = ['Freshman standing', 'Sophomore standing', 'Junior standing', 'Senior standing',
              'Graduate/professional standing', 'Consent of instructor']

subjectRegex = r'(A F AERO|AFRICAN|AFROAMER|A A E|BSE|LSC|AGROECOL|AGRONOMY|AMER ' \
               r'IND|ANATOMY|ANAT\&PHY|ANESTHES|ANTHRO|ABT|ART|ART ED|ART HIST|ASIAN ' \
               r'AM|ASIAN|ASIALANG|ASTRON|MICROBIO|RP \& SE|BIOCHEM|BIOLOGY|BIOCORE|B M E|BOTANY|B M ' \
               r'I|CRB|CBE|CHEM|CHICLA|DERM|HDFS|GEN BUS|ACCT I S|FINANCE|INFO SYS|INTL BUS|M H R|MARKETNG|OTM|REAL ' \
               r'EST|CIV ENGR|R M I|ACT SCI|CLASSICS|CSCS|COM ARTS|CS\&D|COMP LIT|COMP SCI|COUN PSY|CNSR ' \
               r'SCI|CURRIC|DY SCI|E ASIAN|ECON|E A STDS|ELPA|ED POL|ED PSYCH|E C E|EMER MED|E M A|E P|E P ' \
               r'D|ESL|ENGL|ENTOM|DS|ENVIR ST|M\&ENVTOX|FAM MED|FISC|FOLKLORE|FOOD SCI|F\&W ' \
               r'ECOL|FRENCH|GENETICS|GEOG|G L E|GEOSCI|GERMAN|GNS|GREEK|OBS\&GYN|HEBR-BIB|HEBR-MOD|HISTORY|MED ' \
               r'HIST|HIST SCI|HORT|H ONCOL|I SY E|INTER-AG|INTEGART|INTEREGR|INTER-HE|ILS|INTER-LS|INTEGSCI|INTL ' \
               r'ST|ITALIAN|JEWISH|JOURN|LAND ARC|LCA|LCA LANG|LATIN|LACIS|LAW|LEGAL ST|L I ' \
               r'S|LINGUIS|LITTRANS|MATH|AN SCI|M E|MD GENET|M M \& I|MED PHYS|MED SC-M|MED SC-V|MEDICINE|MEDIEVAL|M ' \
               r'S \& E|ATM OCN|MIL SCI|MOL BIOL|MUSIC|MUS PERF|NAV SCI|NEUROL|NEURSURG|NEURODPT|NTP|N ' \
               r'E|CNP|NURSING|NUTR SCI|OCC THER|ONCOLOGY|OPHTHALM|PATH-BIO|PATH|PEDIAT|PHM SCI|PHMCOL-M|PHARMACY|PHM ' \
               r'PRAC|S\&A PHM|PHILOS|DANCE|KINES|PHY THER|PHY ASST|PHYSICS|BMOLCHEM|PHYSIOL|PL PATH|POLI ' \
               r'SCI|PORTUG|POP HLTH|PSYCHIAT|PSYCH|PUB AFFR|PUBLHLTH|RADIOL|RHAB MED|RELIG ST|C\&E SOC|SCAND ' \
               r'ST|STS|SR MED|SLAVIC|SOC WORK|SOC|SOIL SCI|SPANISH|STAT|COMP BIO|SURGERY|SURG SCI|THEATRE|URB R ' \
               r'PL|GEN\&WS|ZOOLOGY)'

courseRegex = subjectRegex + r'\s\d+'

courseCombinations = []
logical_combinations = []

def mapRequisites(courses):
    # filter courses without requisites
    courses = list(filter(lambda c: c['requisite'] is not None, courses))

    combinationID = 0
    for course in courses:
        requisite = course['requisite']

        # first, check for common SOLE prerequisites (class standing, instr. consent)
        if requisite == commonReqs[0]:
            course.requiresFreshmanStanding = True
        elif requisite == commonReqs[1]:
            course.requiresSophomoreStanding = True
        elif requisite == commonReqs[2]:
            course.requiresJuniorStanding = True
        elif requisite == commonReqs[3]:
            course.requiresSeniorStanding = True
        elif requisite == commonReqs[4]:
            course.requiresGraduateOrProfessionalStanding = True
        elif requisite == commonReqs[5]:
            course.requiresInstructorConsent = True

        # check if requisite is a single course
        # {combinationId: (requisite, sub_combination)}
        case = __checkCase(requisite)
        if case['singleCourse']:
            courseCombinations.append({combinationID: (requisite, None)})  # this is likely a better way to do this
            course.prerequisiteId = combinationID
            combinationID += 1
        # check for two courses with same subject
        elif case['doubleCourse']:
            pass
        # check for two courses with different subjects
        elif case['doubleCourse_diff_subj']:
            course1 = case['doubleCourse_diff_subj'].group('course1')
            combinator = case['doubleCourse_diff_subj'].group('combinator')
            course2 = case['doubleCourse_diff_subj'].group('course2')
            courseCombinations.append({combinationID: (course1, None)})
            courseCombinations.append({combinationID: (course2, None)})
            logical_combinations.append((combinationID, combinator.upper()))
            combinationID += 1

    return courseCombinations


def __checkCase(s):
    singleCourse = re.fullmatch(f'^({courseRegex})$', s)
    doubleCourse = re.fullmatch(fr'(^{subjectRegex}\s(?P<course1>\d+)\s(?P<combinator>and|or)\w(?P<course2>\d+)$|'
                                + fr'^{subjectRegex}\s(?P<course1num>\d+),\s(?P<course2num>\d+)$)')
    doubleCourse_diff_subj = re.fullmatch(fr'^(?P<course1>{courseRegex})\w(?P<combinator>and|or)\w(?P<course2>{courseRegex})$', s)

    return {
        'singleCourse': singleCourse,
        'doubleCourse': doubleCourse,
        'doubleCourse_diff_subj': doubleCourse_diff_subj,
    }
