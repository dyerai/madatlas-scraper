from sqlalchemy import Table, Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship

from src.utils.base import Base, engine


course_subjects = Table(
    'course_subjects', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

# this may need to be its own class
course_credits = Table(
    'course_credits', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('credits', Integer)
)


class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    abbrev = Column(String)
    subjects = relationship("Subject", secondary=course_subjects)
    name = Column(String)
    number = Column(Integer)
    description = Column(String)
    requisites = Column(String)
    counts_as_LS_credit = Column(Boolean)
    breadth = Column(String)
    level = Column(String)
    gen_ed = Column(String)
    counts_as_ethnic_studies = Column(Boolean)
    counts_toward_50percent_grad = Column(Boolean)
    '''
    L&S Credit - Counts as Liberal Arts and Science credit in L&S
    Breadth - (Biological Science|Humanities|Literature|Natural Science|Physical Science|Social Science)
    Level - (Elementary|Intermediate|Advanced)
    Gen Ed - (Communication Part A|Communication Part B|Quantitative Reasoning Part A|Quantitative Reasoning Part B)
    Ethnic St - Counts toward Ethnic Studies requirement
    '''
    repeatable = Column(Boolean)
    lastTaught = Column(String)

    def __init__(self, abbrev, name, number, description, requisites, counts_as_LS_credit, breadth, level, gen_ed, counts_as_ethnic_studies, counts_toward_50percent_grad, repeatable, lastTaught):
        self.abbrev = abbrev
        self.name = name
        self.number = number
        self.description = description
        self.requisites = requisites
        self.counts_as_LS_credit = counts_as_LS_credit
        self.breadth = breadth
        self.level = level
        self.gen_ed = gen_ed
        self.counts_as_ethnic_studies = counts_as_ethnic_studies
        self.counts_toward_50percent_grad = counts_toward_50percent_grad
        self.repeatable = repeatable
        self.lastTaught = lastTaught
    """
    requiresFreshmanStanding: bool = False
    requiresSophomoreStanding: bool = False
    requiresJuniorStanding: bool = False
    requiresSeniorStanding: bool = False
    requiresGraduateOrProfessionalStanding: bool = False
    requiresInstructorConsent: bool = False
    prerequisiteId: int = None
    id: int = None
    """


class Subject(Base):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbrev = Column(String)
    code = Column(Integer)

    def __init__(self, name, abbrev, code):
        self.name = name
        self.abbrev = abbrev
        self.code = code


class Credits(Base):
    __tablename__ = 'course_credits'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    credits = Column(Integer)
    course = relationship("Course", backref='course_credits')

    def __init__(self, course, credits):
        self.course = course
        self.credits = credits


Base.metadata.create_all(engine)


