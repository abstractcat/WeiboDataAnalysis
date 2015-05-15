# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import time
import matplotlib.pyplot as plt
from WeiboDataAnalysis.postgres import PostgresConn
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

def main():
    mid="3817886315883820"
    #hist_repost_delta(mid)
    hist_repost_count(mid)

def hist_repost_delta(mid):
    db = PostgresConn()
    sql="select tm from repost where root_mid='%s' order by tm asc;"%mid
    rows = db.query(sql)
    tm_second=map(lambda x:time.mktime(x[0].timetuple()),rows)

    #change time to suffix from first repost
    tm_second=map(lambda x:x-tm_second[0],tm_second)

    #filter out repost that is too far away
    tm_second=filter(lambda x:x-tm_second[0]<3600*12,tm_second)

    #get delta of successive repost
    tm_delta=[]
    for i in range(1,len(tm_second)):
        tm_delta.append(tm_second[i]-tm_second[i-1])

    #filter out delta time that is too long
    tm_delta=filter(lambda x:x<100,tm_delta)

    #get title of weibo
    sql="select content from weibo where mid='%s';"%mid
    rows=db.query(sql)
    content=rows[0][0]
    content=content.decode('utf-8')[:20]

    fig,(ax1,ax2)=plt.subplots(2, sharex=False)
    bins=[i*1 for i in range(0,100)]
    ax1.hist(tm_delta,bins)
    y=[i+1 for i in range(0,len(tm_second))]
    ax2.plot(tm_second,y,'^-')
    plt.title(content)
    plt.show()

def hist_repost_count(mid):
    db = PostgresConn()
    sql="select uname from repost where root_mid='%s' order by tm asc;"%mid
    rows = db.query(sql)
    names=map(lambda x:x[0],rows)
    dist_names=list(set(names))
    #map from name to int
    name_dict={}
    for i in range(0,len(dist_names)):
        name_dict[dist_names[i]]=i
    names_id=[]
    name_count={}
    for name in names:
        names_id.append(name_dict[name])
        name_count[name]=name_count.get(name,0)+1

    for name in name_count:
        if name_count[name]>1:
            print(name+':'+str(name_count[name]))

    #get title of weibo
    sql="select content from weibo where mid='%s';"%mid
    rows=db.query(sql)
    content=rows[0][0]
    content=content.decode('utf-8')[:20]

    plt.title(content)
    plt.hist(names_id,bins=len(name_dict))
    plt.show()

if __name__ == '__main__':
    main()