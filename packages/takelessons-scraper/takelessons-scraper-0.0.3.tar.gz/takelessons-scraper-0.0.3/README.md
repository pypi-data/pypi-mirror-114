# Scrape the chat logs from TakeLessons

## What is this?
If you noticed that TakeLessons doesn't have an API or a way to export your own data you can use this package to get at it.

## How do I use it?

### Prerequisites

1. Install Chrome
2. Find the correct selenium driver version for your install [here](https://chromedriver.chromium.org/downloads)
3. Add it to PATH or make a note of where it is
4. ```pip install takelessons-scraper```

### Example Usage:

```py 
# Assume some db object you can save your data to
db = SomeDBStore()
from takelessons_scraper import TakeLessonsScraper
chromedriver_path = '/path/to/chromedriver'
username = 'username'
password = 'password'
scraper = TakeLessonsScraper(chromedriver_path)
# login to load cookies behind scenes
scraper.login(username, password)
# get a block of chat data up to date
chat_date = '2020-01-01'
# you may need to sleep a bit
chat_log = scraper.get_chat_history(chat_date) # Chat obj, can get raw json back
db.save(chat_log)
```

## Notes:
Please consider this a hobby project to be used as reference. Since it is a scraper I expect it to fail as regularly as the source is updated... which could be at any time and not within my control.
