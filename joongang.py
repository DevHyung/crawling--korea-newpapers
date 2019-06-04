from bs4 import BeautifulSoup
from selenium import webdriver
import time
browser = webdriver.Chrome('./chromedriver')
f = open("./links/중앙일보.txt", 'r')
links = f.readlines()

try:
    for link in links:
        print(">>", link)
        browser.get(link)
        time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
        # 언론사명, 날짜, 제목, URL 정보
        # 페이지 소스 얻어오기
        bs4 = BeautifulSoup(browser.page_source, 'lxml')

        # 제목 가져오기
        title = bs4.find('h1', attrs={'class': 'headline mg'}).get_text()
        print("제목 : ", title)

        # 날짜 가져오기
        date = bs4.select('div.byline>em')[1].text
        date = date.replace("입력", "").lstrip()
        print("날짜 : ", date)

        # 내용 가져오기

        #   필요없는 내용 제거
        for tag in bs4.find_all('div','ab_photo photo_center'):
            tag.extract()
        for tag in bs4.find_all('div','ab_photo photo_left'):
            tag.extract()
        for tag in bs4.find_all('div','ab_sub_headingline'):
            tag.extract()
        for tag in bs4.find_all('div','ab_related_article'):
            tag.extract()
        for tag in bs4.find_all('div','ab_player ovp_player ovp_player16-9'):
            tag.extract()
        article = bs4.find('div', attrs={'id': 'article_body'}).get_text()
        print("내용 : ", article.lstrip())
    f.close()
    browser.quit()

except:
    print("Page load Timeout Occured. Quiting !!!")
    f.close()
    browser.quit()
