use mydb;

SELECT
	a.year
    , a.month
    , a.YM
    , b.Brand
    , b.Model
    , a.Target_Audience
    , concat(a.YM,"-",b.Model,"-",a.Target_Audience) as Ad_id
    , sum(value) as count_reg
 FROM
	(SELECT
		year
		, month
		,(CASE
			WHEN Month = "6" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )
			WHEN Month = "5" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )
			WHEN Month = "4" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )       
			WHEN Month = "3" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )        
			WHEN Month = "2" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )        
			WHEN Month = "1" THEN substring(concat(Year,"0",Month,"월"), 3, 5 )        
			ELSE substring(concat(Year,"",Month,"월"),3,5)     
			END   
		) As YM
		, brand
		, model
		,(CASE
			WHEN sales_type = "개인-남자" AND age ="20~29" THEN "남20대"
			WHEN sales_type = "개인-남자" AND age ="30~39" THEN "남30대"
			WHEN sales_type = "개인-남자" AND age ="40~49" THEN "남40대"
			WHEN sales_type = "개인-남자" AND age ="50~59" THEN "남50대"
			WHEN sales_type = "개인-남자" AND age ="60~69"  THEN "남60대이상"
			WHEN sales_type = "개인-남자" AND age ="70~"  THEN "남60대이상"
			WHEN sales_type = "개인-여자" AND age ="20~29" THEN "여20대"
			WHEN sales_type = "개인-여자" AND age ="30~39" THEN "여30대"
			WHEN sales_type = "개인-여자" AND age ="40~49" THEN "여40대"
			WHEN sales_type = "개인-여자" AND age ="50~59" THEN "여50대"
			WHEN sales_type = "개인-여자" AND age ="60~69"  THEN "여60대이상"
			WHEN sales_type = "개인-여자" AND age ="70~"  THEN "여60대이상"           
			ELSE "delete row"
		END
		) As Target_Audience	
		, value
	 FROM kaida) a
LEFT OUTER JOIN
  demension_upload b
On (a.model = b.model_pk)
GROUP BY a.year, a.month, a.YM, b.Brand, b.Model, a.Target_Audience, Ad_id
;