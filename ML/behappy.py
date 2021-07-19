import pandas as pd
def get_tv_data(data):
    data.drop(['일자','요일','시간대','프로그램','장르.1','CM위치\변수'], axis=1, inplace=True)
    data.reset_index(drop=True, inplace=True)

    for i in range(0,len(data)):
        
        data['장르'][i] = data['장르'][i].split('-')[0]


    for i in range(0,len(data)):

        data[data['채널'][i]+' '+data['장르'][i]] = 0
        data[data['채널'][i]+' '+'광고횟수'] = 0
        data[data['채널'][i]+' '+'시청자수'] = 0

    for i in range(0,len(data)):

        data[data['채널'][i]+' '+data['장르'][i]][i] = 1
        data[data['채널'][i]+' '+'광고횟수'][i] = data['광고횟수'][i]
        data[data['채널'][i]+' '+'시청자수'][i] = data['시청자수'][i]
     
    data['년월'] = data['년'].astype(str) +' '+ data['월'].str.zfill(3)

    data_i = data.drop(['Advertiser', 'Product', '년월','년','월','채널','장르','광고횟수','시청자수'], axis=1)

    df = pd.DataFrame(data_i.sum()).T

    df['index'] = data['년월'][0]
    df['Advertiser'] = data['Advertiser'][0]
    df['Product'] = data['Product'][0]

    return(df)

def get_merge_df(regi_data, tv_data):
    regi_data.fillna(0, inplace=True)

    regi_data.drop(['Unnamed: 0', 'Brand', 'Model', 'Series'], axis=1, inplace=True)

    regi_data = pd.DataFrame(regi_data.sum().T.rename('regi'))

    regi_data.reset_index(inplace=True)

    df = pd.merge(regi_data, tv_data).fillna(0)

    return(df)
