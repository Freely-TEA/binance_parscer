import csv
from datetime import datetime
from time import sleep
import zipfile
from os import mkdir, remove
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class ParseSite:

    def __init__(self):
        self.url = 'https://www.binance.com/en/futuresng-activity/leaderboard'
        self.driver = webdriver.Firefox()
    
    def parse(self):
        driver = self.driver
        driver.get(self.url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            mkdir('data') # cоздаём папку data (на всякий случай)
        except:
            pass
        
        # выборка таблиц
        table = 1
        while table != 5:
            if table == 1:
                swith_button_1_lvl = driver.find_element_by_id('tab-PERPETUAL')
                swith_button_1_lvl.click()
                swith_button_2_lvl = driver.find_element(By.XPATH, "//div[@class='css-15bkqdg']")
                swith_button_2_lvl.click()
                sleep(1)
            elif table == 2:
                swith_button_1_lvl = driver.find_element_by_id('tab-PERPETUAL')
                swith_button_1_lvl.click()
                swith_button_2_lvl = driver.find_element(By.XPATH, "//div[@class='css-y8a5ze']")
                swith_button_2_lvl.click()
                sleep(1)
            elif table == 3:
                swith_button_1_lvl = driver.find_element_by_id('tab-DELIVERY')
                swith_button_1_lvl.click()
                swith_button_2_lvl = driver.find_element(By.XPATH, "//div[@class='css-1eas35w']")
                swith_button_2_lvl.click()
                sleep(1)
            elif table == 4:
                swith_button_1_lvl = driver.find_element_by_id('tab-DELIVERY')
                swith_button_1_lvl.click()
                swith_button_2_lvl = driver.find_element(By.XPATH, "//div[@class='css-y8a5ze']")
                swith_button_2_lvl.click()
                sleep(1)

            elem_text = []
            
            for i in range(50):
                # поиск таблицы
                elem = driver.find_element(By.XPATH, '//table')
                spam = elem.text.split('\n')
                for _ in range(5):
                    spam.pop(0)
                for el in spam:
                    elem_text.append(el)
                
                # перелистывание
                button = driver.find_elements(By.XPATH, '//button')
                if i == 0:
                    button[12].click()
                elif i == 1 or i == 48:
                    button[13].click()
                elif i == 2 or i == 47:
                    button[14].click()
                elif i == 3 or i == 46:
                    button[15].click()
                elif i >= 4 and i <= 45:
                    button[16].click()
                elif i == 49:
                    button[7].click() 
                        
            # запись в файл
            with open(f'Table-{table}.csv', mode='w', newline='', encoding='utf8') as csv_file:
                table_writer = csv.writer(csv_file, delimiter=',')
                to_write = []
                while len(elem_text) != 0:
                    for _ in range(5):
                        to_write.append(elem_text.pop(0))
                    table_writer.writerow([
                        to_write[0], #'Ranking Badge'
                        to_write[1], #'Name'
                        to_write[2], #'Daily ROI'
                        to_write[3], #'Position sharing'
                        to_write[4] #'Follow'
                    ])
                    to_write = []
            table += 1
            
    # архивирование 
    def zipping(self, name):
        zname = f'data\{name}.zip'
        zfile = zipfile.ZipFile(zname,'w')
        for i in range(1, 5):
            zfile.write(f'Table-{i}.csv')
            remove(f'Table-{i}.csv')
        zfile.close()

if __name__ == '__main__':
    # взятие времени сна
    config = ConfigParser()
    config.read('config.ini')
    sleep_time = config.get('parser', 'sleep_time')
    last_date = ''
    counting = 1
    while True:
        #### место для proxy ####
        parser = ParseSite()
        parser.parse()

        now = datetime.now().strftime("%Y-%m-%d")
        if last_date != now:
            last_date = now:
            counting = 1 
        parser.zipping(name=now)
        counting += 1

        parser.driver.close()

