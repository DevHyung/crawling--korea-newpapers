from bs4 import BeautifulSoup
from selenium import webdriver
import time


f = open("./조선일보.txt", 'r')
links = f.readlines()
print(links)
browser = webdriver.Chrome('./chromedriver')
try:
    for link in links:
        print(">>", link)
        if "biz" in link:
            print("== biz ==")
            browser.get(link)

            time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
            # 언론사명, 날짜, 제목, URL 정보
            # 페이지 소스 얻어오기
            bs4 = BeautifulSoup(browser.page_source, 'lxml')

            # 제목 가져오기
            title = bs4.find('h1', attrs={'id': 'news_title_text_id'}).get_text()
            print("제목 : ", title)

            # 날짜 가져오기
            date = bs4.find('div', attrs={'class': 'news_date'}).get_text()
            date = date.replace("입력", "").split('|', 1)[0].lstrip()
            print("날짜 : ", date)


            # 내용 가져오기
            articles = bs4.find_all('div', attrs={'class': 'par'})
            for article in articles:
                for span in bs4.find_all("span", attrs={'class': 'par_in_ad'}):
                    span.decompose()
                print("내용 : ", article.get_text())

        else:
            print("== news == ")
            browser.get(link)

            time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
            # 언론사명, 날짜, 제목, URL 정보
            # 페이지 소스 얻어오기
            bs4 = BeautifulSoup(browser.page_source, 'lxml')

            # 제목 가져오기
            title = bs4.find('h1', attrs={'id': 'news_title_text_id'}).get_text()
            print("제목 : ", title)

            # 날짜 가져오기
            date = bs4.find('div', attrs={'class': 'news_date'}).get_text()
            date = date.replace("입력", "").split('|', 1)[0].lstrip()
            print("날짜 : ", date)

            # 내용 가져오기
            articles = bs4.find_all('div', attrs={'class': 'par'})
            for article in articles:
                for span in bs4.find_all("span", attrs={'class': 'par_in_ad'}):
                    span.decompose()
                print("내용 : ", article.get_text())

        f.close()
        browser.quit()
except:
    print("Page load Timeout Occured. Quiting !!!")
    f.close()
    browser.quit()
