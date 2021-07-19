use mydb;

-- 광고주별 ROW의 개수
SELECT
 COALESCE(Advertiser, 'Total Count') as Advertiser
 , count(Advertiser)
 FROM
	TV_monthly
GROUP BY Advertiser WITH ROLLUP
;

-- 연도, 월별 ROW의 개수
SELECT
 COALESCE(Year, 'Total') as Year
 , COALESCE(Month, 'Year Sum') as Month
 , count(Advertiser)
 FROM
	TV_monthly
GROUP BY Year, Month WITH ROLLUP
;

-- TV monthly 테이블정리 YM컬럼, 브랜드, 모델 , UITV_dailyD추가
SELECT
    c.*
	,b.Brand
    ,b.Model	
    ,concat(c.YM,"-",b.Model,"-",c.Target_Audience) as Ad_id
 FROM
	(SELECT
		*
		, (case
				when Month = "6월" THEN substring(concat(Year,"0",Month), 3, 5 )
				when Month = "5월" THEN substring(concat(Year,"0",Month), 3, 5 )
				when Month = "4월" THEN substring(concat(Year,"0",Month), 3, 5 )       
				when Month = "3월" THEN substring(concat(Year,"0",Month), 3, 5 )        
				when Month = "2월" THEN substring(concat(Year,"0",Month), 3, 5 )        
				when Month = "1월" THEN substring(concat(Year,"0",Month), 3, 5 )        
				else substring(concat(Year,"",Month),3,5)
			end
		) as YM
		From TV_monthly)  c
        
LEFT OUTER JOIN
	demension_upload b
On (c.Product = b.model_pk)
;