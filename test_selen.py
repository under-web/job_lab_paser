import csv
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from main import get_requests, get_html_url


def get_html_data(clear_url):
    # opts = Options()
    # opts.headless = True
    # assert opts.headless
    # # browser = webdriver.Firefox(options=opts)
    # browser = webdriver.Firefox()
    # browser.get('https://joblab.ru/')

    # input('Нажмите ENTER')
    for url in clear_url:

        browser.switch_to.window(browser.window_handles[-1])
        browser.execute_script(f"window.open('{url}')")
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])

        try:
            vacantion = browser.find_element('xpath', '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/h1').text
        except Exception:
            vacantion = ''

        try:
            organization = browser.find_element('xpath',
                                                '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/p/b/a').text
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


def get_registration(start_url):
    global browser
    browser = webdriver.Firefox()
    browser.get(start_url)
    url = input('Нажмите ENTER')

    get_html_data(get_html_url(get_requests(url)))
    # browser.close()
    # browser.quit()


def main():
    start_url = 'https://joblab.ru'
    get_registration(start_url)
    # get_html_data()


if __name__ == '__main__':
    main()
