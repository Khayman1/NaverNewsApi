import requests
import urllib.parse
import json
import os
import re
from datetime import datetime
from tqdm import tqdm
# 데이터프레임으로 변환 및 저장
import pandas as pd
from datetime import datetime
import time

# API 키 설정
client_id = "TSv_s3GbD90z6QRiBZUN" #개인 거 발급받아서 사용
client_secret = "jA9u6XAoDh"

# 검색어 설정 및 인코딩
# query = "벡스인텔리전스"  # 검색어를 "벡스인텔리전스"로 변경
# encoded_query = urllib.parse.quote(query)
corp_name_list = pd.read_csv("enterprise_df_14_utf8_data.csv")["기업명"].dropna().unique().tolist()

# 헤더 설정
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
    "User-Agent": "Mozilla/5.0",  # Sometimes adding a user agent helps
}

all_results = []

# 디버깅용 헤더 출력
print(f"Using headers: {headers}")

for corp_name in tqdm(corp_name_list, desc="기업별 뉴스 검색", unit="기업"):
    try:
        time.sleep(1) #서버 부하 방지
        query = urllib.parse.quote(corp_name)
        url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&start=1&sort=sim"
        #Api 요청보내기
        response = requests.get(url, headers=headers)
        
        # 응답 확인 (200 정상, 201 생성 시 정상, 200/201 빼고 다 비정상)
        if response.status_code == 200:
            # JSON 결과 파싱
            data = json.loads(response.text)
            # print(f"총 검색 결과: {data['total']}개")
            
            # 검색 결과 출력
            # for idx, item in enumerate(data["items"], 1):
            #     print(f"\n[{idx}] {item['title']}")
            #     print(f"Original link: {item['originallink']}")
            #     print(f"링크: {item['link']}")
            #     print(f"설명: {item['description']}")
            #     print(f"발행일: {item['pubDate']}")
            
            # 검색 결과 데이터프레임으로 변환
            df = pd.DataFrame(data["items"])
            
            # 기업명 컬럼 추가
            df["기업명"] = corp_name
            
            # HTML 태그 제거 및 텍스트 정리
            if "title" in df.columns:
                # 모든 HTML 태그를 정규식으로 제거
                df["title"] = df["title"].apply(lambda x: re.sub(r"<.*?>", "", x))
                df["description"] = df["description"].apply(
                    lambda x: re.sub(r"<.*?>", "", x)
                )
            
            # all_results에 추가
            all_results.append(df)
            
        else:
            print(f"Error {response.status_code}: {response.reason}")
            print(f"Response body: {response.text}")
    except Exception as e:
        print(f"Exception occurred for '{corp_name}': {e}")

# 모든 결과를 하나의 데이터프레임으로 합치기
if all_results:
    final_df = pd.concat(all_results, ignore_index=True)
    
    # 기업명 컬럼을 맨 앞으로 이동
    cols = ['기업명'] + [col for col in final_df.columns if col != '기업명']
    final_df = final_df[cols]
    
    # 현재 시간을 파일명에 추가하여 저장
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 파일 이름 설정 (모든 기업 데이터가 들어있다는 의미로 'all_news' 사용)
    file_name = f"naver_news_14_{current_time}.csv"
    
    # os.path를 사용하여 경로 생성
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(output_dir, file_name)
    
    final_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"\n🎉데이터가 저장되었습니다: {file_path}")
    print(f"총 {len(final_df)}개의 뉴스 기사가 저장되었습니다.")
else:
    print("저장할 데이터가 없습니다.")

# XML 형식으로 요청하려면 아래 URL을 사용
# url = f"https://openapi.naver.com/v1/search/news.xml?query={encoded_query}&display=10&start=1&sort=sim"