# Brian Study Hub - 开发日志

## 2026-02-28
- 完成了：
  - 完整搭建 Brian AS Study Hub 飞书互动学习机器人
  - 三门课程内容生成：Pure Math 1 (8章/41知识点/40题)、Statistics 1 (5章/26知识点/25题)、AS Physics (11章/49知识点/55题)
  - FastAPI 后端 + SQLite 数据库 + Claude API 问答集成
  - 互动消息卡片：主菜单 → 选科 → 选章 → 学习/测试模式
  - 部署到腾讯云广州服务器 (159.75.221.127)
  - Cloudflare Tunnel 解决 HTTPS/ICP 问题
  - 域名：brian.jinglongai.xyz
  - 修复 API URL：open.feishu.cn → open.larksuite.com（国际版 Lark）
  - 推送到 GitHub: macli8666-oss/brian-study

- 待做事项：
  - 让 Brian 下载 Lark（国际版）并注册账号
  - 在 Lark 搜索 Brian Study Hub 机器人进行测试
  - 测试完整交互流程：主菜单 → 选科 → 选章 → 学习/测试
  - 验证 Claude API 问答功能
  - 如需要，增加学习进度报告功能（发送给家长）
  - 确认 Lark 开发者后台的事件订阅和权限配置正确

- 已知问题：
  - 尚未验证消息事件是否正常推送（之前因平台版本不匹配未能测试）
  - 需确认 Lark 开发者后台已正确配置：im.message.receive_v1 事件订阅、im:message 权限

- 关键文件：
  - app/main.py — 主程序，FastAPI 路由和消息/卡片处理
  - app/feishu_client.py — Lark API 客户端
  - app/card_builder.py — 互动卡片构建
  - app/claude_client.py — Claude API 集成
  - app/content_loader.py — 课程内容加载
  - app/config.py — 配置（API URL: open.larksuite.com）
  - content/*.json — 三门课程内容数据
  - .env — 环境变量（App ID/Secret/API Key）

- 平台说明：
  - App 创建在 Lark 国际版 (open.larksuite.com)
  - Brian 需使用 Lark 国际版 app
  - 家长 (Mac) 也在国际版，可建群监控进度
