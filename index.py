import csv
import json

from selenium import webdriver
from selenium.common.exceptions import (TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-logging")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

from logIn import *


def test_login():
    driver.get("https://platzi.com/login/")

    login_form = Login(driver)
    login_form.login()


def course_data_scraper():
    with open('data_school_courses.csv', mode='r', encoding='utf-8') as f:
        csvfile = csv.DictReader(f)

        for row in csvfile:
            cursos = row['cursos']

            replaced_row = cursos.replace("clases","")
            replaced_row = replaced_row.replace("/","")
            replaced_row = replaced_row.replace("-"," ")

            print(f'Recogiendo datos del curso: {replaced_row}')

            full_link_name = f'https://platzi.com{cursos}'
            driver.get(full_link_name)

            try:
                online_flag = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@class="CourseDetail-left-title"]')))

                if online_flag:
                    course_name = driver.find_element(By.XPATH, '//*[@class="CourseDetail-left-title"]').text
                    course_level = driver.find_element(By.XPATH, '//*[@class="CourseLevel-label"]').text
                    course_duration = driver.find_element(By.XPATH, '//*[@class="CourseDetail-middle-right"]//span').text
                    teacher_name = driver.find_element(By.XPATH, '//*[@class="TeacherList-full-name"]').text

                    href_lst = []
                    class_links = driver.find_elements(By.XPATH, '//*[@id="timeline-v2"]//a[@class="MaterialItem-anchor"]')
                    for link in class_links:
                        link.get_attribute("href")
                        href_lst.append(f'https://platzi.com{link}')

                    dictionary = {
                        'Course_name': course_name,
                        'Url': full_link_name,
                        'Teacher': teacher_name,
                        'Duration': course_duration,
                        'Level': course_level,
                        'Course_classes': href_lst
                    }

                    with open('output.json', mode='a', encoding='utf-8') as outfile:
                        json.dump(
                            f'[{dictionary},'
                            , outfile)

            except TimeoutException:
                print(f'No se pudo acceder al curso: {replaced_row}')
                with open('output.json', mode='a', encoding='utf-8') as outfile:
                        json.dump('[', outfile)

        with open('output.json', mode='a', encoding='utf-8') as outfile:
            json.dump(']', outfile)


if __name__ == '__main__':
    test_login()
    course_data_scraper()