use mydb;

-- 광고주별 ROW의 개수
SELECT
 COALESCE(Advertiser, 'Total Count') as Advertiser
 , count(Advertiser)
 FROM
	TV_daily
GROUP BY Advertiser WITH ROLLUP
;


-- 연도, 월별 ROW의 개수
SELECT
 COALESCE(Year, 'Total') as Year
 , COALESCE(Month, 'Year Sum') as Month
 , count(MyUnknownColumn)
 FROM
	TV_daily
GROUP BY Year, Month WITH ROLLUP
;


-- TV_daily로 연원브랜드별 GRPs 요약 - YM컬럼, 브랜드, 모델  추가
SELECT
	a.Year
    ,a.Month
    ,a.YM
    ,b.Brand
    ,b.Model
    ,a.Target_Audience
    ,concat(a.YM,"-",b.Model,"-",a.Target_Audience) as Ad_id
    ,a.SPOT
    ,a.Audience
    ,a.eqGRPs
    ,a.GRPs
FROM
 (SELECT
	(case
			when Month = "6월" THEN substring(concat(Year,"0",Month), 3, 5 )
			when Month = "5월" THEN substring(concat(Year,"0",Month), 3, 5 )
			when Month = "4월" THEN substring(concat(Year,"0",Month), 3, 5 )       
			when Month = "3월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			when Month = "2월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			when Month = "1월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			else concat(Year,"",Month)
	 end
	) As YM
    ,Year
    ,Month
	, Product
	, Target_Audience
	, concat(Year,"-",Month,"-",Product,"-",Target_Audience) as UID
	, floor(sum(SPOT)) as SPOT
	, format(sum(Adience), 0) as Audience
	, round(sum(eqGRP)*100,1) as eqGRPs
	, round(sum(GRP), 1) as GRPs
	From TV_daily
	GROUP BY YM,Year,Month, Product, Target_Audience, UID) a
LEFT OUTER JOIN
  demension_upload b
On (a.Product = b.model_pk)
;



SELECT
	a.Year
    ,a.Month
    ,a.YM
    ,b.Brand
    ,b.Model
    ,a.Target_Audience
    ,concat(a.YM,"-",b.Model,"-",a.Target_Audience) as Ad_id
    ,a.SPOT
    ,a.Audience
    ,a.eqGRPs
    ,a.GRPs
FROM
 (SELECT
	(case
			when Month = "6월" THEN substring(concat(Year,"0",Month), 3, 5 )
			when Month = "5월" THEN substring(concat(Year,"0",Month), 3, 5 )
			when Month = "4월" THEN substring(concat(Year,"0",Month), 3, 5 )       
			when Month = "3월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			when Month = "2월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			when Month = "1월" THEN substring(concat(Year,"0",Month), 3, 5 )        
			else substring(concat(Year,"",Month),3,5)
	 end
	) As YM
    ,Year
    ,Month
	, Product
	, Target_Audience
	, concat(Year,"-",Month,"-",Product,"-",Target_Audience) as UID
	, floor(sum(SPOT)) as SPOT
	, format(sum(Adience), 0) as Audience
	, round(sum(eqGRP)*100,1) as eqGRPs
	, round(sum(GRP), 1) as GRPs
	From TV_daily
	GROUP BY YM,Year,Month, Product, Target_Audience, UID) a
LEFT OUTER JOIN
  demension_upload b
On (a.Product = b.model_pk)
;

