import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
start = time.time()
latitude = 24.953756
longitude = 121.225314
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
    "91.0.4472.124 Mobile Safari/537.36 Edg/91.0.864.67"
}
def crawler(n):
    url = "https://ifoodie.tw/explore/list/火鍋?place=current&latlng=" + str(latitude) + "%2C" + str(longitude) + "&sortby=distance&opening=true&page=" + str(n)
    data = requests.get(url, headers)
    root = BeautifulSoup(data.text, "lxml")
    #data.encoding = "UTF-8"
    # 爬取前五筆餐廳卡片資料
    cards = root.find_all("div", class_="jsx-4284778824 restaurant-info", limit=5)
    content = ""
    url_distance = "https://www.google.com.tw/maps/dir/" + "桃園市中壢區中和路139號"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(10)
    browser.get(url_distance)
    for card in cards:
        name = card.find("a", class_="jsx-4284778824 title-text").text # 餐廳名稱
        rate = card.find("div", class_="jsx-1207467136 text") # 餐廳評價
        address = card.find("div", class_="jsx-4284778824 address-row").text  # 餐廳地址
        search = browser.find_element_by_xpath("//*[@id='sb_ifc51']/input")
        search.send_keys(address)
        search.send_keys(Keys.ENTER)
        browser.find_element_by_xpath("//*[@id='omnibox-directions']/div/div[2]/div/div/div[1]/div[2]/button/img").click()
        distances = browser.find_element_by_xpath("//*[@id='section-directions-trip-0']/div/div[1]/div[1]/div[2]/div")
        distance = "您距離此餐廳大約:" + distances.text
        picture = card.find("img").get("data-src")
        if picture == None:
            picture = card.find("img").get("src")
        if rate == None:
            content += f"{name} \n暫無評分 \n{address} \n{distance}\n{picture}\n\n"
            # 將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
        else:
            content += f"{name} \n{rate.text}顆星 \n{address} \n{distance}\n{picture}\n\n"
            # 將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
        search.clear()
    browser.quit()
    print(content, end="")
    if(content == ""):
        return False
    else:
        return True


#page = 1
#while crawler(page):
#    page += 1
crawler(1)
end = time.time()

print(end - start)