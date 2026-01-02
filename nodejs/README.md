# 🎬 实时弹幕词云系统 + AI 智能分析

基于 WebSocket 的实时弹幕词云系统，集成 DeepSeek AI 智能分析，专为课堂互动设计。

## ✨ 核心功能

### 📝 实时弹幕词云
- 🚀 **真正实时** - WebSocket 即时推送，所有人同步看到
- 💫 **无刷新无闪烁** - 流畅体验，词云动态更新
- 📱 **响应式设计** - 完美支持手机、平板、投影仪
- 🎨 **动态词云** - 浮动动画，彩虹配色，视觉吸引力强

### 📋 问题管理系统
- 🎯 老师发布问题，全员实时看到
- 💬 学生针对问题发送弹幕回答
- 📊 自动统计发言排行榜
- 🔄 一键清除问题和数据

### 🤖 AI 智能分析 (DeepSeek)
- **智能总结** - 自动分析学生弹幕，提炼核心观点
- **精华提炼** - 去重、分类、提取最有价值的回答
- **课堂展示** - 简洁输出（200字内），适合投影展示
- **透明覆盖** - AI 结果覆盖在词云上，背景透明可见词云
- **实时广播** - 分析结果自动推送给所有在线用户

## 🎯 典型使用场景

**课堂互动流程：**
1. 📤 老师发布问题："你最喜欢心理学的哪个部分？"
2. 💭 学生发送弹幕回答
3. 📊 词云实时生成，显示高频关键词
4. 🤖 老师点击"AI 分析"
5. ✨ AI 自动总结：核心观点 + 精华表达
6. 👥 分析结果展示给全体师生

## 🚀 快速开始

### 本地运行

```bash
# 1. 进入项目目录
cd nodejs

# 2. 安装依赖
npm install

# 3. 启动服务
npm start
```

然后访问 `http://localhost:3000`

### 局域网访问（手机/投影仪）

1. 电脑和设备连接同一 WiFi
2. 查看电脑 IP（如 `192.168.1.100`）
3. 设备浏览器访问 `http://192.168.1.100:3000`

## ☁️ 部署到 Render（推荐）

### 第一步：推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库.git
git push -u origin main
```

### 第二步：部署到 Render

1. 访问 [Render](https://render.com)，注册/登录
2. 点击 **New** → **Web Service**
3. 连接你的 GitHub 仓库
4. 配置：
   - **Name**: 自定义名称
   - **Root Directory**: `nodejs`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. 点击 **Create Web Service**

### 第三步：配置环境变量

在 Render 控制台：
1. 进入 **Environment** 标签
2. 添加环境变量：

| Key | Value | 说明 |
|-----|-------|------|
| `DEEPSEEK_API_KEY` | 你的 API 密钥 | DeepSeek AI 功能 |
| `PORT` | 自动设置 | Render 自动配置 |

3. 保存后自动重新部署

> 💡 **获取 DeepSeek API 密钥**: 访问 [DeepSeek 官网](https://platform.deepseek.com/)

## 🔧 配置说明

### 修改数据库连接

编辑 `server.js`：

```javascript
const NEO4J_URI = "neo4j+s://你的地址.databases.neo4j.io";
const NEO4J_USER = "neo4j";
const NEO4J_PASSWORD = "你的密码";
const TARGET_LABEL = "Danmu_xinli";  // 数据标签
const ADMIN_PASSWORD = "admin888";   // 管理员密码
```

### AI 功能说明

**简洁模式**（当前版本）：
- 输出控制在 200 字内
- 提炼 3-5 个核心观点
- 适合课堂投影展示
- 结合问题分析回答

**提示词优化**：在 `server.js` 的 `analyzeForClassroom()` 函数中调整

## 📱 使用指南

### 学生端操作
1. 输入姓名
2. 输入弹幕内容（回答问题）
3. 点击"发送弹幕"
4. 查看词云和 AI 分析结果

### 管理员操作
1. 点击"🔐 管理员"展开
2. 输入密码：`admin888`
3. **设置问题**：
   - 在"📋 设置问题"框输入问题
   - 点击"📤 发布问题"
   - 全员实时看到问题
4. **AI 分析**：
   - 点击"✨ 分析弹幕·提炼精华"
   - AI 结果覆盖显示在词云上
   - 所有用户同步看到分析结果
5. **清理数据**：
   - 清空词云：只清除词云数据
   - 清空所有：清除所有弹幕和词云

## 📂 项目结构

```
nodejs/
├── server.js              # 后端服务（WebSocket + AI）
├── package.json           # 依赖配置
├── public/
│   ├── index.html        # 前端页面（学生端）
│   └── admin.html        # 后台管理（可选）
└── README.md             # 本文档
```

## 🎨 界面设计

### 布局
- **左侧栏**（300px）：发送弹幕 + 排行榜 + 管理员
- **主区域**：问题展示 + 词云 + AI 结果覆盖层

### 配色方案
- **主色调**：紫色渐变（#667eea → #764ba2）
- **AI 色调**：青绿色（#00b894 → #00cec9）
- **词云颜色**：彩虹 8 色动态随机

### 特效
- 词云浮动动画（2.5-4.5s）
- AI 结果 85% 透明覆盖
- 毛玻璃背景模糊（5px）

## 🔄 与 Streamlit 版本对比

| 特性 | Streamlit 版本 | Node.js 版本 |
|------|---------------|-------------|
| **实时性** | 轮询刷新（3秒） | WebSocket 即时 |
| **页面闪烁** | 有 | 无 |
| **并发支持** | 一般 | 优秀 |
| **AI 功能** | 无 | ✅ 集成 DeepSeek |
| **问题管理** | 无 | ✅ 实时发布 |
| **部署难度** | 简单 | 中等 |
| **手机体验** | 一般 | 优秀 |

## 🛠️ 技术栈

- **后端**: Node.js + Express + Socket.IO
- **数据库**: Neo4j（图数据库）
- **AI**: DeepSeek API
- **前端**: 原生 HTML/CSS/JS + WordCloud2.js
- **部署**: Render / Railway / Vercel

## 📄 许可

MIT License

## 🤝 贡献

欢迎提出建议和改进！

---

**开发者**: GitHub Copilot  
**最后更新**: 2026年1月2日
| 并发支持 | 一般 | 优秀 |
| 部署难度 | 简单 | 中等 |
