# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import time
import matplotlib.pyplot as plt
from WeiboDataAnalysis.postgres import PostgresConn

def main():
    mid="3824377479537361"
    hist_repost_delta(mid)

def hist_repost_delta(mid):
    sql="select tm from repost where root_mid='%s' order by tm asc;"%mid
    db = PostgresConn()
    rows = db.query(sql)
    tm_second=map(lambda x:time.mktime(x[0].timetuple()),rows)
    tm_delta=[]
    for i in range(1,len(tm_second)):
        tm_delta.append(tm_second[i]-tm_second[i-1])

    plt.hist(tm_delta,bins=100)
    plt.show()

if __name__ == '__main__':
    main()