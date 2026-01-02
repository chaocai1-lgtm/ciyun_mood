# 🎬 实时弹幕词云系统 (Node.js 版本)

基于 WebSocket 的实时弹幕词云，无刷新、无闪烁！

## ✨ 特点

- 🚀 **真正实时** - WebSocket 即时推送，发送后所有人立刻看到
- 💫 **无闪烁** - 不需要刷新页面，体验流畅
- 📱 **响应式设计** - 完美支持手机端
- 🔗 **共享数据库** - 与 Streamlit 版本共用 Neo4j 数据库

## 🚀 本地运行

```bash
# 进入目录
cd nodejs版本

# 安装依赖
npm install

# 启动服务
npm start
```

然后访问 http://localhost:3000

## 📱 手机访问

1. 电脑和手机连接同一个 WiFi
2. 查看电脑的局域网 IP（如 192.168.1.100）
3. 手机浏览器访问 http://192.168.1.100:3000

## ☁️ 部署到云端

### 方案1: Render (推荐，免费)

1. 将代码推送到 GitHub
2. 访问 https://render.com
3. 新建 Web Service，连接你的仓库
4. 选择 `nodejs版本` 目录
5. 自动部署完成！

### 方案2: Railway

1. 访问 https://railway.app
2. 从 GitHub 导入项目
3. 自动部署

### 方案3: Vercel

需要改造成 Serverless 架构，WebSocket 需要额外配置。

## 🔧 配置说明

在 `server.js` 中修改：

```javascript
const NEO4J_URI = "你的Neo4j地址";
const NEO4J_USER = "用户名";
const NEO4J_PASSWORD = "密码";
const TARGET_LABEL = "数据标签";
const ADMIN_PASSWORD = "管理员密码";
```

## 📂 文件结构

```
nodejs版本/
├── server.js          # 后端服务
├── public/
│   └── index.html     # 前端页面
├── package.json       # 依赖配置
└── README.md          # 说明文档
```

## 🎯 与 Streamlit 版本的区别

| 特性 | Streamlit | Node.js |
|------|-----------|---------|
| 实时性 | 轮询刷新 | WebSocket 即时 |
| 页面闪烁 | 有 | 无 |
| 并发支持 | 一般 | 优秀 |
| 部署难度 | 简单 | 中等 |
