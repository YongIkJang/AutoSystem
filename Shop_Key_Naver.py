import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import json
import urllib.request
import pandas as pd
import warnings
import os
from dotenv import load_dotenv
warnings.filterwarnings(action='ignore')
load_dotenv()  # .env 읽기

# ✅ Naver API 정보 (발급받은 값 입력 필요)
client_id = os.getenv("Naver_Client_ID")
client_secret = os.getenv("Naver_Client_PASSWORD")

if not client_id:
    raise ValueError("API 키가 없습니다! .env 파일과 변수 이름 확인")

if not client_secret:
    raise ValueError("API 키가 없습니다! .env 파일과 변수 이름 확인")

#commit 확인

# ✅ API URL
url = "https://openapi.naver.com/v1/datalab/shopping/categories"

# ✅ 요청 바디
startDate = "2020-01-01"
endDate = "2020-12-31"
timeUnit = "month"
category = [
    {"name":"패션의류", "param":["50000000"]},
    {"name":"화장품/미용", "param":["50000002"]}
]
device = ""
gender = "f"
ages = ["20", "30", "40"]

body = {
    "startDate": startDate,
    "endDate": endDate,
    "timeUnit": timeUnit,
    "category": category,
    "device": device,
    "gender": gender,
    "ages": ages
}
body = json.dumps(body)

# ✅ API 요청
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type","application/json")

response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
print("응답 코드:", rescode)

if rescode == 200:
    result = json.loads(response.read())
    
    # ✅ DataFrame 생성
    df = pd.DataFrame(result['results'][0]['data'])
    df = df.rename(columns={'ratio': result['results'][0]['title']})
    
    # ✅ 다른 카테고리 데이터 추가
    for i in range(1, len(category)):
        tmp = pd.DataFrame(result['results'][i]['data'])
        tmp = tmp.rename(columns={'ratio': result['results'][i]['title']})
        df = pd.merge(df, tmp, how='left', on='period')
    
    # ✅ 날짜 변환
    df = df.rename(columns={'period': 'date'})
    df['date'] = pd.to_datetime(df['date'])
    
    print(df.head())
else:
    print("Error Code:" + str(rescode))

# ✅ 시각화
columns = df.columns[1:]
plt.figure(figsize=(12,6))
plt.title('Shopping Search Trend', size=20, weight='bold')
for col in columns:
    sns.lineplot(x=df['date'], y=df[col], label=col)
plt.ylabel("Click Ratio")
plt.legend(loc='upper right')
plt.show()
