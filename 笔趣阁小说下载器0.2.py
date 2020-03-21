## 笔趣阁小说下载器
## 在网址中找到XX_XXX的书籍id（例如http://www.paoshu8.com/138_138049/中的138_138049/）
## 在book_id中输入找到的书籍ID
import re
import requests
book_id = input('请输入小说"XX_XXX"的ID:'+"\n")
ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
url0 = 'http://www.paoshu8.com/'+ book_id +'/'
rst0 = requests.get(url0,headers=ua).text   #抓取目录页内容
book_name = re.compile('<h1>(.*?)</h1>',re.S).findall(rst0)[0]  #获取小说名称
unit_url = re.compile('<dd><a href="/.*?/(\d{4,9}).html">',re.S).findall(rst0)  #获取章节页面编号
file_down = open( '《'+ book_name + '》.txt', 'a+', encoding='utf-8') # 创建和标题同名的文件
file_down.write('《'+book_name+'》')  # 写入书名
print('开始下载：《' + book_name+'》一共有'+ str(len(unit_url)) +'章')
for i in unit_url:
    book_unit_url = url0 + i + '.html'      #完成章节网址拼接
    rst1 = requests.get(book_unit_url, headers=ua).text     # 抓取章节页内容
    title = re.compile('<h1>(.*?)</h1>',re.S).findall(rst1)[0]      # 获取文章标题
    file_down.write('\r\n-----' + title + '-----\r\n')      # 写入标题
    content = re.compile('<div id="content">(.*?)</div>',re.S).findall(rst1)        # 获取文章内容
    for sentence in content:
        sentence1 = (re.compile('<p>\u3000\u3000(.*?)</p>').findall(sentence))
        for sentence2 in sentence1:
            file_down.write(sentence2 + '\r\n')     # 写入正文
    print('正在下载：' + title)
print('《' + book_name +'》下载完成,一共有'+ str(len(unit_url)) +'章')
##优化写入文章正则
##加入搜索下载功能