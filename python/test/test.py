import urllib.parse
import urllib.request
import json
import requests
import time
import glob
from fpdf import FPDF,HTMLMixin


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options() # 啟動無頭模式
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('--headless')  #規避google bug
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
option = webdriver.ChromeOptions()
option.add_argument("--window-size=1280,1024")
option.add_argument("--hide-scrollbars")
url='https://kktix.com/events.json?search=0xFE'

# 請求頭資訊
herders={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36', 'Referer':'https://movie.douban.com','Connection':'keep-alive'}

# 設定請求頭
req = urllib.request.Request(url,headers=herders)
# 發起請求，得到response響應
response=urllib.request.urlopen(req)


# json轉換為字典
hjson = json.loads(response.read())

# driver = webdriver.Chrome()
# 印出他的URL
for item in hjson["entry"]:
    print(item["url"])
a=item["url"]
executable_path = './chromedriver'
driver = webdriver.Chrome(executable_path=executable_path,
chrome_options=chrome_options)

driver.get(a) 




print("-------列印頁面的標題-------")
print(driver.title) 
#下載圖片
print("-------下載封面圖片-------")
banner = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/img").get_attribute('src')
url=banner
r=requests.get(url)
scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(scroll_width, scroll_height)

imgtime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
driver.save_screenshot('images/'+imgtime+'第一步截圖.png') 

with open('./images/封面.jpg','wb') as f:
#將圖片下載下來
    f.write(r.content)
print("-------列印頁面文字-------")
text =driver.find_element_by_class_name('description').text
print(text)
print('-------下一步-------')             
button=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[7]/a")
button.click()


print('-------關閉登入通知-------')
wait = WebDriverWait(driver, 10)
button1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button1.click()
print('-------購買票數-------')
wait = WebDriverWait(driver, 10)
input1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ticket_344407"]/div/span[3]/button[2]')))
input1.click()
print('-------同意授權條款-------')
wait = WebDriverWait(driver, 10)
check1= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="person_agree_terms"]')))
check1.click()

driver.save_screenshot('images/'+imgtime+'第二步截圖.png') 
print('-------下一步-------')
wait = WebDriverWait(driver, 10)
button3= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationsNewApp"]/div/div[5]/div[4]/button')))
button3.click()
print('-------關閉登入通知-------')
wait = WebDriverWait(driver, 10)
button4= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestModal"]/div[2]/div/div[3]/button')))
button4.click()

#讀取基本資料json 
f = open('text.json','r',encoding="utf-8")
hjson = json.loads(f.read())
print('-------填寫姓名-------')
wait = WebDriverWait(driver, 10)
name= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701843"]/div/div/input')))
name.send_keys(hjson['name'])
print('-------填寫信箱-------')
wait = WebDriverWait(driver, 10)
email= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_email_701844"]/div/div/input')))
email.send_keys(hjson['email'])
print('-------填寫電話-------')
wait = WebDriverWait(driver, 10)
phone= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701845"]/div/div/input')))
phone.send_keys(hjson['phone'])
print('-------填寫代號-------')
wait = WebDriverWait(driver, 10)
input3= wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="field_text_701846"]/div/div/input')))
input3.send_keys(hjson['datecode'])
f.close


print('-------同意授權條款-------')
wait = WebDriverWait(driver, 10)
check2 =wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="person_agree_terms"]')))
check2.click()


driver.save_screenshot('images/'+imgtime+'第三步截圖.png') 
print('-------確認表單資料-------')
button4=driver.find_element_by_xpath('//*[@id="registrations_controller"]/div[4]/div[2]/div/div[6]/a')
button4.click()

print('-------恭喜!您已完成購票-------') 
time.sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.save_screenshot('images/'+imgtime+'完成截圖.png') 
  
pdf = FPDF()
pdf.add_font('微軟正黑體','','微軟正黑體-1.ttf',True)
pdf.set_font('微軟正黑體', size=16)
pdf.add_page()
pdf.text(100,100,"第一步")
pdf.image('images/'+imgtime+'第一步截圖.png', 1, 1, w=150)
pdf.add_page()
pdf.text(100,100,"第二步")
pdf.image('images/'+imgtime+'第二步截圖.png', 1, 1, w=150)
pdf.add_page()
pdf.text(100,100,"第三步")
pdf.image('images/'+imgtime+'第三步截圖.png', 1, 1, w=150)
pdf.add_page()
pdf.text(100,100,"完成")
pdf.image('images/'+imgtime+'完成截圖.png', 1, 1, w=150)
pdf.output('0xFE.pdf')



