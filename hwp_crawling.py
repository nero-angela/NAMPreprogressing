#-*- coding: utf-8 -*-
import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def getNAMFileInfo(html, kind):
    # html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # 파일 정보
    links = soup.select('#ajaxResult a')
    fileInfoList = []
    hashs = []
    for link in links:
        href = link['href']
        hrefReg = re.findall('fn_pdfPopup', href)
        if len(hrefReg) > 0:
            fileInfo = re.findall('\'(.*?)\'', href)
            hashStr = hash(frozenset(fileInfo))
            if hashStr not in hashs:
                print(hashStr)
                hashs.append(hashStr)
                if kind == "HWP":
                    paddingSize = len(fileInfo[1])
                    file = str(int(fileInfo[1])+1).zfill(paddingSize)
                else:
                    file = fileInfo[1]
                fileInfoList.append("fn_fileDown('" + fileInfo[0] + "', '" + file + "')")
    print(fileInfoList)
    return fileInfoList

# kind = PDF / HWP
def getNationalAssemblyMinutes(url, kind):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("detach", True)
    driver = webdriver.Chrome('/Users/apple/Library/WebDriver/chromedriver', chrome_options=chromeOptions)
    driver.get(url)
    driver.execute_script("fn_movePage('1000', '1')")
    html = driver.find_element_by_css_selector('body').get_attribute('innerHTML')

    fileInfoList = getNAMFileInfo(html, kind)
    for fileInfo in fileInfoList:
        driver.execute_script(fileInfo)

getNationalAssemblyMinutes("http://likms.assembly.go.kr/record/mhs-30-011.do", "HWP")
