"""
链家二手房
"""
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent

class LianjiaSpider:
    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'

    def get_html(self, url):
        for i in range(3):
            try:
                html = requests.get(url=url, headers={'User-Agent':UserAgent().random}, timeout=3).text
                # 直接调用解析函数
                self.parse_html(html)
                break
            except Exception as e:
                print('Retry')

    def parse_html(self, html):
        """解析提取数据"""
        # 1、创建解析对象
        p = etree.HTML(html)
        # 2、基准xpath  li_list: [<element li at xxx>,<element li at xxx>,...,<element li at xx>]
        li_list = p.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        # 3、遍历,依次提取每个房源信息,放到一个字典中
        item = {}
        for li in li_list:
            # 名称 + 地址
            name_list = li.xpath('.//div[@class="positionInfo"]/a[1]/text()')
            item['name'] = name_list[0].strip() if name_list else None
            address_list = li.xpath('.//div[@class="positionInfo"]/a[2]/text()')
            item['address'] = address_list[0].strip() if address_list else None
            # 户型+面积+方位+是否精装+楼层+年代+类型
            # info_list: ['两室一厅 | 78.88 | 南北 | 精装修 | 12层 | 2005 | 板楼']
            info_list = li.xpath('.//div[@class="houseInfo"]/text()')
            if info_list:
                info_list = info_list[0].split('|')
                if len(info_list) == 7:
                    item['model'] = info_list[0].strip()
                    item['area'] = info_list[1].strip()
                    item['direct'] = info_list[2].strip()
                    item['perfect'] = info_list[3].strip()
                    item['floor'] = info_list[4].strip()
                    item['year'] = info_list[5].strip()
                    item['type'] = info_list[6].strip()
                else:
                    item['model']=item['area']=item['direct']=item['perfect']=item['floor']=item['year']=item['type'] = None
            else:
                item['model'] = item['area'] = item['direct'] = item['perfect'] = item['floor'] = item['year'] = item['type'] = None
            # 总价 + 单价
            total_list = p.xpath('.//div[@class="totalPrice"]/span/text()')
            item['total'] = total_list[0].strip() if total_list else None
            unit_list = p.xpath('.//div[@class="unitPrice"]/span/text()')
            item['unit'] = unit_list[0].strip() if unit_list else None

            print(item)

    def run(self):
        for i in range(1,101):
            url = self.url.format(i)
            self.get_html(url)
            time.sleep(random.randint(1,2))

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()

















