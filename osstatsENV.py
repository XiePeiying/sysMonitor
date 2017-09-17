#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#statsENV


"""
host[0]: 用户名
host[1]: 系统密码
host[2]: 操作系统类型，1.linux; 2.AIX
host[3]: 系统描述
host[4]: 是否需要对数据库进行检查
host[5]: 系统ip地址（如果有多台的话，可以对多台进行检查）
"""

host_list=[#用户名， 密码，操作系统类型(1.linux|aix),系统描述信息，是否对数据库进行检查，ip地址(当有多台机器的时候，写多台机器) 
           #['oracle','oracle123',           '1', '测试主机',     True, ['192.168.1.112']],
           #['oracle','oracle123',           '1', '测试主机',     False, ['192.168.1.112']],
           #['oracle','oracle123',           '1', '测试主机',     True, ['192.168.1.112']],
           #['oracle','ORA!@#123',           '1', '北京市',      True, ['10.11.250.75','10.11.250.76']]
           
          ]  

"""
检查项列表：
分为linux和aix两部分，两者的区别仅仅是命令的格式稍有不同，该列表是一个多维数组
[[检查项名称]
 [检查需要用到的命令]
 [检查输出结果中各项的的名称(该部分的条目数和检查命令输入的结果条目数相同)]]
如：
    [ 
      [ 'filesystem', 名称
        '''df -Pm|grep -v Filesystem|grep -v "-"|awk {'print $6,$2,$3,$5'}''', 检查用到的命令，生成4个结果
        ['mount_point','total','used','used_ratio']    对生成的结果进行命令，要求一一对应
      ]
    ]

"""


os_stat_list_linux=[['filesystem','''df -Pm|grep -v Filesystem|grep -v "-"|awk {'print $6,$2,$3,$5'}''',['mount_point','total','used','used_ratio']],
              ['CPU', '''vmstat 1 1|tail -1|awk {'print "CPU",$15,$14,$13,$13+$14'}''',['CPU','cpu_idle','cpu_system','cpu_user','cpu_used_ratio']],
              ['MEM', '''free -m|grep Mem|awk '{printf("%s %s %s %s %s", "MEM",$2,$3-$6-$7,$4+$6+$7,($3-$6-$7)/$2*100)}' ''',['MEM','mem_total_mb','mem_used_mb','mem_free_mb','mem_used_ratio']]
             ]

os_stat_list_aix=[['filesystem','''df -Pm|grep -v Filesystem|grep -v "-"|awk {'print $6,$2,$3,$5'}''',['mount_point','total','used','used_ratio']],
              ['CPU', ''' vmstat 1 1|tail -1|awk {'print "CPU",$16,$15,$14,$14+$15'}''',['CPU','cpu_idle','cpu_system','cpu_user','cpu_used_ratio']],
              ['MEM', '''svmon -Gi 1 1|grep memory|awk '{printf("%s %s %s %.0f %s","MEM",$2*4/1024,$3*4/1024, $4*4/1024,$3/$2*100)}' ''',['MEM','mem_total_mb','mem_used_mb','mem_free_mb','mem_used_ratio']]
             ]
