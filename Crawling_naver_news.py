# curl "https://openapi.naver.com/v1/search/news.xml?query=%EC%A3%BC%EC%8B%9D&display=10&start=1&sort=sim" \
# -H "X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}" \
# -H "X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}" -v

# Naver News API 발급 주소
# 1일 25,000건 제한
# https://developers.naver.com/main/

# Documentation: https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4
# 네이버 API 신청 현황 : https://developers.naver.com/apps/#/list


# 클라이언트 아이디 값
# 64g43aYmdLhFMenUVVVZ

# 클라이언트 시크릿 값
# LrXCNWZHsp

# 요청 코드 예시

# curl "https://openapi.naver.com/v1/search/news.xml?query=LG&display=10&start=1&sort=sim" -H "X-Naver-Client-Id: TSv_s3GbD90z6QRiBZUN" -H "X-Naver-Client-Secret: jA9u6XAoDh" -v
# curl "https://openapi.naver.com/v1/search/news.json?query=LG&display=10&start=1&sort=sim" `
#  -H "X-Naver-Client-Id: TSv_s3GbD90z6QRiBZUN" `
#  -H "X-Naver-Client-Secret: CWUFBLoPo8" `
#  --ssl-no-revoke -v

# Python 코드로 네이버 뉴스 API 호출 구현
import requests
import urllib.parse 
import json 
import os
import re
from datetime import datetime

# 데이터프레임으로 변환 및 저장
import pandas as pd
from datetime import datetime

# API 키 설정
client_id = "TSv_s3GbD90z6QRiBZUN" #개인 거 발급받아서 사용
client_secret = "jA9u6XAoDh"

# 검색어 설정 및 인코딩
query = "벡스인텔리전스"  # 검색어를 "벡스인텔리전스"로 변경
encoded_query = urllib.parse.quote(query)

# API URL 설정 (JSON 형식)
url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display=10&start=1&sort=sim"

# 헤더 설정
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
    "User-Agent": "Mozilla/5.0",  # Sometimes adding a user agent helps
}

# 디버깅용 헤더 출력
print(f"Using headers: {headers}")

# API 요청 보내기
try:
    response = requests.get(url, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {response.headers}")

    # 응답 확인 (200 정상, 201 생성 시 정상, 200/201 빼고 다 비정상)
    if response.status_code == 200:
        # JSON 결과 파싱
        data = json.loads(response.text)
        print(f"총 검색 결과: {data['total']}개")

        # 검색 결과 출력
        for idx, item in enumerate(data["items"], 1):
            print(f"\n[{idx}] {item['title']}")
            print(f"링크: {item['link']}")
            print(f"설명: {item['description']}")
            print(f"발행일: {item['pubDate']}")

        # 검색 결과 데이터프레임으로 변환
        df = pd.DataFrame(data["items"])

        # HTML 태그 제거 및 텍스트 정리
        if "title" in df.columns:
            # 모든 HTML 태그를 정규식으로 제거
            df["title"] = df["title"].apply(lambda x: re.sub(r"<.*?>", "", x))
            df["description"] = df["description"].apply(
                lambda x: re.sub(r"<.*?>", "", x)
            )

        # 현재 시간을 파일명에 추가하여 저장
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"naver_news_{query}_{current_time}.csv"

        # os.path를 사용하여 경로 생성
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(output_dir, file_name)

        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"\n데이터가 저장되었습니다: {file_path}")
    else:
        print(f"Error {response.status_code}: {response.reason}")
        print(f"Response body: {response.text}")
except Exception as e:
    print(f"Exception occurred: {e}")

# XML 형식으로 요청하려면 아래 URL을 사용
# url = f"https://openapi.naver.com/v1/search/news.xml?query={encoded_query}&display=10&start=1&sort=sim"
