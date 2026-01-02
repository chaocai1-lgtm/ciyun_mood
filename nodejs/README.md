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

### 🤖 AI 功能配置 (DeepSeek)

系统集成了 DeepSeek AI 进行弹幕智能分析，包括：
- 📊 **弹幕总结** - 分析学生弹幕的整体情况、热点话题、精华观点
- 💎 **精华提炼** - 去重并提炼最有价值的学生发言
- ☁️ **词云分析** - 基于词云数据分析学生关注点和学习状态

#### 在 Render 上配置环境变量

1. 登录 Render 控制台
2. 选择你的 Web Service
3. 进入 **Environment** 选项卡
4. 添加环境变量：
   - **Key**: `DEEPSEEK_API_KEY`
   - **Value**: `你的DeepSeek API密钥`
5. 保存后服务会自动重新部署

> ⚠️ **安全提示**: 不要将 API 密钥直接写在代码中提交到 GitHub，请使用环境变量！

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
