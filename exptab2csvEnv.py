#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#exptab2csvENV.py


db_info_dict={
         'username'    :'cjcl',
         'password'    :'bXuVNCnSdkf8',
         'hostname'    :'10.6.135.237',
         'servicename' :'thtf',
         'port'        :'1521'
         }


"""
table_info_list = [[tableowner,table_name,导出条件],[]]
如:[["C2017_000000_201_1_1","where bgq = '201701MM'"],[]]
table_info_list_bgq[i][0]: tableowner
table_info_list_bgq[i][1]: tablename
table_info_list_bgq[i][2]: query
"""
table_info_list_query=[
    ['scott','emp', ''],
    ['scott','DEPT',''],
    ['scott','csv_test02',''],
    ['scott','csv_test03','']
]


"""
table_info_list = [[tableowner,table_name,[BGQ]],[]]
如:[["C2017_000000_201_1_1",['201702MM','201703MM'],[]]
table_info_list_bgq[i][0]: tableowner
table_info_list_bgq[i][1]: tablename
table_info_list_bgq[i][3]: 要导出的报告期列表['201701MM','201702MM','201703MM']
"""
table_info_list_bgq=[
    ['CJCL','c2017_000000_201_1_1', ['201702MM','201703MM','201704MM']],
    ['CJCL','c2017_000000_X204_1_11', ['201702MM','201703MM','201704MM','201705MM','201706MM','201707MM','201708MM']],
    ['CJCL','c2017_000000_X204_1_12', ['201702MM','201703MM','201704MM','201705MM','201706MM','201707MM','201708MM']]
]