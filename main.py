#Вакансия: div class="vacancy-serp-item__layout"
#Ссылка: а class="bloko-link" "href"
#Вилка: зарплаты span data-qa="vacancy-serp__vacancy-compensation"
#Компания: a data-qa="vacancy-serp__vacancy-employer"
#Город: div data-qa="vacancy-serp__vacancy-address"

import requests
from bs4 import BeautifulSoup
import fake_headers
import json

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

main_response = requests.get("https://spb.hh.ru/search/vacancy?L_save_area=true&text=python%2C+Django%2C+Flask&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50", headers=gen_headers())
main_html_data = main_response.text
main_soup = BeautifulSoup(main_html_data, "lxml")

vacancies = main_soup.find_all("div", class_="vacancy-serp-item__layout")
parsed_data = []
for vacancy in vacancies:
    link = vacancy.find("a", class_="bloko-link")["href"]

    salary_compensation = vacancy.find("span", {"data-qa":"vacancy-serp__vacancy-compensation"})
    if salary_compensation:
        salary = salary_compensation.text
    else:
        salary = f"зарплата не указана"
    company = vacancy.find("a", {"data-qa":"vacancy-serp__vacancy-employer"}).text
    city = vacancy.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text

    parsed_data.append({
        "link": link,
        "salary": salary,
        "company": company,
        "city": city
    })

    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)







