# -*- coding: utf-8 -*-
import random
import re
import threading

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta
from tkinter import *
import requests


root = Tk()
root.title("네이버 검색순위")
root.minsize(width=400, height=100)
root.maxsize(width=400, height=150)

OWNER = 'isaeg'
REPO = 'naverSearch'
API_SERVER_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

MY_API_KEY = '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'  # 노출되면 안됨, 각자의 방법으로 보호하자.
res = requests.get(f"{API_SERVER_URL}/releases/latest", auth=(OWNER, MY_API_KEY))  #
if res.status_code != 200:
    print(datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 체크 실패")
# print(res.json())
rs  =res.json()
new_version = str(rs["assets"][0]["id"])
with open("./version", "r") as f:
    now_version = f.read()

# progress.stop()
    # e.delete(0, END)


def versionCheck(now,new):
    if now != new:
        print("====================")
        print("업데이트 가능 버전을 발견했습니다.")
        return True
    else:
        return False

def scroll(driver):
    while True:
        #loc-main-section-root > div > div.YXb5L > a
        driver.execute_script("window.scrollBy(0,800);")
        mainSelector ='#place-app-root'
        time.sleep(1)
        # moreSelector = '#place-main-section-root > div > div > a'
        # time.sleep(2)
        try:
            mainInput = driver.find_element(By.CSS_SELECTOR,mainSelector)
            time.sleep(2)
            getLink = mainInput.find_element(By.CLASS_NAME,'LNifq')
            # moreInput = driver.find_element(By.CSS_SELECTOR, moreSelector)
            getLink.send_keys(Keys.ENTER)
            return True
        except:
            return False


def check_elements(nums):
    n = len(nums)
    for i in range(n - 1):
        if nums[i] >= nums[i + 1]:
            return True
    return False


def start(key,detail):
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36')
    options.add_argument("--disable-logging")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    url = "https://m.naver.com/"
    driver.get(url)

    keyword = key
    detailName = detail.strip()

    searchSelector = '#MM_SEARCH_FAKE'
    searchMSelector = '#query'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, searchSelector)
    ))
    postInput = driver.find_element(By.CSS_SELECTOR, searchSelector)
    postInput.click()

    searchMInput = driver.find_element(By.CSS_SELECTOR, searchMSelector)
    searchMInput.click()
    time.sleep(2)
    searchMInput.send_keys(keyword)
    time.sleep(random.randrange(2, 4))
    searchButtonSelector = '#sch_w > div > form > button'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, searchButtonSelector)
    ))
    searchButtonInput = driver.find_element(By.CSS_SELECTOR, searchButtonSelector)
    searchButtonInput.click()

    '''검색 이 후 더보기 찾기 '''
    scrollFlag = scroll(driver)

    if not scrollFlag:
        return "모바일 웹 - 더 보기가 막혔습니다.. 키워드 변경 / 잠시 후 해주세요 "
    # while True:
    #     driver.execute_script("window.scrollBy(0,800);")
    #     moreSelector = '#place-main-section-root > div > div > a'
    #     time.sleep(2)
    #     try:
    #         moreInput = driver.find_element(By.CSS_SELECTOR, moreSelector)
    #         time.sleep(2)
    #         moreInput.send_keys(Keys.ENTER)
    #         break
    #     except:
    #         break
    #         return "잠시 후 다시해주세요"

    # li 모두 포함 셀렉터
    adLinks = []
    # driver.find_element(By.TAG_NAME, 'body').click()
    time.sleep(1)

    # liInput = placeInput.find_elements(By.TAG_NAME, 'li')
    # adCheck = liInput.find_element(By.CLASS_NAME, "cZnHG")
    links = []
    adLinkArr =[]
    realLinks = []

    maxLink = []
    while True:
        # placeSelector = '#_list_scroll_container > div > div > div:nth-child(2) > ul'
        cnt = 0
        linkCnt = 0
        placeSelector = 'eDFz9'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, placeSelector)
        ))
        placeInput = driver.find_element(By.CLASS_NAME, placeSelector)
        liInput = placeInput.find_elements(By.TAG_NAME, 'li')
        print('li 링크 갯수 확인합시다' , len(liInput))
        linkCnt += 1
        maxLink.append(len(liInput))
        print('max ???' , maxLink)
        # 광고는 없애버립시다잉
        for i in range(len(liInput)):
            if not '광고' in liInput[i].text:
                realLinks.append(liInput[i])
        if len(realLinks) > 2000:
            return f'{len(realLinks)} 순위 밖입니다'
        action = ActionChains(driver)
        action.move_to_element(realLinks[len(realLinks)-1]).perform()
        ## 스크롤 시 더 이상 있는지 없는지 체크


        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        for i in range(len(realLinks)):
            eachLink = realLinks[i]
            try:
                # findText = eachLink.find_element(By.CLASS_NAME,'TYaxT')
                # class 명 바뀌면 업데이트 해야함 >> 더보기 에서 상호명들 class 임
                findText = eachLink.find_element(By.CLASS_NAME,'place_bluelink')
                spanText = findText.find_element(By.TAG_NAME,'span')
                links.append(spanText.text)
            except:
                print('찾고있는 장소가 없으신가요?? 가 떳어요 ')
                print('요기는 넘겨야갯징')
        # 중복제거
        # links = set(links)
        # links = list(links)
        # 순서 유지하고 중복 제거
        print('-------before-------', len(links))
        links = list(dict.fromkeys(links))
        print('--------after------', len(links))
        print(links)
        if cnt == 0:
            if len(realLinks) <100:
                break
        cnt += 1
        if detailName in links:
            break
        result = check_elements(maxLink)
        if result:
            break

    if detailName in links:
        index = links.index(detailName)
        print(f"'{detailName}'은 {index + 1} 순위입니다.")
        return f"'{detailName}'은 {index + 1} 순위입니다."
    else:
        return "등록이 안되있네요.."




