import csv
from selenium.webdriver.common.by import By

class Login:
    def __init__(self, driver):
        self.driver = driver

        with open('keys.csv', mode='r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                user = row['user']
                password = row['password']

        self.user = user
        self.password = password

        self.username_locator = '//*[@name="email"]'
        self.password_locator = '//*[@name="password"]'
        self.submit_locator = '//span[contains(text(), "Inicia sesión")]'

    def login(self):
        driver = self.driver

        driver.find_element(By.XPATH, self.username_locator).send_keys(self.user)
        driver.find_element(By.XPATH, self.password_locator).send_keys(self.password)
        driver.find_element(By.XPATH, self.submit_locator).click()

        print("Ingreso completado")