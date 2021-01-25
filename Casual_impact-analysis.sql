SELECT CRM.SK_BELEGDATUM
            , CASE
                  WHEN CRM.SK_BELEGDATUM < 20190101 THEN COUNT(DISTINCT(CRM.SK_CUSTOMER))/353343
                  ELSE COUNT(DISTINCT(CRM.SK_CUSTOMER))/351491
                END POPULATION_SHARE
        FROM ZALANDO_ETL.V_VA_POS_CRM CRM
        INNER JOIN ZALANDO_ETL.V_SHOP_A SHOPS ON CRM.SK_SHOP = SHOPS.SK_SHOP
        INNER JOIN ZALANDO_ETL.V_CUSTOMER_ADDRESS_A CUS
        ON CRM.ZEOS_CUSTOMER_ID = CUS.CUSTOMER_ID
        WHERE SHOPS.SHOPNAME = 'Zalando Shop'
              AND SHOPS.ISO_COUNTRY_CODE = 'CH'
              AND CRM.SK_BELEGDATUM BETWEEN {pre_start} AND {post_end}
              AND (CUS.ZIP LIKE '65%' OR CUS.ZIP LIKE '66%'
              OR CUS.ZIP LIKE '67%'
              OR CUS.ZIP LIKE '68%'
              OR CUS.ZIP LIKE '69%')
        GROUP BY CRM.SK_BELEGDATUM
        ORDER BY CRM.SK_BELEGDATUM

/*  data_test = pd.read_sql_query(sql, con)
    data_test['REGION']='Ticino' */


        SELECT CRM.SK_BELEGDATUM
                , CASE
                      WHEN CRM.SK_BELEGDATUM < 20190101 THEN COUNT(DISTINCT(CRM.SK_CUSTOMER))/8191184
                      ELSE COUNT(DISTINCT(CRM.SK_CUSTOMER))/8254542
                  END POPULATION_SHARE
                FROM ZALANDO_ETL.V_VA_POS_CRM CRM
                INNER JOIN ZALANDO_ETL.V_SHOP_A SHOPS ON CRM.SK_SHOP = SHOPS.SK_SHOP
                INNER JOIN ZALANDO_ETL.V_CUSTOMER_ADDRESS_A CUS
                ON CRM.ZEOS_CUSTOMER_ID = CUS.CUSTOMER_ID
                WHERE SHOPS.SHOPNAME = 'Zalando Shop'
                      AND SHOPS.ISO_COUNTRY_CODE = 'CH'
                      AND CRM.SK_BELEGDATUM BETWEEN {pre_start} AND {post_end}
                      AND CUS.ZIP NOT LIKE '65%' AND CUS.ZIP NOT LIKE '66%' AND CUS.ZIP NOT LIKE '67%'
                      AND CUS.ZIP NOT LIKE '68%' AND CUS.ZIP NOT LIKE '69%'
                GROUP BY CRM.SK_BELEGDATUM
                ORDER BY CRM.SK_BELEGDATUM


/* # prepare causal impact dataframe

df = pd.concat([data_test, data_control]).reset_index(drop='True')
df['SK_BELEGDATUM'] = pd.to_datetime(df['SK_BELEGDATUM'], format="%Y%m%d")
df_p = df.pivot(index='SK_BELEGDATUM', columns='REGION', values='POPULATION_SHARE')
df_p
In [ ]:
#run causal impact
try:
    from causalimpact import CausalImpact
except:
    get_ipython().system('pip install pycausalimpact;')
    from causalimpact import CausalImpact

import pandas as pd
import datetime as dt

pre_start=20180101
test_start=20180701
post_end=20191231

# Set dates
pre_end = (dt.datetime.strptime(str(test_start), '%Y%m%d') + dt.timedelta(days=-1)).strftime('%Y-%m-%d')
pre_start, test_start, post_end = [dt.datetime.strptime(str(d), '%Y%m%d').strftime('%Y-%m-%d') for d in [pre_start, test_start, post_end]]
pre_list = [pre_start, pre_end]
post_list = [test_start, post_end]

# Select only required columns
df_s = df_p.loc[:, [test_region] + [control_regions]]

# Rename variables
values = ['x' + str(i) for i in range(0, len([control_regions]))]
df_s.rename(columns={**{test_region: 'y'}, **dict(zip([control_regions], values))}, inplace=True)

# Do the analysis
ci = CausalImpact(df_s, pre_list, post_list, nseasons=[{'period': 7}])
In [ ]:
ci.summary()

# Prepare a dataframe to store the results in.
cols = ['control_regions'] + ['CUSTOMER_SHARE'+mode for mode in ['abs', 'rel']]
results = pd.DataFrame(index=['Ticino'], columns=cols)

results.at[test_region, 'control_regions'] = control_regions
results.at[test_region, 'CUSTOMER_SHARE'+'abs'] = ci.summary_data.at['abs_effect', 'cumulative']
results.at[test_region, 'CUSTOMER_SHARE'+'rel'] = ci.summary_data.at['rel_effect', 'cumulative']
results


*/
