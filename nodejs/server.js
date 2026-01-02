const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const neo4j = require('neo4j-driver');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: { origin: "*" }
});

// ======================= 配置区 =======================
const PORT = process.env.PORT || 3000;
const NEO4J_URI = "neo4j+s://7eb127cc.databases.neo4j.io";
const NEO4J_USER = "neo4j";
const NEO4J_PASSWORD = "wE7pV36hqNSo43mpbjTlfzE7n99NWcYABDFqUGvgSrk";
const TARGET_LABEL = "Danmu_xinli";
const ADMIN_PASSWORD = "admin888";
// =====================================================

// Neo4j 连接
const driver = neo4j.driver(NEO4J_URI, neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD));
const KEYWORD_LABEL = `Keyword_${TARGET_LABEL}`;
const LOG_LABEL = `Log_${TARGET_LABEL}`;

// 静态文件
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// 获取词云数据
async function getCloudData() {
    const session = driver.session();
    try {
        const result = await session.run(
            `MATCH (k:${KEYWORD_LABEL}) RETURN k.text as name, k.count as value ORDER BY k.count DESC LIMIT 100`
        );
        return result.records.map(r => ({
            name: r.get('name'),
            value: r.get('value').toNumber ? r.get('value').toNumber() : r.get('value')
        }));
    } finally {
        await session.close();
    }
}

// 获取日志数据
async function getLogs() {
    const session = driver.session();
    try {
        const result = await session.run(
            `MATCH (l:${LOG_LABEL}) RETURN l.时间 as time, l.姓名 as name, l.内容 as content ORDER BY l.时间 DESC LIMIT 100`
        );
        return result.records.map(r => ({
            time: r.get('time'),
            name: r.get('name'),
            content: r.get('content')
        }));
    } finally {
        await session.close();
    }
}

// 添加弹幕
async function addDanmu(name, content) {
    const session = driver.session();
    const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    try {
        // 添加日志
        await session.run(
            `CREATE (l:${LOG_LABEL} {姓名: $name, 内容: $content, 时间: $timestamp})`,
            { name, content, timestamp }
        );
        // 更新词云
        await session.run(
            `MERGE (k:${KEYWORD_LABEL} {text: $content})
             ON CREATE SET k.count = 1
             ON MATCH SET k.count = k.count + 1`,
            { content }
        );
        return true;
    } finally {
        await session.close();
    }
}

// 清空词云
async function clearCloud() {
    const session = driver.session();
    try {
        await session.run(`MATCH (k:${KEYWORD_LABEL}) DETACH DELETE k`);
        return true;
    } finally {
        await session.close();
    }
}

// 清空所有数据
async function clearAll() {
    const session = driver.session();
    try {
        await session.run(`MATCH (n) WHERE n:${KEYWORD_LABEL} OR n:${LOG_LABEL} DETACH DELETE n`);
        return true;
    } finally {
        await session.close();
    }
}

// WebSocket 连接
io.on('connection', async (socket) => {
    console.log('用户连接:', socket.id);
    
    // 发送初始数据
    try {
        const cloudData = await getCloudData();
        const logs = await getLogs();
        socket.emit('init', { cloudData, logs });
    } catch (err) {
        console.error('获取初始数据失败:', err);
    }
    
    // 接收新弹幕
    socket.on('danmu', async (data) => {
        const { name, content } = data;
        if (!name || !content) return;
        
        try {
            await addDanmu(name, content);
            const cloudData = await getCloudData();
            const logs = await getLogs();
            // 广播给所有用户
            io.emit('update', { cloudData, logs, newDanmu: { name, content } });
        } catch (err) {
            console.error('添加弹幕失败:', err);
            socket.emit('error', { message: '发送失败，请重试' });
        }
    });
    
    // 管理员清空词云
    socket.on('clearCloud', async (data) => {
        if (data.password !== ADMIN_PASSWORD) {
            socket.emit('error', { message: '密码错误' });
            return;
        }
        try {
            await clearCloud();
            const cloudData = await getCloudData();
            io.emit('update', { cloudData, logs: await getLogs() });
            socket.emit('success', { message: '词云已清空' });
        } catch (err) {
            socket.emit('error', { message: '清空失败' });
        }
    });
    
    // 管理员清空所有
    socket.on('clearAll', async (data) => {
        if (data.password !== ADMIN_PASSWORD) {
            socket.emit('error', { message: '密码错误' });
            return;
        }
        try {
            await clearAll();
            io.emit('update', { cloudData: [], logs: [] });
            socket.emit('success', { message: '所有数据已清空' });
        } catch (err) {
            socket.emit('error', { message: '清空失败' });
        }
    });
    
    socket.on('disconnect', () => {
        console.log('用户断开:', socket.id);
    });
});

// 启动服务器
server.listen(PORT, () => {
    console.log(`🚀 服务器运行在 http://localhost:${PORT}`);
    console.log(`📱 手机访问请使用局域网IP`);
});

// 优雅关闭
process.on('SIGINT', async () => {
    await driver.close();
    process.exit();
});
