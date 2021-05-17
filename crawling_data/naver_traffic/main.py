import os, sys
import shutil
import json, urllib.request

import numpy as np
import pandas as pd
import copy
import seaborn as sns
import matplotlib.pyplot as plt

# api_key
client_id = #naver_api
client_secret = #naver_api

# Data.csv process
ad_df = pd.read_csv("./datas/datas.csv")
ad_df = ad_df[ad_df["values"].isna() == False].reset_index(drop=True)
ad_df = ad_df.drop("Unnamed: 0", 1)

# search_word query for crawler
search_word = ad_df[["brand_ad", "values"]]

search_dict = []
data_len = len(search_word)
brand_ad = search_word["brand_ad"].values
values = search_word["values"].str.split(",", expand=True).values

for idx in range(data_len):
    search_dict.append({"groupName": brand_ad[idx], 
                        "keywords" : values[idx][values[idx] != None].tolist()})

# json form    
def get_trend(body, client_id, client_secret):
    url = "https://openapi.naver.com/v1/datalab/search"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    return json.loads(response.read().decode('utf-8'))

#  api 가 한번에 5개의 데이터만 키워드만 검색 가능 
#  또한 정확한 키워드의 검색 양이 아닌 상대적인 값만 제시함(최대 검색 수를 100으로 설정)
# 기준이 되는 데이터 키워드가 있어야 상대적인 값을 절대적으로 변경 가능 
# 기준이 되는 값은 ASTON MARTIN_기흥인터내셔널

standard = copy.deepcopy(search_dict[0])
crop_dict = search_dict[1:]
split_list = [crop_dict[i:i+4] for i in range(0, len(crop_dict), 4)]

# naver api 사용 트랜드 데이터 수집
search_result = []

for i in range(len(split_list)) :
    insert_words = []
    split_result = [] 
    
    insert_words = copy.deepcopy(split_list[i])
    insert_words.append(standard)

    body = {
        "startDate":"2016-01-01",
        "endDate":"2021-05-05",
        "timeUnit":"date",
        "keywordGroups": insert_words
        }
        
    body = json.dumps(body, ensure_ascii=False)
    split_result.append(get_trend(body, client_id, client_secret))
    
    # 상대적인 값을 절대 적인 값으로 변경하는 작업 
    # 검색어 트렌드 스케일링 ASTON MARTIN_기흥인터내셔널의 첫날 검색 비율을 10으로 지정 
    for i in range(len(split_result[0]["results"])):
        if split_result[0]["results"][i]["title"] ==  'ASTON MARTIN_기흥인터내셔널':
            val = 10 / split_result[0]["results"][i]["data"][0]['ratio']
            
    for i in range(len(split_result[0]["results"])):
        for j in range(len(split_result[0]["results"][i]["data"])):
            split_result[0]["results"][i]["data"][j]["ratio"] =\
                                split_result[0]["results"][i]["data"][j]["ratio"] * val
    
    search_result.append(split_result)
    
# DataFrame 화 
result_df = pd.DataFrame()

for i in range(len(search_result)):
    df = pd.DataFrame(search_result[i][0]["results"])
    
    for j in range(len(df)):
        df_1= pd.DataFrame(df["data"][j])
        title = df["title"][j]
        df_1["title"] = title
        result_df = pd.concat([result_df, df_1])

# DataFrame 정리 title, subtitle로 (검색어 주제, 관련 키워드)
result_df[["title", "sub_title"]] = result_df["title"].str.split("_", expand = True)


# csv 파일로 저장 
## 파일 저장할 폴더 만들기
path = './model_data'
if os.path.isdir(path):
    shutil.rmtree(path)
    os.mkdir(path)
else:
    os.mkdir(path)

## csv save
result_df["title"] = result_df["title"].str.replace(" ","") 
title_len = len(result_df["title"].unique())

for i in range(title_len):
    title = result_df["title"].unique()[i]
    df = result_df[result_df["title"] == title]
    df.to_csv("./model_data/{}.csv".format(title), index=False) # .csv 파일 공백 제거
    
# 중복이 있는 기흥인터내셔널 정리 
ASTONMARTIN = pd.read_csv('./model_data/ASTONMARTIN.csv')
a_part = ASTONMARTIN[ASTONMARTIN["sub_title"] != "기흥인터내셔널"]
b_part = ASTONMARTIN[ASTONMARTIN["sub_title"] == "기흥인터내셔널"][:1952]
ASTONMARTIN = pd.concat([a_part, b_part], 0)
ASTONMARTIN.to_csv("./model_data/ASTONMARTIN.csv", index=False)