def btncmd():
    # 내용 출력
    print(keyword.get()) # 1 : 첫번째 라인, 0 : 0번째 column 위치
    print(detailName.get()) # 1 : 첫번째 라인, 0 : 0번째 column 위치
    # progress_label2 = Label(root, text="작업 진행 중...")
    # progress_label2.grid(row=5, column=1, pady=10)  #
    update_label3 = Label(root, text='')
    update_label3 = Label(root, text='기다려주세용')
    update_label3.grid(row=3, column=1, pady=10)  #
    btn.config(state="disabled")

    key =keyword.get()
    detail =detailName.get()

    def long_task():
        result = start(key,detail)
        root.after(0, lambda: handle_result(result,update_label3))

    threading.Thread(target=long_task).start()

def handle_result(result,update_label3):
    # progress_label2.config(text="끝!!!")
    update_label3.config(text = result)  #
    btn.config(state="normal")
    return

def on_tab(event):
    current_widget = event.widget
    all_widgets = current_widget.master.winfo_children()

    # 현재 위젯의 인덱스 찾기
    current_index = all_widgets.index(current_widget)

    # 다음 위젯으로 이동
    next_index = (current_index + 1) % len(all_widgets)
    next_widget = all_widgets[next_index]
    next_widget.focus_set()

label = Label(root, text="검색 키워드 :")
# label.pack(side=LEFT, padx=20, pady=40)
label.grid(row=1, column=0)
keyword = Entry(root, width=20, fg='gray')
keyword.insert(END, "키워드 입력하세요")
keyword.grid(row=1, column=1)

label2 = Label(root, text="상호명  :")
label2.grid(row=2,column=0)
detailName = Entry(root,width=20 ,fg='gray')
detailName.grid(row=2, column=1)
detailName.insert(END, "상호명 입력하세요")

label3 = Label(root, text="순위:")
label3.grid(row=3, column=0)
now = now_version
new = new_version
checkFlag = versionCheck(now,new)
if checkFlag:
    update_label4 = Label(root, text="업데이트 버전이 존재합니다")
    update_label4.grid(row=4, column=0, pady=10)  #
else:
    update_label4 = Label(root, text="최신버전입니다.")
    update_label4.grid(row=4, column=0, pady=10)  #
btn = Button(root, text="검색", command=btncmd ,width=20)
btn.grid()

label.bind("<Tab>", on_tab)
label2.bind("<Tab>", on_tab)
label3.bind("<Tab>", on_tab)



root.mainloop()