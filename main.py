from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,time,sys,json

dir_path = '.\\videos'
count = 0
lst = []

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        lst.append(os.path.join(dir_path, path))
        count += 1
print("   ", count, " Videos found in the videos folder, ready to upload...")
print(lst)

dir_path = '.\\account profiles'
count = 0
lst1 = []

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        lst1.append(os.path.abspath(os.path.join(dir_path, path)))
        count += 1
print("   ", count, " Json Files found in the Account folder ...")

for i in range(count):
    file_name = os.path.basename(lst1[i])
    print("        ","{} : {}".format(i,file_name))

response_ = int(input("Which One You Need To Upload : "))
f = open(lst1[response_])
l = json.load(f)

options = webdriver.ChromeOptions()
options.add_argument('--profile-directory={}'.format(l["profilenum"]))
options.add_argument("--user-data-dir={}".format(l["profilepath"]).replace("\\","\\\\")) #Path to your chrome profile
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

driver.get("https://www.tiktok.com/upload?lang=en")

def caption(file_name):
    try:
        iframe = driver.find_element(By.XPATH,"//iframe[@src='https://www.tiktok.com/creator#/upload?lang=en']")
        driver.switch_to.frame(iframe)
    except:
        pass

    #notranslate public-DraftEditor-content

    check_txt = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content'))).text

    if check_txt.lower()==file_name:
        print("Caption Already Added")
    else:
        print(check_txt)
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content'))).clear()
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'public-DraftEditor-content'))).send_keys(file_name)
        print("Added File Name As Caption Successfully")

def copyrightcheck():
    try:
        iframe = driver.find_element(By.XPATH,"//iframe[@src='https://www.tiktok.com/creator#/upload?lang=en']")
        driver.switch_to.frame(iframe)
    except:
        pass

    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'tiktok-switch__switch-inner'))).click()

    while True:
        b = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'copyright')))
        b = b.find_element(By.CLASS_NAME,"tool-tip").text
        if "checking" in b.lower():
            continue
        elif "no issues detected" in b.lower():
            
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-post'))).click()
            print("No Issue Uploading")
            break

def upload_module(file_path):
    response=False
    try:
        iframe = driver.find_element(By.XPATH,"//iframe[@src='https://www.tiktok.com/creator#/upload?lang=en']")
        driver.switch_to.frame(iframe)
    except:
        pass
    
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'file-select-button')))
        response = True
    except:
        response=False

    if response:
        v = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'upload')))
        x = v.find_element(By.XPATH,"//input[@type='file']")
        x.send_keys(file_path)

        while True:
            try:
                v = driver.find_element(By.CLASS_NAME,"change-video-btn").text
                print(v)
                if "change video" in v.lower():
                    print("Done Uploading")
                    time.sleep(1)
                    break
            except:
                time.sleep(0.5)

def checkuploaded():
    try:
        v = driver.find_element(By.CLASS_NAME,"tiktok-modal__modal-title").text
        if "uploaded" in v.lower():
            driver.find_element(By.CLASS_NAME,"tiktok-modal__modal-button").click()
            return
    except:
        time.sleep(0.5)

for i in lst:
    file_ = os.path.abspath(i)
    upload_module(file_)
    caption(os.path.basename(file_).replace(".mp4",""))
    time.sleep(1)
    copyrightcheck()
    checkuploaded()
    time.sleep(0.5)

print("All Done Successfully")
input()
