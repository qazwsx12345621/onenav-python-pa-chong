import os
import requests
from lxml import etree
from openpyxl import Workbook

# 读取链接文本文件
file_name = "links.txt"
with open(file_name, "r") as file:
    links = file.read().splitlines()

# 创建Excel表格
workbook = Workbook()
worksheet = workbook.active

# 写入表头
worksheet.append(["标题", "分类", "简介", "标签", "链接", "描述"])

# 访问每个链接并提取特定内容
total_links = len(links)  # 总链接数
processed_links = 0  # 已处理的链接数
failed_links = []  # 处理失败的链接
successful_links = []  # 处理成功的链接

for link in links:
    processed_links += 1

    try:
        response = requests.get(link)
        html_content = response.text

        # 使用lxml解析html内容
        tree = etree.HTML(html_content)

        # 提取标题
        title = tree.xpath('//h1[@class="site-name h3 my-3"]/text()')
        if not title:  # 检查是否存在标题
            failed_links.append(link)
            continue

        # 提取分类
        classify = tree.xpath("//i[contains(@class, 'iconfont icon-arrow-r-m custom-piece_c')]/following-sibling::a[contains(@class, 'btn-cat')]/text()")

        # 提取简介
        synopsis = tree.xpath('//div[@class="mt-2"]/p[@class="mb-2"]/text()')

        # 提取标签
        label = tree.xpath('//div[@class="mt-2"]/span[@class="mr-2"]/a/text()')

        # 提取链接
        url = tree.xpath('//span[@class="site-go-url"]//a/@href')

        # 提取描述
        description = tree.xpath('//div[@class="panel-body single my-4 "]//text()')

        row_data = [title[0] if title else "", ', '.join(classify).replace(" ", ""), synopsis[0] if synopsis else "", ', '.join(label).replace(" ", ""), url[0] if url else "", ', '.join(description).replace(" ", "")]
        worksheet.append(row_data)

        successful_links.append(link)

        # 输出处理进度信息
        print(f"已处理 {processed_links}/{total_links} 条数据")

    except Exception as e:
        failed_links.append(link)
        print(f"访问链接失败：{link}")
        print(str(e))
        continue

# 保存Excel表格
workbook.save("extracted_data[].xlsx")

# 输出处理结果
print("处理完成！")
print(f"成功处理 {len(successful_links)}/{processed_links} 条数据")
print(f"处理失败 {len(failed_links)}/{processed_links} 条数据")

# 检查并创建处理成功和处理失败的链接文本文件
if not os.path.isfile("successful_links.txt"):
    with open("successful_links.txt", "w"):
        pass

if not os.path.isfile("failed_links.txt"):
    with open("failed_links.txt", "w"):
        pass

# 将处理成功和处理失败的链接保存到文本文件
with open("successful_links.txt", "w") as file:
    for link in successful_links:
        file.write(link + "\n")

with open("failed_links.txt", "w") as file:
    for link in failed_links:
        file.write(link + "\n")
