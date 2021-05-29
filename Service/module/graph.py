import matplotlib.pyplot as plt
import seaborn as sns

def ad_brand (data, x_name):
    plt.figure(figsize=(50,20))
    plt.subplot(221)
    
    sns.countplot(data=data, x=x_name, order=data['Brand'].value_counts().index)
    
    plt.title('브랜드별 광고횟수', fontsize=25, y=1.03)       
    plt.xlabel('Brand', fontsize=15, labelpad=30)                         
    plt.ylabel('Count', fontsize=15, rotation=1, labelpad=30)  
    plt.xticks(rotation=90)

    plt.savefig('./ad_brand.png')
    plt.show()
    
    
def advertiser (data1, x_name1):
    plt.figure(figsize=(20, 5))
    
    avg_view = data1.groupby('Advertiser').agg('mean')[['평균시청률']].reset_index()
    avg_view.sort_values('평균시청률', ascending=False, inplace=True)
    
    plt.subplot(121)
    sns.countplot(data=data1, x=x_name1, order=data1['Advertiser'].value_counts().index)
    plt.xticks(rotation=90)
    plt.title('광고주별 광고횟수')
    
    
    plt.subplot(122)
    sns.barplot(data=avg_view, x='Advertiser', y='평균시청률')
    plt.xticks(rotation=90)
    plt.title('광고주별 평균시청률')

    plt.savefig('./advertiser.png')
    plt.show()