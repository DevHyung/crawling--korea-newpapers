from bs4 import BeautifulSoup
from selenium import webdriver
import time
browser = webdriver.Chrome('./chromedriver')
f = open("./links/동아일보.txt", 'r')
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
        title = bs4.find('h2', attrs={'class': 'title'}).get_text()
        print("제목 : ", title)

        # 날짜 가져오기
        date = bs4.find('span', attrs={'class': 'date01'}).get_text()
        date = date.replace("입력", "").lstrip()
        print("날짜 : ", date)

        # 내용 가져오기

        #   필요없는 내용 제거
        for tag in bs4.find_all('div','article_relation'):
            tag.extract()
        for tag in bs4.find_all('div','articlePhotoC'):
            tag.extract()
        for tag in bs4.find_all('div','bestnews'):
            tag.extract()
        for tag in bs4.find_all('div','btn_Journalist'):
            tag.extract()
        for tag in bs4.find_all('script'):
            tag.extract()
        for tag in bs4.find_all('p','view_copyright'):
            tag.extract()
        for tag in bs4.find_all('div','article_issue'):
            tag.extract()
        article = bs4.find('div', attrs={'class': 'article_txt'}).get_text()

        print("내용 : ", article.lstrip())
    f.close()
    browser.quit()

except:
    print("Page load Timeout Occured. Quiting !!!")
    f.close()
    browser.quit()
