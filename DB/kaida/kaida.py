from selenium import webdriver
from selenium.webdriver.support.select import Select
import time 
import pandas as pd
from bs4 import BeautifulSoup
import configparser

def clear_menu(driver):
    from selenium import webdriver
    # 나이 체크박스 초기화
    driver.execute_script("$('#td_Age > .item_wrap > label > input').prop('checked', false);")
    # tag 초기화
    driver.execute_script("$('.sel_item button').click();");
    
def select_menu(driver, sales_type_id, age_id, year):

    import time
    from selenium.webdriver.support.select import Select
    from selenium import webdriver

    # 메뉴 초기화
    clear_menu(driver)
    time.sleep(0.5)
    
    # 구매유형 클릭
    driver.find_element_by_css_selector(f'input#{sales_type_id}').click()
    time.sleep(0.5)
    
    years = Select(driver.find_element_by_xpath('//*[@id="searchYear"]'))
    years.select_by_value(f'{year}')
    
    # 연령대 클릭
    try: 
        driver.find_element_by_css_selector(f'input#{age_id}').click()
        time.sleep(0.5)
        
    except:
        pass
    
def make_table_df(driver, sales_type, age, year):

    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    import pandas as pd
    
    # 컬럼 데이터 수집
    columns = driver.find_elements_by_css_selector("table.re_table > thead > tr > th")
    columns = [column.text for column in columns] + [ "sales_type", "age", "year"] 

    # 데이터 프레임 만들기
    df = pd.DataFrame(columns=columns)

    # 데이터 프레임 채우기
    rows = driver.find_elements_by_css_selector("table.re_table > tbody > tr")
    for row in rows:
        cells = row.find_elements_by_css_selector('td,th')
        datas = [cell.text for cell in cells] + [sales_type, age, year]     
        df.loc[len(df)] = datas
    
    return df

    
def kaida_model(user_id, user_pass, webdriver_path = "", start_year = 2016, end_year =2022, sales_types = 'all', ages = 'all'):
    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    import time 
    import pandas as pd
    from bs4 import BeautifulSoup
    import configparser

    try : 
        if webdriver_path == "":
            driver = webdriver.Chrome()
        else : 
            driver = webdriver.Chrome(webdriver_path)

        driver.get("https://www.kaida.co.kr/uat/uia/egovLoginUsr.do")
        driver.find_element_by_css_selector('#userId').send_keys(user_id)
        driver.find_element_by_css_selector('#userPass').send_keys(user_pass)
        driver.execute_script('actionLogin()')
        driver.get("https://www.kaida.co.kr/ko/statistics/custom2.do")
        time.sleep(1)

        selector = '#pageBody > article.body_wrap > div > div.select_filter > table > tbody > tr > td:nth-child(8) > div > label'

        #구매유형
        type_select = driver.find_elements_by_css_selector(selector)
        type_select = {st.text: st.get_attribute("for") for st in type_select}

        # 연령
        age_select = driver.find_elements_by_css_selector(".td_Age > .item_wrap > label")
        age_select = {a.text: a.get_attribute("for") for a in age_select}

        if sales_types == 'all':
            sales_types = type_select.keys()
        elif type(sales_types) == str:
            sales_types = [sales_types]

        if ages == 'all':
            ages = age_select.keys()
        elif type(ages) == str : 
            ages = [ages]


        dfs = []

        for year in range(start_year, end_year): #2016, 2022
            for sales_type in sales_types:
                for age in ages:
                    sales_type.replace(" ", "")
                    age.replace(" ", "")

                            # 메뉴 선택
                    select_menu(driver, type_select[sales_type], age_select[age], year)

                            # 검색버튼 클릭
                    driver.find_element_by_css_selector('.searchBtn').click()
                    time.sleep(0.2)

                            # 데이터 수집해서 데이터 프레임으로 만들기
                    try: 
                        df = make_table_df(driver, sales_type, age, year)
                        dfs.append(df)
                    except:
                        pass

                    print([sales_type, age, year])

        # 수집된 데이터 프레임 병합
        result_df = pd.concat(dfs)

        # index 초기화
        result_df.reset_index(drop=True, inplace=True)

        # csv 파일로 저장
        result_df.to_csv(f"result{year}.csv", index=False, encoding='utf-8-sig')
        result_df.to_excel(f"result{year}.xlsx", index=False)

        # 출력
        result_df.tail()
        
    
    
    finally : 
        driver.quit()
        