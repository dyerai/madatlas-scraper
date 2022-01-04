from utils.base import Base, Session, engine
from src.Scrapers import scrapeSubjects, scrapeCourses
from src.Models import Credits, Subject, Course


session = Session()

print('Scraping subjects...')
scrapeSubjects(session)
session.commit()
print('Finished scraping subjects..\nNow scraping courses')
scrapeCourses(session)

session.commit()
session.close()
print('Finished.')
