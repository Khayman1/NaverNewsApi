# 📘 Naver 뉴스 검색 API 예제

이 프로젝트는 **네이버 오픈API**를 활용하여 원하는 검색어에 대한 뉴스 데이터를 JSON 형식으로 조회하고,  
필요한 정보를 추출해 **CSV 파일로 저장**하는 Python 스크립트입니다.

---

## 🚀 주요 기능
- 네이버 뉴스 API 연동 (JSON 형식)
- 검색어 기반 뉴스 조회
- 뉴스 제목, 링크, 설명, 날짜 추출
- HTML 태그 제거 후 가공
- 실행 시 자동으로 `.csv` 파일로 저장

---
## 📋 필수 사항
## 1. 네이버 개발자 센터 API 키 발급
네이버 개발자 센터 접속
애플리케이션 등록 후 Client ID와 Client Secret 발급
일일 25,000건 검색 제한

## 2. 입력 파일 준비
enterprise_df_14_utf8_data.csv 파일 필요
파일에 "기업명" 컬럼이 포함되어야 

---
## 🛠 사용 방법

### 1. 필수 라이브러리 설치
아래 명령어를 터미널이나 CMD에 입력하여 필수 라이브러리를 설치하세요:

```bash
bashpip install requests pandas tqdm

### 2. API 키 설정
코드 내 다음 부분을 본인의 API 키로 수정:
pythonclient_id = "YOUR_CLIENT_ID"      # 발급받은 Client ID
client_secret = "YOUR_CLIENT_SECRET"  # 발급받은 Client Secret

### 3. 실행
bashpython naver_news_search.py
