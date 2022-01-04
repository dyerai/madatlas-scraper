"""DB CREATION CLI

Usage:
    app.py
"""
from src.utils.base import Session, engine, Base
from src.Scrapers import scrapeSubjects, scrapeCourses


def run():
    # start db
    print("Initializing database...")
    Base.metadata.create_all(engine)
    session = Session()
    print("Database initialized.")

    # scrape wisc subjects
    print("Now scraping subjects")
    scrapeSubjects(session)
    print("Subjects scraped.")

    # scrape wisc courses
    print("Now scraping courses")
    scrapeCourses(session)
    print("Courses scraped.")

