以下是一份适合放在 GitHub 上的 `README.md` 文档，你可以复制粘贴到项目根目录，并根据实际情况微调（如替换邮箱、演示截图等）。

```markdown
服务器运维监控系统 (Server Monitor)

一个基于 **Flask + Celery + Redis + MySQL** 的轻量级服务器性能监控平台，可实时采集 CPU、内存、磁盘、网络指标，提供历史趋势图表和阈值告警功能。

![Python Version](https://img.shields.io/badge/python-3.7-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.5-green)
![Celery](https://img.shields.io/badge/Celery-5.2.7-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Redis](https://img.shields.io/badge/Redis-7.0-red)

---
功能特点

- **实时监控** – 每秒采集一次系统指标，前端仪表盘每10秒自动刷新
- **历史趋势** – 最近24小时 CPU/内存/磁盘使用率变化曲线（ECharts）
- **定时采集** – Celery Beat 每60秒自动执行采集任务
- **双存储** – 历史数据持久化到 MySQL，最新数据缓存到 Redis
- **智能告警** – 超过阈值时记录告警事件并打印日志（可扩展邮件/钉钉）
- **简洁 Web UI** – Bootstrap 响应式布局，开箱即用

---

## 技术栈

| 分类       | 技术                                                         |
|-----------|--------------------------------------------------------------|
| 后端框架   | Flask + Flask-CORS                                           |
| 异步任务   | Celery (Worker + Beat)                                       |
| 数据库     | MySQL 8.0 (数据持久化)                                       |
| 缓存/消息  | Redis 7.0 (Celery broker/backend + 最新指标缓存)              |
| 系统监控   | psutil                                                       |
| 前端图表   | ECharts + Bootstrap                                          |
| Python 版本| 3.7                                                          |

---

## 项目结构

```
monitor_project/
├── app/
│   ├── __init__.py
│   ├── api.py               # Flask 路由与视图
│   ├── tasks.py             # Celery 任务定义
│   ├── monitor.py           # psutil 指标采集
│   ├── models.py            # MySQL/Redis 操作
│   ├── alert.py             # 告警逻辑
│   └── templates/
│       └── dashboard.html   # 前端仪表盘
├── config.py                # 配置文件（数据库、Redis等）
├── run.py                   # Flask 启动入口
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

---

## 快速开始

### 1. 环境准备 (Ubuntu 22.04)

```bash
# 安装 MySQL、Redis
sudo apt update
sudo apt install mysql-server redis-server -y

# 安装 Python 3.7 及虚拟环境支持
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.7 python3.7-venv python3.7-dev -y
```

### 2. 克隆项目并创建虚拟环境

```bash
git clone https://github.com/yourname/monitor_project.git
cd monitor_project
python3.7 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install 'importlib_metadata<5.0'   # 兼容 Python 3.7
```

> `requirements.txt` 内容见附录。

### 4. 配置数据库

```bash
# 登录 MySQL (root)
sudo mysql
```

执行以下 SQL：

```sql
CREATE DATABASE monitor_db CHARACTER SET utf8mb4;
CREATE USER 'monitor_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourStrongPwd123!';
GRANT ALL PRIVILEGES ON monitor_db.* TO 'monitor_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

然后创建数据表（使用 `monitor_user` 登录）：

```bash
mysql -u monitor_user -p
USE monitor_db;
# 复制 SQL 建表语句（参见附录）
```

### 5. 修改配置

编辑 `config.py`，将 `MYSQL_PASSWORD` 改为你设置的密码。

### 6. 启动服务（需要三个终端）

| 终端 | 命令 |
|------|------|
| Worker | `celery -A app.tasks worker --loglevel=info -c 1` |
| Beat   | `celery -A app.tasks beat --loglevel=info` |
| Web    | `python run.py` |

### 7. 访问监控页面

浏览器打开 `http://localhost:5000`，等待60秒后即可看到数据。

---

## 预览截图

(建议放置一张仪表盘截图，此处留空)

---

## 常见问题

### 1. `ModuleNotFoundError: No module named 'app'`
确保在项目根目录下运行，且 `app/__init__.py` 存在。

### 2. Celery 报错 `AttributeError: 'EntryPoints' object has no attribute 'get'`
```bash
pip install 'importlib_metadata<5.0'
```

### 3. MySQL 连接失败 `Access denied`
- 检查 `config.py` 中的密码与数据库用户密码一致。
- 确认 `monitor_user` 已授权 `monitor_db`。

### 4. 前端显示无数据
- 检查 Celery worker/beat 是否正常运行。
- 查看 MySQL 中 `metrics_history` 表是否有记录。
- 测试 Redis：`redis-cli ping` 应返回 `PONG`。

---

## 扩展计划

- [ ] 支持多主机监控（通过 SSH 或 Agent）
- [ ] 邮件/企业微信告警
- [ ] 使用 Docker Compose 一键部署
- [ ] 增加 JWT 认证与用户管理

---

## 许可证

MIT License

---

## 附录

### requirements.txt

```
Flask==2.2.5
Flask-CORS==4.0.0
celery==5.2.7
redis==4.5.4
pymysql==1.0.2
psutil==5.9.4
cryptography==41.0.7
```

### 建表 SQL

```sql
USE monitor_db;

CREATE TABLE hosts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(100) NOT NULL UNIQUE,
    ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metrics_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    metric_time DATETIME NOT NULL,
    cpu_percent FLOAT,
    mem_total BIGINT,
    mem_used BIGINT,
    mem_percent FLOAT,
    disk_total BIGINT,
    disk_used BIGINT,
    disk_percent FLOAT,
    net_sent BIGINT,
    net_recv BIGINT,
    INDEX idx_host_time (host_id, metric_time),
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE CASCADE
);

CREATE TABLE alert_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(50) NOT NULL,
    threshold FLOAT NOT NULL,
    duration INT DEFAULT 0,
    enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE alert_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    metric_name VARCHAR(50),
    trigger_value FLOAT,
    message TEXT,
    alert_time DATETIME,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE CASCADE
);

INSERT INTO hosts (hostname, ip) VALUES ('ubuntu-local', '127.0.0.1');
INSERT INTO alert_rules (metric_name, threshold) VALUES 
    ('cpu_percent', 80.0),
    ('mem_percent', 85.0),
    ('disk_percent', 85.0);
```

---

**如果觉得本项目对你有帮助，欢迎 Star ⭐**
```

你可以将以上内容保存为 `README.md`，并根据实际 GitHub 仓库地址、个人联系方式等稍作修改。需要我帮你生成 `requirements.txt` 文件的内容吗？（上面已包含）
