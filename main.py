import time
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_requests(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    time.sleep(5)
    return r.text


def get_html_url(html):
    clear_url = []
    soup = BeautifulSoup(html, 'lxml')
    links_all = soup.find_all('a')
    for i in links_all:
        if '.html' in i.get('href'):
            clear_url.append('https://joblab.ru' + i.get('href'))
            print('https://joblab.ru' + i.get('href'))
    return clear_url


def get_html_data(clear_url):
    opts = Options()
    opts.headless = True
    assert opts.headless
    # browser = webdriver.Firefox(options=opts)
    browser = webdriver.Firefox()
    browser.get('https://joblab.ru/')

    input('Нажмите ENTER')
    for url in clear_url:

        # browser.switch_to.window(browser.window_handles[-1])
        browser.execute_script(f"window.open('{url}')")
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])


        try:
            vacantion = browser.find_element('xpath', '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/h1').text
        except Exception:
            vacantion = ''

        try:
            organization = browser.find_element('xpath', '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/p/b/a').text
        except Exception:
            organization = ''

        try:
            name = browser.find_element('xpath',
                                        '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[2]/td[2]/p').text
        except Exception:
            name = ''

        try:
            phone_hide = browser.find_element('xpath', '//*[@id="p"]')
            time.sleep(1)
            phone_hide.click()
            time.sleep(1)
            phone = browser.find_element('xpath',
                                         '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[3]/td[2]/p/span/a').text
        except Exception:
            phone = ''

        try:
            email_hide = browser.find_element('xpath', '//*[@id="m"]')
            time.sleep(1)
            email_hide.click()
            time.sleep(1)
            email = browser.find_element('xpath',
                                         '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[4]/td[2]/p/span/a').text
        except Exception:
            email = ''

        out_data = [organization,
                    name,
                    phone,
                    email,
                    vacantion]
        try:
            with open("koo.csv", mode="a", encoding='utf-8', errors='ignore') as csv_file:
                file_writer = csv.writer(csv_file, delimiter=";")
                file_writer.writerow(out_data)
        except Exception:
            continue
        browser.close()
        browser.quit()


def main():

    page = 1
    # base_url = 'https://joblab.ru/search.php?r=vac&srregion=50&srcity%5B%5D=77&page='
    base_url = 'https://joblab.ru/search.php?r=res&srregion=50&srcity%5B%5D=77&page='
    end_url = '&submit=1'

    while page != 3:
        url = base_url + str(page) + end_url
        get_html_data(get_html_url(get_requests(url)))

        print('стр.№ ', page)
        page += 1


if __name__ == '__main__':
    main()
