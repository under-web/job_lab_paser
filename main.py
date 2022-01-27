import time
import requests
import csv
import random
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

def csv_writer(out_data, name_file):
    with open(f"{name_file}.csv", mode="a", encoding='utf-8', errors='ignore') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=";")
        file_writer.writerow(out_data)

def get_html_data(clear_url, name_file):
    opts = Options()
    opts.headless = True
    assert opts.headless
    # browser = webdriver.Firefox(options=opts)
    global browser
    browser = webdriver.Firefox()
    browser.get('https://joblab.ru/')

    input(' Введите логин пароль и нажмите ENTER')
    for url in clear_url:
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])
        browser.get(f'{url}')
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])


        try:
            vacantion = browser.find_element('xpath', '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/h1').text
        except Exception:
            vacantion = ''


        try:
            name = browser.find_element('xpath',
                                        '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[1]/td[2]/p/b').text
        except Exception:
            name = ''

        try:
            phone_hide = browser.find_element('xpath', '//*[@id="p"]')
            time.sleep(1)
            phone_hide.click()
            time.sleep(1)
            phone = browser.find_element('xpath',
                                         '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[2]/td[2]/p/span/a').text
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

        try:
            age = browser.find_element('xpath',
                                       '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr[15]/td[2]/p').text
        except Exception:
            age = ''


        out_data = [name,
                    age,
                    phone,
                    email,
                    vacantion]
        if out_data[0] == '':
            input('Введите капчу и нажмите ENTER! ')
        csv_writer(out_data, name_file)
        # close_book()
        time.sleep(random.randint(1, waiter))
    browser.close()
    browser.quit()


# def close_book(need_book=3):
#     all_books = len(browser.window_handles)
#     if all_books >= need_book:
#         browser.switch_to.window(browser.window_handles[0])
#         browser.close()
#         time.sleep(1)


def main():
    global waiter
    page = 1
    high_page = int(input('Введите глубину парсинга (стр.): ')) + 1
    row_url = input('Вставьте ссылку для парсинга: ')
    waiter = int(input('Укажите максимальное время паузы (сек):'))
    name_file = (input('Придумайте название для файла (Например - data или output): '))

    result_list_url = []
    while page != high_page:
        l = row_url.split('&srcategory')
        url = ''.join(l[0]) + f'&page={str(page)}' + ''.join(l[1])  # в цикле собираем все урл
        result_list_url.extend(get_html_url(get_requests(url)))
        print('стр.№ ', page)
        page += 1

    get_html_data(result_list_url, name_file)  # достаем данные из собраных урл


if __name__ == '__main__':
    main()
