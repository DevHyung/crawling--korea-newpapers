from bs4 import BeautifulSoup
from selenium import webdriver
import time
browser = webdriver.Chrome('./chromedriver')
f = open("./links/경향신문.txt", 'r')
links = f.readlines()

try:
    for link in links:
        print(">>", link)
        browser.get(link)
        time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
        # 언론사명, 날짜, 제목, URL 정보
        # 페이지 소스 얻어오기
        bs4 = BeautifulSoup(browser.page_source, 'lxml')
        print(">>>", browser.current_url)
        if "h2" in browser.current_url:
            print("== h2 ==")
            # 언론사명, 날짜, 제목, URL 정보

            # 제목 가져오기
            title = bs4.find('div', attrs={'class': 'art_tit'}).get_text()
            print("제목 : ", title.strip())

            # 날짜 가져오기
            dates = bs4.find_all('div', attrs={'class': 'art_date'})
            for d in dates:
                if "수정" not in d.get_text():
                    date = d.get_text()
            print("날짜 : ", date.replace("입력", "").strip())

            # 내용 가져오기
            articles = bs4.find_all('p', attrs={'class': 'art_text'})
            for tag in bs4.find_all('a', attrs={'target': '_blank'}):
                tag.extract()
            print("내용 : ")
            for article in articles:
                print(article.get_text().strip())
        elif "biz" in browser.current_url:
            print("== biz ==")
            # 언론사명, 날짜, 제목, URL 정보

            # 제목 가져오기
            title = bs4.find('h1', attrs={'id': 'articleTtitle'}).get_text()
            print("제목 : ", title.strip())

            # 날짜 가져오기
            date = bs4.select('div.byline>em')[0].text
            date = date.replace("입력 :", "").lstrip()
            print("날짜 : ", date)

            # 내용 가져오기
            articles = bs4.find_all('p', attrs={'class': 'content_text'})
            print("내용 : ")
            for article in articles:
                print(article.get_text().strip())
        else:
            print("== news ==")
            # 언론사명, 날짜, 제목, URL 정보

            # 제목 가져오기
            title = bs4.find('h1', attrs={'id': 'article_title'}).get_text()
            print("제목 : ", title.strip())

            # 날짜 가져오기
            date = bs4.select('div.byline>em')[0].text
            date = date.replace("입력 :", "").lstrip()
            print("날짜 : ", date)

            # 내용 가져오기
            for tag in bs4.find_all('div', 'art_photo_wrap'):
                tag.extract()
            article = bs4.find('div', attrs={'class': 'art_body'}).get_text()
            print("내용 : ", article.strip())
    f.close()
    browser.quit()

except:
    print("Page load Timeout Occured. Quiting !!!")
    f.close()
    browser.quit()
