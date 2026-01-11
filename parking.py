from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

DAYS_MAP = {
    0: "MONDAY",
    1: "TUESDAY",
    2: "WEDNESDAY",
    3: "THURSDAY",
    4: "FRIDAY",
    5: "SATURDAY"
}

def run():
    with sync_playwright() as p:
        headless = os.getenv("HEADLESS", "true").lower() == "true"
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # Go to login page
        page.goto("https://secure.mipermit.com/newham/application/home.aspx")

        # Fill login form
        page.fill("#LAMemberNumber", username)
        page.fill("#LAPIN", password)
        page.click("button[type='submit']")

        # Wait for navigation or dashboard to load
        page.wait_for_load_state('networkidle')

        # Navigate to form
        page.goto("https://secure.mipermit.com/newham/Account/PayAndStayManagement.aspx?Type=SPECIAL")

        # Fill out the form
        for i in range(0, 6):
            print(f"Creating stay for {DAYS_MAP[i]}")
            page.select_option('#CreateRequestDate', str(i+1))
            page.select_option('#CreateHour', "08")
            page.select_option('#CreateMinute', "00")

            page.select_option('#CreateDuration', label="12 hours")
            page.click("#cmdCreateConfirmStay")
            page.wait_for_load_state('networkidle')
            page.click("#cmdCreateStay")
            page.wait_for_load_state('networkidle')
            time.sleep(5)
        print("Form submitted successfully.")
        browser.close()

if __name__ == "__main__":
    run()
