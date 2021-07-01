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
    [ ] n (and/or) x
    [X] Consent of instructor
    [X] n
    [ ] n. Not open for students with credit for n or n
    [X] class standing
    [X] Graduate/professional standing
    [ ] Graduate standing or special student
    
    CHECK FOR \w BEFORE \d, IF FALSE, COURSES ARE OF THE SAME SUBJECT
    
    
    
    regex subject string = (AFAERO|AFRICAN|AFROAMER|AAE|BSE|LSC|AGROECOL|AGRONOMY|AMERIND|ANATOMY|ANAT\&PHY|ANESTHES|ANTHRO|ABT|ART|ARTED|ARTHIST|ASIANAM|ASIAN|ASIALANG|ASTRON|MICROBIO|RP\&SE|BIOCHEM|BIOLOGY|BIOCORE|BME|BOTANY|BMI|CRB|CBE|CHEM|CHICLA|DERM|HDFS|GENBUS|ACCTIS|FINANCE|INFOSYS|INTLBUS|MHR|MARKETNG|OTM|REALEST|CIVENGR|RMI|ACTSCI|CLASSICS|CSCS|COMARTS|CS\&D|COMPLIT|COMPSCI|COUNPSY|CNSRSCI|CURRIC|DYSCI|EASIAN|ECON|EASTDS|ELPA|EDPOL|EDPSYCH|ECE|EMERMED|EMA|EP|EPD|ESL|ENGL|ENTOM|DS|ENVIRST|M\&ENVTOX|FAMMED|FISC|FOLKLORE|FOODSCI|F\&WECOL|FRENCH|GENETICS|GEOG|GLE|GEOSCI|GERMAN|GNS|GREEK|OBS\&GYN|HEBR\-BIB|HEBR\-MOD|HISTORY|MEDHIST|HISTSCI|HORT|HONCOL|ISYE|INTER\-AG|INTEGART|INTEREGR|INTER\-HE|ILS|INTER\-LS|INTEGSCI|INTLST|ITALIAN|JEWISH|JOURN|LANDARC|LCA|LCALANG|LATIN|LACIS|LAW|LEGALST|LIS|LINGUIS|LITTRANS|MATH|ANSCI|ME|MDGENET|MM\&I|MEDPHYS|MEDSC\-M|MEDSC\-V|MEDICINE|MEDIEVAL|MS\&E|ATMOCN|MILSCI|MOLBIOL|MUSIC|MUSPERF|NAVSCI|NEUROL|NEURSURG|NEURODPT|NTP|NE|CNP|NURSING|NUTRSCI|OCCTHER|ONCOLOGY|OPHTHALM|PATH\-BIO|PATH|PEDIAT|PHMSCI|PHMCOL\-M|PHARMACY|PHMPRAC|S\&APHM|PHILOS|DANCE|KINES|PHYTHER|PHYASST|PHYSICS|BMOLCHEM|PHYSIOL|PLPATH|POLISCI|PORTUG|POPHLTH|PSYCHIAT|PSYCH|PUBAFFR|PUBLHLTH|RADIOL|RHABMED|RELIGST|C\&ESOC|SCANDST|STS|SRMED|SLAVIC|SOCWORK|SOC|SOILSCI|SPANISH|STAT|COMPBIO|SURGERY|SURGSCI|THEATRE|URBRPL|GEN\&WS|ZOOLOGY)
    
    commonReqs = ['Freshman standing', 'Sophomore standing', 'Junior standing', 'Senior standing', 'Consent of instructor', 'Graduate/professional standing']
