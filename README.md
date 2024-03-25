# 自动签到脚本集合

## 项目简介

基于青龙面本的自动签到脚本集

青龙面板仓库地址: [https://github.com/whyour/qinglong](https://github.com/whyour/qinglong)

面板安装

```yaml
version: "3.5"
services:
  ql:
    image: whyour/qinglong
    container_name: ql
    restart: always
    environment:
      - TZ=Asia/Shanghai
    ports:
      - "5701:5700"
    volumes:
      - /home/ql:/ql/data
```

## BurnHair 自动签到

环境变量名: burn、burn1、burn2.....burn99 (最多支持100个帐号)

环境变量值: Cookie

> 示例: session=MTcxMDc1NjAyM3xEWDhFQVFM...

## Epic 免费游戏通知

需设置通知器: 企业微信应用 - 图文卡片

## 日志推送

基于消息头的日志推送

检测所有已启动的任务日志，抓取当天日志消息，根据消息头，选择指定的通知器进行推送，需要配合 **青龙面板应用** 使用

> 青龙面板 - 系统设置 - 应用设置 - 新建应用（需要权限: 定时任务、环境变量、日志管理）

应用环境变量名: `ql_app`

应用环境变量值: `cline_id;client_secret`

> 示例: aaaaaa;bbbbbb

内置通知器:

- 企业微信应用 - 纯文本

  默认消息头: `[企业微信]`

  默认环境变量名: `wecom`

  默认环境变量值: `id;secret;to_user;agent_id`

  > 示例:  ww2xxxxxx;B9kqCehzUU3hPQrzOeUxxxxxx;@all;1000002

  代理变量名(选填): `wecom_proxy`

  > 示例: `http://111.111.111.111:9999`

- 企业微信应用 - 图文卡片

  默认消息头: `[企业微信图片]`

  默认环境变量名: `wecom`

  默认环境变量值: `id;secret;to_user;agent_id`

  > 示例:  ww2xxxxxx;B9kqCehzUU3hPQrzOeUxxxxxx;@all;1000002

- 企业微信机器人

  默认消息头: `[企业微信机器人]`

  默认环境变量名: `wecom_robot_url`

  默认环境变量值: `url` 

  > 示例:  `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxx`

  