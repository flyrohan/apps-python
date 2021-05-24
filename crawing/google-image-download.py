import os
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib, urllib.request
from time import sleep
from shutil import copyfileobj
from base64 import b64decode
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# origin https://coder38611.tistory.com/6

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_PATH = os.path.join(ROOT_PATH, "images")
DRIVER_PATH = os.path.join(ROOT_PATH, "chromedriver.exe")
GOOGLE_URL = "https://www.google.com/search"
DOWNLOAD_IMAGES = 5

class StatusBar():
    def init(self, window, msg):
        self.window = window        
        self.var = StringVar()
        self.entry = Entry(window, state='readonly', readonlybackground="#dfdfdf", fg='black')
        self.entry.grid(row=3, column=0, columnspan=2, sticky="we")
        self.entry.config(textvariable=self.var, relief='flat')
        self.set(msg)

    def get(self):
        return self.var.get()

    def set(self, msg):
        self.var.set(msg)
        self.entry.update()

statusBar = StatusBar()

def download_images(path, keyword, counts, hide_browser):    
    if False == os.path.isfile(DRIVER_PATH):
        message = "Not found: " + DRIVER_PATH
        messagebox.showinfo("ERROR", message)
        exit()

    if False == os.path.isdir(path):
        message = "Not found: " + path
        messagebox.showinfo("ERROR", message)
        exit()

    options = webdriver.ChromeOptions()
    options.headless = hide_browser
    statusBar.set("Connecting ...")

    try:
        driver = webdriver.Chrome(DRIVER_PATH, options=options)
        search_url = '''https://www.google.com/search?tbm=isch&source=hp&biw=&bih=&ei=0VgdX4viLcq9hwOB7IngCQ&q=''' + \
                        keyword.strip()
        driver.get(search_url)
        driver.implicitly_wait(10)

        image_urls = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')

        # 다음 페이지의 가장 밑까지 가게한다
        last_height = driver.execute_script('return document.body.scrollHeight')
        while len(image_urls) < counts:
            print('Scrolling ', len(image_urls))
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(1)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                try:
                    driver.find_element_by_class_name('mye4qd').click()
                except:
                    break
            last_height = new_height
            image_urls = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')        

        # 페이지 내 모든 이미지를 찾음
        image_urls = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
        image_url = []
        image_cnt = 0
        print('Found images: ', len(image_urls))
        statusBar.set('Found images: ' + str(len(image_urls)))

        # for thumbnail in image_urls:
        for i in range(len(image_urls)):
            thumbnail = image_urls[i]
            print("capture[", i, "]: ", thumbnail)
            statusBar.set("capture: " + str(i))
            # 원본 이미지를 다운로드하기 위해 썸네일을 클릭함            
            ActionChains(driver).click(thumbnail).perform()
            driver.implicitly_wait(10)

            # 같은 클래스를 가진 이미지가 여러개이기 때문에 xpath를 통해 지정함
            try:
                xpath = '//*[@id="islrg"]/div[1]/div['+ str(i+1) +']/a[1]/div[1]/img'
                image_url.append(driver.find_element_by_xpath(xpath).get_attribute("src"))                
            except:
                print('Not founnd elements !!!')
                continue

            image_cnt += 1
            if image_cnt >= counts:
                break

        for i, src in zip(range(image_cnt), image_url):
            index = i + 1            
            file = os.path.join(path, str(index) + ".jpg")
            urllib.request.urlretrieve(src,  file)
            if index >= counts:
                break
            print("SAVE[", index, "] ", file)
            statusBar.set("SAVE [" + str(index) + "] " + str(file))

    finally:
        # 브라우저를 닫고 더 이상의 셀레니움을 사용한 코드 실행을 멈춤
        if False == hide_browser:
            driver.quit()
        statusBar.set("DONE: " + str(path))

def create_image_dir(dir):
    try:
        if not(os.path.isdir(dir)):
            os.makedirs(os.path.join(dir))
            print("PATH: ", dir)
    except Exception as e:
            print("Failed to create directory:", e)
            exit()

def main():
    window = Tk()
    window.title("Google Image Download")
    window.resizable(width=True, height=False)

    keyword, counts =  StringVar(), StringVar()
    hide = BooleanVar() 
    counts.set(DOWNLOAD_IMAGES)
    hide.set(True)

    def btn_action():
        word = keyword.get()
        num  = int(counts.get())
        path = os.path.join(DOWNLOAD_PATH, word)        
        create_image_dir(path)
        download_images(path, word, num, hide.get())

    ttk.Label(window, text = "Keyword\t").grid(row = 0, column = 0, padx = 10, pady = 5)
    ttk.Label(window, text = "Counts\t").grid(row = 1, column = 0, padx = 10, pady = 5)
    ttk.Entry(window, textvariable = keyword).grid(row = 0, column = 1, padx = 10, pady = 5, ipadx=200)
    ttk.Entry(window, textvariable = counts).grid(row = 1, column = 1, padx = 10, pady = 5)
    ttk.Checkbutton(window, text='Hide browser', var=hide).grid(row = 2, column = 0, padx = 10, pady = 5)
    ttk.Button(window, text="Find", command=btn_action).grid(row = 2, column = 1, padx = 10, pady = 10)  
    statusBar.init(window, "Ready")    

    window.mainloop()

if __name__ == "__main__":
	main()