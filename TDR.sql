SELECT COUNTRY_SHIPPING, TDR, GMV_bDics_OS, GMV_bDics_OS/(1+VAT) 'NMV_bDisc_OS', FC_FROM_DATE, FC_FOR_DATE, VAT,

CASE
	WHEN COUNTRY_SHIPPING ='DE' THEN
		CASE
		WHEN FC_FOR_DATE >= to_date('2020-07-01','yyyy-mm-dd') AND FC_FOR_DATE <= to_date('2020-12-31','yyyy-mm-dd')
		THEN 0.16

		WHEN FC_FOR_DATE <= to_date('2020-07-01','yyyy-mm-dd')
		THEN 0.19

		WHEN FC_FOR_DATE >= to_date('2020-12-31','yyyy-mm-dd')
		THEN 0.19
		END

	WHEN COUNTRY_shipping NOT IN ('DE') THEN
		CASE
		WHEN VAT = VAT THEN VAT
		END
END VAT

FROM (SELECT COUNTRY_SHIPPING,
sum(CPS.ACTUALS.GMV_BEF_CANCELLATION)/sum(CPS.ACTUALS.NMV_BEF_CANCELLATION)-1 VAT
FROM CPS.ACTUALS
GROUP BY COUNTRY_SHIPPING) aa

LEFT JOIN (WITH CC AS (SELECT 1-((1-(m1.RISK_DR+m1.STRATEGIC_DR))*(1-m1.COUPON_DR)) TDR,
m1.GMV_BCANC_SHOP/((1-(m1.RISK_DR+m1.STRATEGIC_DR))*(1-m1.COUPON_DR)) GMV_bDics_OS,
COUNTRY,
FC_FOR_DATE,
FC_FROM_DATE
FROM CPS.CPS_FCWEEKLY_EXTRACTION m1)

SELECT sum(CC.TDR*CC.GMV_bDics_OS)/sum(CC.GMV_bDics_OS) TDR,
CC.COUNTRY,
CC.FC_FOR_DATE,
CC.FC_FROM_DATE,
SUM(CC.GMV_bDics_OS) GMV_bDics_OS
FROM CC
GROUP BY CC.COUNTRY, CC.FC_FOR_DATE, CC.FC_FROM_DATE) ss

ON aa.COUNTRY_SHIPPING=ss.COUNTRY
WHERE TO_DATE(TO_CHAR(FC_From_date),'YYYY-MM-DD') = (SELECT MAX(TO_DATE(TO_CHAR(FC_FROM_DATE),'YYYY-MM-DD')-49-7) FROM CPS.CPS_FCWEEKLY_EXTRACTION)
