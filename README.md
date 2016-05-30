#LoveqSpider

> A WebSpider of www.loveq.cn

#Intro
LoveqSpider is a WebSpider to saving Programme's downloadURL of www.loveq.cn.
And the Spider will dump the JSON file.


![gif][1]

#How to use

 - Step One

Set the begin page and end page. 
```python
......
#传入起止页码，在此传入了1,71,表示抓取第1到71页的节目
spider = Spider()
spider.savePagesInfo(1,71)
......
```
 - Step Two

Set the begin year and end year.
```python
......
#设置年份,3代表2003年,16代表16年
for i in range(3,16):
    year = ''
.......
```
 - Step Three

Run!

#License
MIT

[1]: http://ww1.sinaimg.cn/mw1024/5e999b55gw1f48xhpl4ang20kx0hvnil.gif
