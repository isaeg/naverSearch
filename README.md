# Naver
모바일 네이버 검색 순위

# 개발 환경
* python 3.9 
* selenium 4.15.2

# 프로세스 
1. main.py ->tkinter 이용 한 gui 창
2. 창에 필요 한 값 입력
   검색 키워드 / 상호명 
3. m.naver.com 접속
4. 검색 키워드로 네이버 검색창에 검색
5. 플레이스 밑에 있는 지도 클릭
6. 스크롤 하면 li 갯수가 계속 늘어나는 형식인데 , 100개단위로 나누어짐
   => 100번째 li로 이동 /200번째 300번째 .. 형식으로 무한 스크롤 
7. 광고 딱지가 붙어있다면 제외
8. 제외 된 상호명들 리스트에 추가
9. 리스트에 setp.2 에 입력한 상호명이 있다면 종료
10. 리스트에 몇번 쨰 위치한지 출력
## 사용자 전달 
1. pyinstaller   .\naverSearch.spec  
2. pyinstaller   .\updateCheck.sepc
3. 해당 폴더 -> dist 폴더 진입
4. naverSearch.exe / updateCheck.exe / version 파일 zip 으로 묶어서 전달


## 주의사항
1. version 파일 수정 시 예전 버전으로 인식합니다.
2. main 창에 '업데이트 버전이 존재합니다' 라는 문구가 떠있다면  
  최신버전이 있다는 정보입니다.(version 파일로 구분)
3. 큰 문제가 없다면 사용해도 무방하나 updateCheck.exe 로 업데이트 이 후 사용하길 권장합니다.
4. 업데이트 하려면  릴리즈에  파일 업로드  
   (pyinstaller   .\naverSearch.spec   이 후 생긴 .exe 파일 zip으로 묶어서 업로드)
5. "assets"[0]["id"] ~~ 에러 뜨면 git 토큰 문제이므로 갱신 필요함 

## 참고사항 
1. 기본적으로 css Selector 로 진행함
2. 가끔 페이지 셀렉터 구분 값이 변경되므로 에러난 부분 체크 필요 
2-1. 안 바뀌었는데 안되면 time.sleep 늘려보기 (대부분 셀렉터 변경)
