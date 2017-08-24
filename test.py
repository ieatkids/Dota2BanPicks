import requests
from lxml import etree


url = 'http://www.meijutt.com/'

html = requests.get(url)

select = etree.HTML(html.text)

contents = select.xpath('//div[@class="l week-hot layout-box "]')




























