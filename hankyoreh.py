from bs4 import BeautifulSoup
from selenium import webdriver
import time
browser = webdriver.Chrome('./chromedriver')
f = open("./links/한겨레.txt", 'r')
links = f.readlines()
try:
    for link in links:
        try:
            print(">>", link)
            browser.get(link)
            time.sleep(5)  # 페이지 글 로딩되는거 기다려주기
            # 페이지 소스 얻어오기
            bs4 = BeautifulSoup(browser.page_source, 'lxml')

            if "well" in link or "ecotopia" in link:
                print("== well or ecotopia ==")
                # 제목 가져오기
                title = bs4.find('div', attrs={'id': 'contentBody'}).find('h1').get_text()
                print("제목 : ", title)

                # 날짜 가져오기
                date = bs4.find('span', attrs={'class': 'date'}).get_text()
                print("날짜 : ", date.strip())

                # 내용 가져오기
                for tag in bs4.find_all('span', 'image_link_wrap'):
                    tag.extract()
                article = bs4.find('div', attrs={'class': 'xe_content'}).get_text()
                print("내용 : ", article.lstrip())
            else:
                print("== news ==")
                # 언론사명, 날짜, 제목, URL 정보

                # 제목 가져오기
                #title = bs4.find('h4', attrs={'class': 'title'}).get_text()
                title = bs4.find('span', attrs={'class': 'title'}).get_text()

                print("제목 : ", title)

                # 날짜 가져오기
                date = bs4.select('p.date-time>span')[0].text
                date = date.replace("등록 :", "").lstrip()
                print("날짜 : ", date)

                # 내용 가져오기
                for tag in bs4.find_all('div', 'desc'):
                    tag.extract()
                for tag in bs4.find_all('script'):
                    tag.extract()
                for tag in bs4.find_all('div', 'image-area'):
                    tag.extract()
                article = bs4.find('div', attrs={'class': 'text'}).get_text()
                print("내용 : ", article.strip())
                '''
                http://www.hani.co.kr/arti/specialsection/esc_section/875139.html
                .iwmads{z-index:1000!important;transition:max-height 400ms ease-in-out;-webkit-transition:max-height 400ms ease-in-out;-moz-transition:max-height 400ms ease-in-out;-ms-transition:max-height 400ms ease-in-out;-o-transition:max-height 400ms ease-in-out;}.iwmads span{display:none}.ip-title h1{margin-left:35px!important}.ip-title h1:before{background-image:url(//cdn.interworksmedia.co.kr/PID0900/CM/A/logo.jpg)}.ip-icons .close{top:10px;right:10px;width:20px;height:20px;}
                힐스 에비뉴 삼송역 스칸센
                이 내용 안빠짐
                '''
        except:
            print("pass")
            pass
    f.close()
    browser.quit()

except:
    print("Page load Timeout Occured. Quiting !!!")
    f.close()
    browser.quit()
