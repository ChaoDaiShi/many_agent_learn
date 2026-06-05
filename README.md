# AI智学助手

基于大模型的个性化资源生成与学习多智能体系统

## 项目简介

AI智学助手是一款面向教育领域的智能学习辅助系统，利用大语言模型和多智能体技术，为学生提供个性化的学习资源生成、学习路径规划和知识问答服务。

## 核心功能

- **学生画像构建**：通过对话式交互构建学生画像，了解学习目标、兴趣方向、知识基础和认知风格
- **RAG知识库检索**：支持PDF文档上传，构建向量知识库，提供精准的知识检索服务
- **个性化资源生成**：根据学生画像生成定制化的学习资源，包括课程讲解、思维导图、练习题库等
- **智能学习路径**：基于学生画像和学习进度，生成个性化学习路径规划
- **错题本管理**：记录和管理学生的错题，支持针对性练习

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus UI框架
- Pinia状态管理

### 后端
- Python 3.10+
- FastAPI Web框架
- MySQL 8.0+ 数据库
- Chroma 向量数据库
- 讯飞星火大模型 API

## 项目结构

```
ai_edu_system/
├── frontend/                    # Vue3前端应用
│   ├── src/
│   │   ├── api/               # API接口封装
│   │   ├── components/         # 公共组件
│   │   ├── views/              # 页面视图
│   │   ├── router/             # 路由配置
│   │   ├── store/              # Pinia状态管理
│   │   └── utils/              # 工具函数
│   ├── dist/                   # 构建产物
│   └── package.json
│
├── backend/                    # FastAPI后端服务
│   ├── main.py                # 项目入口
│   ├── api/                   # 路由接口层
│   ├── agent/                 # 多智能体模块
│   ├── service/               # 业务逻辑层
│   ├── db/                    # 数据库模块
│   ├── config/                # 配置文件
│   ├── utils/                 # 工具函数
│   └── requirements.txt       # Python依赖
│
├── docs/                      # 项目文档
│   ├── database.md            # 数据库设计文档
│   └── deploy.md              # 部署文档
│
└── sql/
    └── init.sql               # 数据库初始化脚本
```

## 快速开始

### 环境要求

- Node.js >= 18.0.0
- Python >= 3.10
- MySQL >= 8.0

### 1. 克隆项目

```bash
git clone <repository-url>
cd ai_edu_system
```

### 2. 数据库配置

创建数据库并执行初始化脚本：

```sql
CREATE DATABASE ai_edu_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```bash
mysql -u username -p ai_edu_db < sql/init.sql
```

### 3. 后端启动

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
```

## API接口

| 模块 | 接口 | 方法 | 说明 |
| :--- | :--- | :--- | :--- |
| 学生画像 | `/api/student/portrait/{student_id}` | GET | 获取学生画像 |
| 学生画像 | `/api/student/portrait` | POST | 创建学生画像 |
| RAG知识库 | `/api/rag/upload` | POST | 上传PDF文档 |
| RAG知识库 | `/api/rag/query` | POST | 检索知识库 |
| 资源生成 | `/api/gen/resource` | POST | 生成学习资源 |
| 学习路径 | `/api/study/path/{student_id}` | POST | 生成学习路径 |
| 健康检查 | `/api/health` | GET | 服务健康检查 |

## 配置说明

后端配置文件 `.env` 需要设置以下环境变量：

- 数据库连接信息（MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE）
- 讯飞星火API配置（SPARK_APP_ID, SPARK_API_KEY, SPARK_API_SECRET）
- JWT密钥（JWT_SECRET_KEY）

## 文档链接

- [数据库设计文档](docs/database.md)
- [部署文档](docs/deploy.md)

## 版本与备份

### 当前版本
- **版本号**: v1.0.0
- **备份名称**: `ai_edu_system_v1.0.0_20260605`
- **备份时间**: 2026年06月05日

### 版本历史
| 版本 | 备份名 | 日期 | 说明 |
| :--- | :--- | :--- | :--- |
| v1.0.0 | `ai_edu_system_v1.0.0_20260605` | 2026-06-05 | 初始版本，包含学生画像、RAG知识库、资源生成、学习路径等核心功能 |

### GitHub仓库
```bash
# 仓库地址
git@github.com:<username>/ai-edu-system.git

# 克隆命令
git clone git@github.com:<username>/ai-edu-system.git

# 提交命令
git add .
git commit -m "feat: 完成AI智学助手v1.0.0开发"
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
git push origin main
```

## 许可证

MIT License