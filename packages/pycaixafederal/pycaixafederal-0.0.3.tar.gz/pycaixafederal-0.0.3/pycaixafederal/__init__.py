"""This module do web crawler of caixa federal."""
__version__ = "0.0.3"

import time
from datetime import datetime

import requests
import wget
import zipfile
import os

from jsmin import jsmin
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

now = datetime.now()

with open(os.path.dirname(__file__) + '/script.js') as js_file:
    minified = jsmin(js_file.read())


def __login(driver, usuario, senha):
    driver.get("https://internetbanking.caixa.gov.br/sinbc/#!nb/login")
    time.sleep(3)
    WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "nomeUsuario")))
    driver.find_element(By.ID, "nomeUsuario").send_keys(usuario)
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(3)
    WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.ID, "lnkInitials")))
    driver.find_element(By.ID, "lnkInitials").click()
    time.sleep(3)
    WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.ID, "password")))
    driver.execute_script("document.querySelector(\'#password\').value=\'" + senha.replace('\n', '') + "\'")
    driver.find_element(By.ID, "btnConfirmar").click()
    time.sleep(5)
    try:
        driver.execute_script("document.getElementById('modal-campanha').remove();")
    except Exception as error_modal:
        print('Possible not an error - modal', __login.__name__, str(error_modal))


def __extratos(driver):
    try:
        driver.execute_script(minified)
        driver.execute_script("window.pycaixa.extratos.methods.get()")
        counter = 1
        while counter > 0:
            counter = driver.execute_script('return window.pycaixa.extratos.counter')
            time.sleep(0.3)
        time.sleep(1)
        return driver.execute_script('return window.pycaixa.extratos.results')
    except Exception as error:
        print('Error', __extratos.__name__, str(error))
    return []


def __faturas(driver):
    return []


def __cdb(driver):
    return None


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    if os.path.isfile('chromedriver.exe'):
        return webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(latest_driver_zip)
    return webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)


def get(usuario, senha):
    driver = get_driver()
    __login(driver, usuario, senha)
    retorno =  {
        'transactions': __extratos(driver),
        'cards': __faturas(driver),
        'cdb': __cdb(driver)
    }
    driver.quit()
    return retorno
