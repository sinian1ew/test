import  requests       #网络请求模块
from lxml import etree    #数据解析模块

#请求头信息
headers={
        'cookie':'ll="118196";'
                ' ''bid=VbEKmQc29vY; ap_v=0,6.0; _pk_id.100001.4cf6=b42b2c7985240f2a.1735625253.;'
                 ' _vwo_uuid_v2=D173B16DFFE6ECFDFBF16D96BA9EF022E|620da59cd7f7097012bbd58a5704badf; '
                'dbcl2="285690245:aBhtHC5CTKk"; ck=pRPx; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1735630934%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D;'
                ' _pk_ses.100001.4cf6=1; __utma=30149280.1492728375.1735625253.1735625253.1735630934.2; '
                '__utmb=30149280.0.10.1735630934; __utmc=30149280;'
                ' __utmz=30149280.1735630934.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
                '__utma=223695111.438571213.1735625253.1735625253.1735630934.2; __utmb=223695111.0.10.1735630934; '
                '__utmc=223695111; __utmz=223695111.1735630934.2.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; '
                 'push_doumail_num=0',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}
#功能函数，去列表第一个元素
def get_first_text(list):
    try:
        return list[0].strip()    #返回第一个字符串，除去两端的空格
    except:
        return ""    #返回空字符串
import pandas as pd
df=pd.DataFrame(columns=["序号","标题","英文标题","链接","导演","评分","评价人数","简介","国家"])   #储存
#使用列表生成式表示十个列表
urls=['https://movie.douban.com/top250?start={}&filter='.format(str(i*20)) for i in range(10)]
count=1     #计算次数
for url in urls:
    res = requests.get(url=url, headers=headers)   #发起请求
    res.encoding='utf-8'
    html = etree.HTML(res.text)   #将返回文本加工为可以解析的html
    lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')    #获取每个电影的li元素
#解析数据
    for li in lis :
        title=get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))  #序号
        titles=get_first_text(li.xpath('./div/div[2]/div[1]/a/span[2]/text()'))   #标签
        src=get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))#s链接
        dictor=get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))#导演
        score=get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))#评分
        comment=get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))#评分人数
        summary=get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))#简介
        country = get_first_text(li.xpath('//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()[2]')).split('/')[-2].strip()
        print(count,title,titles,src,dictor,score,comment,summary,country)
        df.loc[len(df.index)] = [count,title,titles,src,dictor,score,comment,summary,country]#将内容赋值到新行中
        count +=1
df.to_excel('douban_top250_movies.xlsx',na_rep='')
        #df.to_excel('douban_top250_movies.xlsx', index=False)#保存csv文件
