from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
''' CONFIG AREA '''
BASE_URL = 'https://search.naver.com/search.naver'
DRIVER_PATH = "./chromedriver"
SEARCH_KEYWORD = "암"
START_DATE = "2018.12.15"
END_DATE =  "2018.12.31"
JOURNAL_NAME = "조선일보"
PAGE_LIMIT = 5


if __name__ == "__main__":
# driver init
    # driver setup
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.maximize_window()
    driver.get('https://search.naver.com/search.naver?query=&where=news&ie=utf8&sm=nws_hty')

    # move to naver
    driver.find_element_by_xpath('//*[@id="nx_query"]').clear()
    driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys(SEARCH_KEYWORD+'\n')
    sleep(1)

# filtering
    driver.find_element_by_xpath('//*[@id="_search_option_btn"]').click()
    # period
    driver.find_element_by_xpath('//*[@id="snb"]/div/ul/li[2]/a').click()
    sleep(0.5)

    driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').click()
    for c in START_DATE:
        driver.find_element_by_xpath('//*[@id="news_input_period_begin"]').send_keys(c)
        sleep(0.1)

    driver.find_element_by_xpath('//*[@id="news_input_period_end"]').click()
    for c in END_DATE:
        driver.find_element_by_xpath('//*[@id="news_input_period_end"]').send_keys(c)
        sleep(0.1)
    driver.find_element_by_xpath('//*[@id="_nx_option_date"]/div[2]/span/button').click()#적용버튼
    sleep(1)
    # journal
    driver.find_element_by_xpath('//*[@id="news_popup"]/a').click()
    sleep(0.5)
    elements = driver.find_elements_by_tag_name('label')
    for e in elements:
        if JOURNAL_NAME == e.text.strip():
            e.click()
            break
    driver.find_element_by_xpath('//*[@id="_nx_option_media"]/div[2]/div[3]/button[1]').click()
    sleep(1)

    # order latest
    driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[1]/div[3]/ul/li[2]/a').click() #최신순
    sleep(1)

# parsing
    outF = open("{}_{}-{}_URL.txt".format(JOURNAL_NAME,START_DATE.replace('.',''),END_DATE.replace('.','')),'w')
    for _ in range(PAGE_LIMIT):
        bs = BeautifulSoup(driver.page_source, 'lxml')
        # extract URL
        ul = bs.find('ul',class_='type01')
        lis = ul.find_all('li')
        for li in lis:
            a = li.find('a', class_=' _sp_each_title')
            link = a['href'].strip()
            outF.write(link+'\n')

        # Paging
        pageLastA = bs.find('div', class_='paging').find_all('a')[-1]
        if pageLastA.get_text().strip() == "다음페이지":
            nextLink = BASE_URL+pageLastA['href']
            driver.get(nextLink)
        else:
            # Last page
            break
        sleep(2)
    outF.close()