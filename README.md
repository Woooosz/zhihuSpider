## 知乎爬虫

此知乎爬虫可以拿到知乎的用户信息,与其他版本的知乎爬虫相比.该爬虫的主要特性有:

<div align = "center">
<img src="http://p17p5mbqh.bkt.clouddn.com/17-12-19/30325139.jpg" width = "400"/>
</div>

### 支持二维码扫码登录

目前知乎的验证码更新提交倒立字的二维坐标,传统的下载验证码图片手段已经不能使用.与此同时，其他知乎爬虫的版本需要用户自行将cookie字段手工写到数据库，
对于一些没有数据库及http协议基础的用户来说较为困难。本项目支持手机扫码一键登录拿cookie，用户友好。

<div align = "center">
<img src="http://p17p5mbqh.bkt.clouddn.com/17-12-19/15257442.jpg" width = "300"/>
</div>

注意！ 根据知乎的规定，cookie有效期为30天。也就是说，**您30天后需要重新登录到您的服务器，扫码二维码.**

### 支持分布式

本项目使用了redis-scrapy组件，重新设计了中间件。将cookie池放在了redis上，实现了分布式部署。具体的推荐架构如下：
如果使用单机模式，在配置完基本环境后。可运行zhihu爬虫

```
scrapy crawl zhihu
```

如果你选择运行在集群模式，项目目前的架构设计如下：
<div align = "center">
<img src="http://p17p5mbqh.bkt.clouddn.com/17-12-19/63592231.jpg" width = "500"/>
</div>

你可以在master中运行get\_info将内容写到数据库, 在slave中运行get\_request爬虫

```
# Run in master
scrapy crawl get_info
# Run in slave
scfapy crawl get_request
```
然而这种架构目前并不完美，根据我的发现目前的性能瓶颈在get\_info,后续的版本中可能会将get\_request模块放到master中,而把get\_info放到slave中运行.

## 安装 & 使用

### 安装环境
```
git clone https://github.com/Woooosz/zhihuSpider
cd zhihuSpider
pip install -r requirements.txt
```
### 导入表信息

```SQL
createdatabase zhihu;
use zhihu;
source database.txt;
```
### 修改settngs信息
修改数据库信息以及redis服务器信息

## 技术栈
* scrapy
* scrapy-redis
* requests
* redis
* mysql

## 其他
无

## License
  MIT




