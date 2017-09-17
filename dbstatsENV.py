#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#dbstatsENV.py


#检查用到的SQL语句
db_name_sql=''' select NAME db_name,VALUE FROM v$parameter WHERE name LIKE 'db_name' '''
tablespace_sql = '''SELECT a.tablespace_name,
        round(a.total_mb) total_mb, 
        round(a.allocated_mb) allocated_mb,
        nvl(round(a.allocated_mb - b.free_mb),0) used_mb,
        nvl(round(decode(a.total_mb,allocated_mb,b.free_mb,(a.total_mb - a.allocated_mb + b.free_mb))),0) free_mb,
        nvl(round((a.allocated_mb - b.free_mb)/total_mb* 100,2),0) used_redio
from
        (
           SELECT 
                  tablespace_name,
                  nvl(sum(DECODE(f.AUTOEXTENSIBLE,'YES',f.MAXBYTES,'NO',f.BYTES)/1024/1024),0) total_mb ,
                  nvl(sum(f.BYTES)/1024/1024,0) allocated_mb 
           from 
                  dba_data_files f 
           GROUP BY 
                  tablespace_name
         ) a    
left join
        (
           SELECT 
                  tablespace_name,
                  nvl(SUM(bytes)/1024/1024,0) free_mb
           FROM 
                  dba_free_space 
           GROUP BY 
                  tablespace_name
        ) b 
on
        a.tablespace_name = b.tablespace_name
order by used_redio desc'''

warnning_sql  = ''' SELECT substr(REASON,1,100) REASON,
       TO_CHAR(CREATION_TIME, 'yyyy-mm-dd hh24:mi:ss') CREATION_TIME,
       OBJECT_TYPE,
       OBJECT_NAME,
       substr(SUGGESTED_ACTION,1,100) SUGGESTED_ACTION
  FROM DBA_OUTSTANDING_ALERTS
 WHERE CREATION_TIME > SYSDATE - 31
 ORDER BY CREATION_TIME '''

flashback_sql = ''' SELECT nvl(f.name,'NULL') name,
       to_char(round(f.SPACE_LIMIT/1024/1024)) SPACE_LIMIT,
       to_char(round(f.SPACE_USED/1024/1024)) SPACE_USED,
       to_char(round(f.SPACE_RECLAIMABLE/1024/1024)) SPACE_RECLAIMABLE,
       to_char(round(f.NUMBER_OF_FILES/1024/1024)) NUMBER_OF_FILES
  FROM v$recovery_file_dest f '''

instance_sql  = ''' SELECT INST_ID,INSTANCE_NAME, STATUS FROM gv$instance '''
database_sql  = ''' SELECT  INST_ID,NAME, OPEN_MODE FROM gv$database '''
asm_sql       = ''' SELECT NAME, total_mb, round(total_mb-free_mb), ROUND((total_mb-free_mb)/total_mb*100,2)||'%' from v$asm_diskgroup '''
auditinfo_sql = ''' SELECT OWNER, OBJECT_NAME, OBJECT_TYPE FROM DBA_OBJ_AUDIT_OPTS WHERE NOT OBJECT_NAME LIKE 'BIN$%' AND ROWNUM <= 20 '''


#需要检查的数据库信息，在osstatsENV中，数据库检查标记为True的在这些都需要要对应的项
database_dict={ '192.168.1.112':[['cjcl','cjclpassword',              '1521', 'snpcjdb' ]],  
              }

#ip:[[cjcl,password,port,dbname],[[cjcl,password,port,dbname]]

#检查项列表，检查项目名称，检查该项目对应的sql语句，输出的结果是不是数值型的结果
#该列表中的每一项都应该有一个sql语句
db_stat_list=[['DB_name',    db_name_sql,     False],
              ['Tablespace', tablespace_sql , True ],
              ['Instance'  , instance_sql   , False],
              ['Database'  , database_sql   , False],
              ['Warning'  ,  warnning_sql   , False],
              ['FlashBask' , flashback_sql  , False],
              ['AudiInfo'  , auditinfo_sql  , False]

]
