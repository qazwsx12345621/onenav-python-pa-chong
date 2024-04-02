import re

# 定义一个函数来提取链接
def extract_links(text):
    #下面替换的时候注意格式例如www.baidu.com则为【www\.baidu\.com】
    pattern = r'<loc>(https://www\.baidu\.com/sites/.*?\.html)</loc>'  # 正则表达式模式匹配具有特定内容的链接
    matches = re.findall(pattern, text)  # 找到所有匹配的链接
    return matches

# 读取URL的内容
url = "https://替换你要采集的域名例如www.baidu.com/sitemap.xml"
import requests
response = requests.get(url)
xml_content = response.text

# 提取链接
links = extract_links(xml_content)

# 将链接写入txt文件
with open("links.txt", "w") as file:
    for link in links:
        file.write(link + "\n")