"""

commonReqs = ['Freshman standing', 'Sophomore standing', 'Junior standing', 'Senior standing',
              'Graduate/professional standing', 'Consent of instructor']


# TODO: this is missing spaces in a bunch of subjects, make this from subjects.json again
subjectRegex = r'(AFAERO|AFRICAN|AFROAMER|AAE|BSE|LSC|AGROECOL|AGRONOMY|AMERIND|ANATOMY|ANAT\&PHY|ANESTHES|ANTHRO|ABT' \
               r'|ART|ARTED|ARTHIST|ASIANAM|ASIAN|ASIALANG|ASTRON|MICROBIO|RP\&SE|BIOCHEM|BIOLOGY|BIOCORE|BME|BOTANY' \
               r'|BMI|CRB|CBE|CHEM|CHICLA|DERM|HDFS|GENBUS|ACCTIS|FINANCE|INFOSYS|INTLBUS|MHR|MARKETNG|OTM|REALEST' \
               r'|CIVENGR|RMI|ACTSCI|CLASSICS|CSCS|COMARTS|CS\&D|COMPLIT|COMPSCI|COUNPSY|CNSRSCI|CURRIC|DYSCI|EASIAN' \
               r'|ECON|EASTDS|ELPA|EDPOL|EDPSYCH|ECE|EMERMED|EMA|EP|EPD|ESL|ENGL|ENTOM|DS|ENVIRST|M\&ENVTOX|FAMMED' \
               r'|FISC|FOLKLORE|FOODSCI|F\&WECOL|FRENCH|GENETICS|GEOG|GLE|GEOSCI|GERMAN|GNS|GREEK|OBS\&GYN|HEBR\-BIB' \
               r'|HEBR\-MOD|HISTORY|MEDHIST|HISTSCI|HORT|HONCOL|ISYE|INTER\-AG|INTEGART|INTEREGR|INTER\-HE|ILS|INTER' \
               r'\-LS|INTEGSCI|INTLST|ITALIAN|JEWISH|JOURN|LANDARC|LCA|LCALANG|LATIN|LACIS|LAW|LEGALST|LIS|LINGUIS' \
               r'|LITTRANS|MATH|ANSCI|ME|MDGENET|MM\&I|MEDPHYS|MEDSC\-M|MEDSC\-V|MEDICINE|MEDIEVAL|MS\&E|ATMOCN' \
               r'|MILSCI|MOLBIOL|MUSIC|MUSPERF|NAVSCI|NEUROL|NEURSURG|NEURODPT|NTP|NE|CNP|NURSING|NUTRSCI|OCCTHER' \
               r'|ONCOLOGY|OPHTHALM|PATH\-BIO|PATH|PEDIAT|PHMSCI|PHMCOL\-M|PHARMACY|PHMPRAC|S\&APHM|PHILOS|DANCE' \
               r'|KINES|PHYTHER|PHYASST|PHYSICS|BMOLCHEM|PHYSIOL|PLPATH|POLISCI|PORTUG|POPHLTH|PSYCHIAT|PSYCH|PUBAFFR' \
               r'|PUBLHLTH|RADIOL|RHABMED|RELIGST|C\&ESOC|SCANDST|STS|SRMED|SLAVIC|SOCWORK|SOC|SOILSCI|SPANISH|STAT' \
               r'|COMPBIO|SURGERY|SURGSCI|THEATRE|URBRPL|GEN\&WS|ZOOLOGY)\s(\d+)'

courseRegex = subjectRegex + r'\s\d+'

courseCombinations = []


def mapRequisites(courses):
    # filter courses without requisites
    courses = list(filter(lambda c: c['requisite'] is not None, courses))

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
        combinationId = 0
        if re.fullmatch(f'^({courseRegex})$', requisite):
            courseCombinations.append({combinationId: (course.abbrev, requisite)})  # this is likely a better way to do this
            # courseCombinations.append((combinationId, course.abbrev, [requisite]))
            combinationId += 1
        # check for two course
        # elif re.fullmatch(fr'^((?P<course1>{courseRegex})\w(?P<combinator>and|or)\w(?P<course2>{courseRegex}))$'):
        #     courseCombinations.append((combinationId, course.abbrev, [requisite,]))

    return courseCombinations


def __parseRequisite():
    pass
