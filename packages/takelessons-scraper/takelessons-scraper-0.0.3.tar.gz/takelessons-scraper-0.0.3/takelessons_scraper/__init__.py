import os

from .takelessons_scraper import TakeLessonsScraper


def get_version():
    filepath = os.path.join(os.path.dirname(__file__), "__version__")
    with open(filepath) as buffer:
        return buffer.readline()


__version__ = get_version()
