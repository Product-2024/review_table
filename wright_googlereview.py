import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rich import print
import pandas as pd



df = pd.read_csv("seoul.csv")
df = df[df["상권업종대분류코드"] == "I2"]
df = df[["상호명", "지점명", "행정동명", "법정동명", "도로명주소", "호정보"]]
df = df.fillna("")

SHOP = "토끼정"
# # the location
LOCATION = "마곡동"
# google's main URL
URL = "https://www.google.com/maps"
t=0
if __name__ == '__main__':
    with sync_playwright() as pw:
        # creates an instance of the Chromium browser and launches it
        browser = pw.chromium.launch(headless=False)
        # creates a new browser page (tab) within the browser instance
        page = browser.new_page()
        for index in df.index:
            t += 1
            row = df.iloc[index]
            SHOP = row["상호명"]
            LOCATION = row["법정동명"]
            # go to url with Playwright page element
            page.goto(URL)
            # deal with cookies page
            page.click('button#searchbox-searchbutton.mL3xi') #검색창 선택
            # write what you're looking for
            page.fill("input", f"{LOCATION} {SHOP}") # 검색어 입력
            page.keyboard.press('Enter')
            time.sleep(6)
            if page.locator("text='리뷰'").count() == 0:
                continue
            else:
                page.locator("text='리뷰'").first.click()
            # print(loc.inner_text())
            # print(page.locator("text='리뷰'").count())
            time.sleep(5)
            # create new soup
            html = page.inner_html('body')
            time.sleep(5)
            # create beautiful soup element
            soup = BeautifulSoup(html, 'html.parser')
            # scrape reviews
            reviews = soup.select('.MyEned')
            reviews = [review.find('span').text for review in reviews]
            # print reviews
            for review in reviews:
                print(review)
                print('\n')
            if t == 5:
                break
