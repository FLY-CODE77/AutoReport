use mydb;

-- 추가된 자동차 모델 찾기
SELECT
    Distinct c.Product
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
				else concat(Year,"",Month)
			end
		) as YM
		From TV_monthly)  c
        
LEFT OUTER JOIN
	demension_upload b
On (c.Product = b.model_pk)

WHERE b.Model IS NULL
;


SELECT
  count(MyUnknownColumn)
FROM
  demension_upload
;



-- Null 값 추가하기/2번 적용되지 않게 주의
 INSERT INTO demension_upload
 (MyUnknownColumn, model_pk, Model, Brand, car_country, car_fuel, car_seg, car_seg_size, car_seg_com)
 VALUES(1169,"아우디RS이트론GT", "e-tron", "Audi", "독일", "전기", "준대형", "SUV", "mobility_e")
;
INSERT INTO demension_upload
(MyUnknownColumn, model_pk, Model, Brand, car_country, car_fuel, car_seg, car_seg_size, car_seg_com)
VALUES(1170,"한국토요타렉서스LC500컨버터블", "LC", "Lexus", "일본", "하이브리드", "스포츠", "스포츠", "performance_sa")
;

-- 추가되었는지 확인하기
SELECT
	*
FROM
	demension_upload
WHERE Model_pk = '아우디RS이트론GT'
;



