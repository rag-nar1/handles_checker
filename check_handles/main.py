import os
import time
import pandas as pd
import csv
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from helpers import colors
load_dotenv()

status={}
# Create chrome driver
def createDriver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return driver


# make timeout 30 seconds for command find element
def find_element(driver, by, value, timeout=40):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))


def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    except InvalidSelectorException:
        return False
    return True



def check_handle(driver,handle,file1):
    driver.get("https://codeforces.com/search")

    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/form/table/tbody/tr/td[1]/input').send_keys(handle)
    time.sleep(1)
    find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[1]/form/table/tbody/tr/td[2]/input').click()
    time.sleep(1)
    # print(check_exists_by_xpath('//*[@id="pageContent"]/div[2]/div[6]/div[2]/h3',driver))
    if check_exists_by_xpath('//*[@id="pageContent"]/div[2]/div[6]/div[2]/h3',driver):
        time.sleep(1)
        if find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[2]/div[6]/div[2]/h3').text.upper()==handle.upper():
            if(find_element(driver,By.XPATH,'//*[@id="pageContent"]/div[2]/div[6]/div[2]/h3').text==handle):
                status[handle]="1"
            else :
                status[handle]="2"
        else:
            status[handle]="0"
    else:
        status[handle]="0"
    file1.write(handle+" "+status[handle]+"\n")


    
def read_file(file):
    lol={}
    data=list(file.read().split("\n"))
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]==" " and (data[i][j+1:]=="not exists" or data[i][j+1:]=="exists"):
                lol[data[i][:j]]=data[i][j+1:]
                break
    return lol

def main():
    file=open("files/handles.csv","r")
    reader=csv.reader(file)
    filex=open("files/result.txt","r")
    lol=read_file(filex)
    print(lol)
    handles=[]
    filex.close()
    filex=open("files/result.txt","w")
    for i in reader:
        handles.append(i[0].strip())
    # print(handles)
    print(lol.keys())

    file.close()
    for i in handles:
        if lol[i]=="not exists":
            driver = createDriver()
            check_handle(driver,i,filex)
        else:
            filex.write(i+" 1"+"\n")
    


if __name__ == "__main__":
    main()