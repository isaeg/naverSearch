import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import pat
from Demos.win32ts_logoff_disconnected import username

OWNER = 'isaeg'
REPO = 'naverSearch'
API_SERVER_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

MY_API_KEY = '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'  # 노출되면 안됨, 각자의 방법으로 보호하자.
res = requests.get(f"{API_SERVER_URL}/releases/latest", auth=(OWNER, MY_API_KEY))  #
if res.status_code != 200:
    print(datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 체크 실패")
# print(res.json())
rs  =res.json()
now_version = ''
with open("./version", "r") as f:
    now_version = f.read()

if str(rs["assets"][0]["id"]) != now_version:
    print("====================")
    print("업데이트 가능 버전을 발견했습니다.")
    print(f'''{rs["name"]} / {rs["tag_name"]}''')  # 해당 릴리즈의 제목과 태그명을 확인할 수 있음
    print(f'''{rs["body"]}''')  # 해당 릴리즈의 내용을 확인할 수 있음

    download_url = rs["assets"][0]["url"]
    contents = requests.get(download_url, auth=(username, pat), headers={'Accept': 'application/octet-stream'}, stream=True)  # 헤더와 stream을 지정하여 파일을 다운받을 수 있도록 했다.

    os.makedirs(os.path.join(application_path, "update"), exist_ok=True)  # 업데이트할 파일이 겹치지 않도록 update 폴더 생성

    # 다운받은 데이터를 태그명으로 저장
    with open(os.path.join(application_path, 'update', f'''{rs["tag_name"]}.zip'''), "wb") as f:
        for chunk in contents.iter_content(chunk_size=1024*1024):
            f.write(chunk)
    def extract(file_name):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(application_path, 'update', 'tmp'))
    test =os.path.join(application_path, "update", 'tmp')
    extract(os.path.join(application_path, 'update', f'''{rs["tag_name"]}.zip'''))
    try:
        shutil.copytree(os.path.join(application_path, "update", 'tmp'), application_path, ignore=shutil.ignore_patterns("update-check.exe",), dirs_exist_ok=True)  # update/tmp에 압축해제된 데이터를 루트에 복사하며, update-check.exe는 복사하지 않음
    except Exception as e:
        print(e)
    # 새로운 버전을 입력해 줌
    with open(os.path.join(application_path, "version"), "w") as f:
        f.write(str(rs["assets"][0]["id"]))

    shutil.rmtree(os.path.join(application_path, "update"))  # 업데이트 임시 폴더 삭제

    print(datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 완료")

    os.startfile(os.path.join(application_path, "naverSearch.exe"))

    with open("./release.txt", "a") as f:
       f.write(f'{rs["name"]}\n' )
       f.write(f'{rs["body"]}\n' )
       f.write(f'{rs["published_at"]}\n' )
       f.write("==========================\n")
else:
    print('최신 버전입니다. ')
    print(str(rs["assets"][0]["id"]))
    os.startfile(os.path.join(application_path, "naverSearch.exe"))