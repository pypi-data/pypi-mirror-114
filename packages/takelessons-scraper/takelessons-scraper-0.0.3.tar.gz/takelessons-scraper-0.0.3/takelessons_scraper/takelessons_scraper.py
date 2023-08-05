import time
import json
from collections import defaultdict
from json.decoder import JSONDecodeError

import requests
import pendulum

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from takelessons_scraper import selenium_tools


class TakeLessonsScraper:
    def __init__(self, selenium_driver_path=None):
        self.selenium_driver_path = selenium_driver_path
        self.driver = None

    def login(self, username, password, headless=True, window_size="1920,1080"):
        login_url = "https://takelessons.com/login"
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument(f"--window-size={window_size}")
        driver = webdriver.Chrome(
            executable_path=self.selenium_driver_path, chrome_options=chrome_options
        )
        driver.get(login_url)
        driver.find_element_by_id("Email").send_keys(username)
        driver.find_element_by_id("Password").send_keys(password)
        driver.find_element_by_css_selector("button.PillButton.Blue").click()
        self.driver = driver

    def get_chat_history(self, date, user_agent=None, cookies=None):
        chat_ajax_url = (
            f"https://takelessons.com/client/journal/ajaxEvents?end_date={date}"
        )
        if not bool(cookies):
            cookies = self.driver.get_cookies()
            cookies = selenium_tools.convert_cookies_to_str(cookies)

        if not bool(user_agent):
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

        headers = {
            "Cookie": cookies,
            "Referer": "https://takelessons.com/client/journal",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": user_agent,
        }
        response = requests.get(chat_ajax_url, headers=headers)
        if response.status_code == 200:
            try:
                chat = Chat(json.loads(response.content))
                return chat
            except JSONDecodeError:
                logging.error('json decode error, have you tried sleeping between calls?')
                logging.info(chat_ajax_url)
                logging.info(response.content)
                raise

    def logout(self):
        self.driver.quit()


class Chat:
    def __init__(self, chat_json):
        self.raw_chat = chat_json
        self.processed_chat_log = Chat.process_chat_log(chat_json)
        self.teachers = list(self.processed_chat_log["teacher_chat"].keys())
        self.students = list(self.processed_chat_log["student_chat"].keys())
        self.next_pull_day = self.processed_chat_log["next_pull_day"]
        self.teacher_chat = self.processed_chat_log["teacher_chat"]
        self.student_chat = self.processed_chat_log["student_chat"]
        self.earliest_date = self.processed_chat_log["earliest_date"]
        self.latest_date = self.processed_chat_log["latest_date"]

    def __str__(self):
        teacher_data = {
            teacher: (
                "num_chat_entries",
                len(self.processed_chat_log["teacher_chat"][teacher]),
            )
            for teacher in self.processed_chat_log["teacher_chat"]
        }

        student_data = {
            student: (
                "num_chat_entries",
                len(self.processed_chat_log["student_chat"][student]),
            )
            for student in self.processed_chat_log["student_chat"]
        }

        return f"<teachers: {teacher_data}, students: {student_data}, earliest_date: {self.earliest_date}, latest_date: {self.latest_date}>"

    @staticmethod
    def process_chat_log(chat_json):
        log = chat_json["params"]  # Why is this called params??
        events, next_event = log["events"], log["nextEndDate"]
        moderator_chat = defaultdict(list)  # teacher : chat
        participant_chat = defaultdict(list)  # student : chat
        min_date, max_date = None, None
        for event in events:
            chat_session = event["rawChatLogs"]
            for chat in chat_session:
                try:
                    date = pendulum.parse(chat.get("date", None))
                    if not bool(min_date):
                        min_date = date
                    else:
                        if date < min_date:
                            min_date = date
                    if not bool(max_date):
                        max_date = date
                    else:
                        if date > max_date:
                            max_date = date

                except pendulum.parsing.exceptions.ParserError:
                    date = chat.get("date", None)
                name = chat.get("name", "")
                body = chat.get("body", "")
                type_speaker = chat.get("type", "").lower()
                if type_speaker == "moderator":
                    moderator_chat[name].append((date, body))
                elif type_speaker == "participant":
                    participant_chat[name].append((date, body))

        return {
            "teacher_chat": moderator_chat,
            "student_chat": participant_chat,
            "next_pull_day": next_event,
            "earliest_date": min_date,
            "latest_date": max_date,
        }
