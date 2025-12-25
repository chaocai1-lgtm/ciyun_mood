from neo4j import GraphDatabase
from datetime import datetime

class Neo4jHandler:
    def __init__(self, uri, user, password, label="Danmu"):
        """
        初始化 Neo4j 数据库连接
        :param label: 专属标签，用于区分不同用户的数据
        """
        # 添加连接超时配置，避免长时间等待
        self.driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
            connection_timeout=10,  # 连接超时10秒
            max_connection_lifetime=60,
            connection_acquisition_timeout=10  # 获取连接超时10秒
        )
        self.label = label
        self.keyword_label = f"Keyword_{label}"
        self.log_label = f"Log_{label}"
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            with self.driver.session() as session:
                session.run("RETURN 1").single()
            return True
        except Exception:
            return False

    def close(self):
        self.driver.close()

    # ========== 词云相关操作 ==========
    def add_record(self, name, content):
        """添加弹幕记录（包含姓名、内容、时间），同时更新词云"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with self.driver.session() as session:
            # 添加日志记录
            session.execute_write(self._create_log_record, name, content, timestamp, self.log_label)
            # 同时更新词云（以内容为关键词）
            session.execute_write(self._create_and_return_keyword, content, self.keyword_label)

    @staticmethod
    def _create_log_record(tx, name, content, timestamp, label):
        query = f"""
            CREATE (l:{label} {{姓名: $name, 内容: $content, 时间: $timestamp}})
        """
        tx.run(query, name=name, content=content, timestamp=timestamp)

    @staticmethod
    def _create_and_return_keyword(tx, text, label):
        query = f"""
            MERGE (k:{label} {{text: $text}})
            ON CREATE SET k.count = 1, k.last_updated = timestamp()
            ON MATCH SET k.count = k.count + 1, k.last_updated = timestamp()
            RETURN k.text, k.count
        """
        result = tx.run(query, text=text)
        return result.single()

    def get_cloud_data(self):
        """获取词云数据"""
        with self.driver.session() as session:
            return session.execute_read(self._get_keywords, self.keyword_label)

    @staticmethod
    def _get_keywords(tx, label):
        query = f"""
            MATCH (k:{label})
            RETURN k.text as name, k.count as value
            ORDER BY k.count DESC LIMIT 100
        """
        result = tx.run(query)
        return [{"name": record["name"], "value": record["value"]} for record in result]

    def get_logs(self):
        """获取所有日志记录"""
        with self.driver.session() as session:
            return session.execute_read(self._get_all_logs, self.log_label)

    @staticmethod
    def _get_all_logs(tx, label):
        query = f"""
            MATCH (l:{label})
            RETURN l.时间 as 时间, l.姓名 as 姓名, l.内容 as 内容
            ORDER BY l.时间 DESC
        """
        result = tx.run(query)
        return [{"时间": record["时间"], "姓名": record["姓名"], "内容": record["内容"]} for record in result]

    def clear_cloud_only(self):
        """只清除词云节点（前端清屏），保留日志"""
        with self.driver.session() as session:
            session.execute_write(self._delete_keywords_only, self.keyword_label)

    @staticmethod
    def _delete_keywords_only(tx, label):
        query = f"MATCH (k:{label}) DETACH DELETE k"
        tx.run(query)

    def clear_all(self):
        """清除所有数据（词云 + 日志）"""
        with self.driver.session() as session:
            session.execute_write(self._delete_all_data, self.keyword_label, self.log_label)

    @staticmethod
    def _delete_all_data(tx, keyword_label, log_label):
        query = f"MATCH (n) WHERE n:{keyword_label} OR n:{log_label} DETACH DELETE n"
        tx.run(query)
