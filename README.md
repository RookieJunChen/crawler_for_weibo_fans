# README

### 简介

  本项目通过*selenium*库爬取指定微博用户的关注、粉丝相关数据（昵称、性别、简介、地域、年龄、星座、学校、公司）。

  需要注意的是，新浪微博网页版(https://weibo.com) 的查看粉丝存在数目限制（最多5页），因此在这里我们通过https://weibo.cn， 来爬取更多的粉丝数据。



### Pipeline

1. *python get_cookie.py*，而后在浏览器上登录，获取相关cookie信息，使得我们之后爬取信息时候可以自动登录
2. 在selenium_crawler.py中填写需要搜索的用户名称后，*python selenium_crawler.py*

