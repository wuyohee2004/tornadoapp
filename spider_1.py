#coding=utf-8

import urllib
import json

from bs4 import BeautifulSoup as bs



# html = urllib.urlopen('http://search.jd.com/Search?keyword=%E7%94%B7%E9%9E%8B&enc=utf-8#keyword=%E7%94%B7%E9%9E%8B&enc=utf-8&qrst=UNEXPAND&qk=title_key%2C%2C%E7%94%B7%E9%9E%8B&rt=1&stop=1&sttr=1&cid2=11730&click=2-11730&psort=&page=2').read()
# print html
# # content = html.decode('gbk')
# t = open('temp.html','w')
# t.write(html)
# t.close()

# JD Search Url:
# 'http://search.jd.com/Search?keyword=%E7%94%B7%E9%9E%8B&enc=utf-8&rt=1&page=2'

# JD JSON:
# http://p.3.cn/prices/mgets?skuids=J_860275,J_1168467,J_1102758,J_1096008,J_833315,J_1074152,J_1266675,J_1074153,J_1062989,J_1229308,J_1082433,J_1102752,J_1134530,J_1102727,J_1242910,J_1257557,J_1074151,J_1134535,J_1084906755,J_1096007,J_1183079,J_1102755,J_1102764,J_1063013,J_1266674,J_1074894,J_1435902426,J_1378682319,J_1093367,J_1133172534&area=2_2811_0_0&type=1&callback=jsonp1424075501802&_=1424075501981

# JD list in:
# <div class="m psearch prebuy plist-n7 no-preview gl-type-6" id="plist">
#   <ul class="list-h clearfix" tpl="1">
#       <li sku="860275">
        # <div class="lh-wrap">
        #   <div class="p-img">
        #       <a target="_blank" href="http://item.jd.com/1459465605.html" onclick="searchlog(1,1459465605,0,2,'','')">
        #           <img width="220" height="220" data-img="1" src="http://img10.360buyimg.com/n7/jfs/t757/166/716382293/302509/8661b643/54d2e8c0N37b54d3f.jpg" class="err-product">
        #       </a>

def get_content_from_jd(keyword,page=1):
    url = 'http://search.jd.com/Search?'
    params = {'keyword':keyword,'page':page,'rt':1,'enc':'utf-8'}
    data = urllib.urlencode(params)
    r = urllib.urlopen(url+data)
    content = r.read()
    r.close()
    return content

# print get_content_from_jd("3d电视")

#*ids = (可迭代)
def get_price_from_ds(*ids):
    url = 'http://p.3.cn/prices/mgets?'
    params = {'skuids':','.join(['J_%s'%id for id in ids]),'type':1}
    data = urllib.urlencode(params)
    opener = urllib.urlopen(url + data)
    response = opener.read()
    opener.close()
    return json.loads(response)


def get_res_from_jd(keyword,page=1):
    #返回一个{id:xx,price:xx,detail:xx,title:xx}
    pass

if __name__ == "__main__":

    content = get_content_from_jd(keyword="纸尿裤",page=4)
    soup = bs(content)
    mids = soup.find_all(sku=True)
    # print mids[0],"\n","+"*200,"\n",mids[1]
    ids = [mid['sku'] for mid in mids]
    # print ids
    prices = get_price_from_ds(*ids)
    # print prices
    res = []
    for mid in mids:
        data = {}
        data['id'] = mid['sku']
        data['img'] = mid.find('img')['data-lazyload']
        aobj = mid.find(class_ = 'p-name').find('a')
        data['url'] = aobj['href']
        data['title'] = aobj.text.strip()
        data['price'] = filter(lambda price:price['id']=='J_%s'%data['id'],prices)[0]['p']
        data['ori_price'] = filter(lambda price:price['id']=='J_%s'%data['id'],prices)[0]['m']
        res.append(data)

    # print(res)
    for prod in res:
        print prod['title']
        print prod['id']
        print prod['price']
        print prod['ori_price']
        print prod['img']