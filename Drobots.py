#coding:utf-8
'''
code by Stu.
公众号：安全黑板报
'''
import requests
import json,re
import feedparser
from bs4 import BeautifulSoup
import time


webhook= 'https://oapi.dingtalk.com/robot/send?access_token=' # webhook可以在丁丁机器人里找到
headers ={"Content-Type": "application/json"}
#给机器人添加图片
links = [
            {
    "title": "安全黑板报每日推送",
    "messageURL": "https://mp.weixin.qq.com/mp/homepage?__biz=MzI5NTg2ODA2NA==&hid=1&sn=b7ef2bafcdb8660ffbcd67e2e70a1674",
    "picURL":"https://mmbiz.qpic.cn/mmbiz_jpg/zibib0z20iaTOWvh1ttjr93Qh47MEq7KMao0bJMyOExEpHt4Mvz7qYxR12L7mQbCZMv3r4XwyAGiasnDwic3BrdBEaA/0?wx_fmt=jpeg"
        }
    ]
linkss = []


# 取出sec-wike rss的 href 和 string，添加到links中
def secwiki():
    try:
        secwiki= "https://www.sec-wiki.com/news/rss"
        rs1 = feedparser.parse(secwiki)
        html = rs1.entries[0]["summary_detail"]["value"]
        soup = BeautifulSoup(html, 'html.parser')
        for k in soup.find_all('a'):
            link1 = {"title": k.string,"messageURL": k['href']}
            linkss.append(link1)
        linkss.pop(-1)#删除最后一条sec-wiki的href
        return "ok"
    except :
        return "secwiki is no ok"

#52bug 爬取一页
def bug52():
    try:
        bug52_url ="http://www.52bug.cn/sec"
        link2_url = requests.get(bug52_url).text
        reg_url = r'<a href="(.*?)html" title="'
        reg_tit = r'<a href=".*?html" title="(.*?)"'
        pattern= re.compile(reg_url)
        tags_url= re.findall(pattern, link2_url)

        pattern= re.compile(reg_tit)
        tags_tit= re.findall(pattern, link2_url)
        for x in range(len(tags_url)):
            link2 = {"title": tags_tit[x],"messageURL": tags_url[x]+"html"}
            linkss.append(link2)
        return "ok"
    except :
        return "bug52 is no ok"

#wikiinio
def wikiinio():
    try:
        url ="http://wiki.ioin.in/"
        link3_url = requests.get(url).text
        reg_url = r'<a href="(.*?)" class="visit-color"'
        reg_tit = r'visit-color" target="_blank">(.*?)</a>'
        pattern= re.compile(reg_url)
        tags_url= re.findall(pattern, link3_url)
        pattern= re.compile(reg_tit,re.DOTALL)#re.DOTALL,可以让正则表达式中的点（.）匹配包括换行符在内的任意字符。
        tags_tit= re.findall(pattern, link3_url)
        for x in range(len(tags_url)):
            link2 = {"title": tags_tit[x].strip(),"messageURL": "http://wiki.ioin.in"+tags_url[x]}
            linkss.append(link2)
        return "ok"
    except :
        return "wikiinio is no ok"

#freebuf 源
def freebuf():
    try:
        freebuf= "https://www.freebuf.com/feed"
        rs1 = feedparser.parse(freebuf)
        l = len(rs1.entries)
        for buf in range(l):
            try:
                url_f = rs1.entries[buf]["link"]
                title_f = rs1.entries[buf]["title_detail"]["value"]
                link4 = {"title": title_f,"messageURL": url_f}
                linkss.append(link4)
            except:
                break
        return "ok"
    except :
        return "freebuf is no ok"

#robots出现错误情况
def error_robots():
    body = {
        "msgtype": "text", 
        "text": {
            "content": "安全黑板报推送出现错误！"
        } 
    }
    message =requests.post(url=webhook, data=json.dumps(body), headers=headers)
#     print u"robots 出现错误！"

#推送完成节点
def ntime(ntime1):
    body = {
        "msgtype": "text", 
        "text": {"content": "%s安全黑板报机器人推送完成" % ntime1} 
    }
    message =requests.post(url=webhook, data=json.dumps(body), headers=headers)
#     print u"推送完成"


#推送操作
def send_mes(freecards):
    body = {
        "feedCard": {
            "links": freecards
        }, 
        "msgtype": "feedCard",
        "at": {
            "atMobiles": [""], 
            "isAtAll": True
        }
    }
    try:
        message =requests.post(url=webhook, data=json.dumps(body), headers=headers)
#         if json.loads(message.text)["errmsg"] == "ok":
#             print u"安全黑板报机器人推送开始！"
#         else:
#             print json.loads(message.text)["errmsg"]
    except:
        error_robots()

if __name__ == '__main__':
    if secwiki() == 'ok' and bug52() == 'ok' and wikiinio() == 'ok' and freebuf() == 'ok':
        num = len(linkss)
        x = 0
        for xx in range((num // 9) +1):
            send_mes(links+linkss[0+x:9+x])
            x+=9
        ntime1 = (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        ntime(ntime1)
    else:
        error_robots()
