import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rich import print
import pandas as pd



df = pd.read_csv("seoul.csv")
df = df[df["상권업종대분류코드"] == "I2"]
df = df[["상호명", "지점명", "행정동명", "법정동명", "도로명주소", "호정보"]]
df = df.fillna("")
df = df[df["행정동명"] == "명동"]

# SHOP = "토끼정"
# # # the location
# LOCATION = "마곡동"
# # google's main URL
global URL 
URL = "https://www.google.com/maps"
t=0

def search_review(page, keyword, ):
    page.goto(URL)
    # deal with cookies page
    page.click('button#searchbox-searchbutton.mL3xi') #검색창 선택
    # write what you're looking for
    page.fill("input", keyword) # 검색어 입력
    page.keyboard.press('Enter')
    time.sleep(6)
    if page.locator("text='검색 결과'").count() != 0:
        print("no search result")
        return -1
    else:
        if page.locator("text='리뷰'").count() == 0:
            print("no review data")
            return -2
        else:
            page.locator("text='리뷰'").first.click()
    time.sleep(4)
    # create new soup
    count = 0
    while ((page.locator("text='자세히'").all() != [])&(count<200)):
        # 스크롤을 최대 200번 하게 되어있는데 최적화 필요
        page.mouse.wheel(0, 15000)
        page.locator("text='자세히'").first.click()
        print('더보기')
        count += 1
        # page.locator("div.m6QErb.DxyBcb.kA9KIf.dS8AEf").scroll_into_view_if_needed()
        time.sleep(1)

    html = page.inner_html('body')
    time.sleep(3)
    # create beautiful soup element
    soup = BeautifulSoup(html, 'html.parser')
    # scrape reviews
    reviews = soup.select('.MyEned')
    reviews = [review.find('span').text for review in reviews]
    # print reviews
    
    for review in reviews:
        print(review)
        print('\n')
    print("Total Review Count : ", len(reviews))
    return 1


if __name__ == '__main__':
    with sync_playwright() as pw:
        # creates an instance of the Chromium browser and launches it
        browser = pw.chromium.launch(headless=False)
        # creates a new browser page (tab) within the browser instance
        page = browser.new_page()
        for index in df.index:
            t += 1
            row = df.loc[index]
            SHOP = row["상호명"]
            LOCATION = row["법정동명"]
            BRANCH = row["지점명"]
            print(f"{LOCATION} {SHOP}")
            # go to url with Playwright page element
            ret = search_review(page, f"{LOCATION} {SHOP}")
            if ret == -1:
                search_review(page, f"{SHOP} {BRANCH}")
            # if t == 5:
            #     break
