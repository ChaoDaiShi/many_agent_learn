# 部署文档

## 系统概述

AI智学助手是基于大模型的个性化资源生成与学习多智能体系统，采用 Vue3 + FastAPI + MySQL + Chroma 技术栈。

## 环境要求

### 前端
- Node.js >= 18.0.0
- npm >= 9.0.0

### 后端
- Python >= 3.10
- MySQL >= 8.0
- Redis（可选，用于缓存）

## 部署步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd ai_edu_system
```

### 2. 数据库配置

#### 创建数据库

```sql
CREATE DATABASE ai_edu_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 执行初始化脚本

```bash
mysql -u username -p ai_edu_db < sql/init.sql
```

### 3. 后端部署

#### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 配置环境变量

复制 `.env` 文件并修改配置：

```bash
cp .env.example .env
```

修改 `.env` 文件：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=ai_edu_db

SPARK_APP_ID=your_app_id
SPARK_API_KEY=your_api_key
SPARK_API_SECRET=your_api_secret

CHROMA_PATH=./chroma_db
UPLOAD_FOLDER=./uploads

JWT_SECRET_KEY=your_jwt_secret_key
```

#### 启动后端服务

```bash
python main.py
```

或者使用 uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 前端部署

#### 安装依赖

```bash
cd frontend
npm install
```

#### 配置环境变量

修改 `.env.local` 文件：

```env
VITE_API_BASE=http://127.0.0.1:8000/api
```

#### 开发模式

```bash
npm run dev
```

#### 生产构建

```bash
npm run build
```

## 目录结构

```
ai_edu_system/
├── frontend/                    # Vue3前端
│   ├── public/                 # 静态资源
│   ├── src/
│   │   ├── api/               # 接口请求封装
│   │   ├── components/         # 公共组件
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   ├── store/              # Pinia状态管理
│   │   └── utils/              # 工具函数
│   ├── .env.local              # 环境变量
│   ├── package.json
│   └── vite.config.js
│
├── backend/                    # FastAPI后端
│   ├── main.py                # 项目入口
│   ├── requirements.txt       # Python依赖
│   ├── config/                # 配置文件
│   ├── api/                   # 路由接口层
│   ├── agent/                 # 多智能体模块
│   ├── db/                    # 数据库模块
│   ├── service/               # 业务逻辑层
│   ├── utils/                 # 工具函数
│   ├── uploads/               # 文件上传目录
│   └── chroma_db/             # Chroma向量库
│
├── docs/                      # 文档
│   ├── database.md            # 数据库设计文档
│   └── deploy.md              # 部署文档
│
└── sql/
    └── init.sql               # 数据库初始化脚本
```

## API接口

### 学生画像接口

| 接口 | 方法 | 说明 |
| :--- | :--- | :--- |
| `/api/student/portrait/{student_id}` | GET | 获取学生画像 |
| `/api/student/portrait` | POST | 创建学生画像 |
| `/api/student/portrait/{student_id}` | PUT | 更新学生画像 |
| `/api/student/portrait/{student_id}` | DELETE | 删除学生画像 |
| `/api/student/chat/{student_id}` | POST | 对话式画像构建 |

### RAG知识库接口

| 接口 | 方法 | 说明 |
| :--- | :--- | :--- |
| `/api/rag/upload` | POST | 上传PDF文档 |
| `/api/rag/documents` | GET | 获取文档列表 |
| `/api/rag/document/{doc_id}` | GET | 获取文档详情 |
| `/api/rag/document/{doc_id}` | DELETE | 删除文档 |
| `/api/rag/query` | POST | 检索知识库 |

### 资源生成接口

| 接口 | 方法 | 说明 |
| :--- | :--- | :--- |
| `/api/gen/resource` | POST | 生成学习资源 |
| `/api/gen/resources` | GET | 获取资源列表 |
| `/api/gen/resource/{resource_id}` | GET | 获取资源详情 |
| `/api/gen/resource/{resource_id}` | PUT | 重新生成资源 |
| `/api/gen/resource/{resource_id}` | DELETE | 删除资源 |
| `/api/gen/types` | GET | 获取资源类型 |

### 学习路径接口

| 接口 | 方法 | 说明 |
| :--- | :--- | :--- |
| `/api/study/path/{student_id}` | GET | 获取学习路径 |
| `/api/study/path/{student_id}` | POST | 生成学习路径 |
| `/api/study/path/{path_id}` | PUT | 更新学习路径 |
| `/api/study/wrong-questions/{student_id}` | GET | 获取错题列表 |
| `/api/study/wrong-question` | POST | 添加错题 |
| `/api/study/wrong-question/{question_id}` | DELETE | 删除错题 |
| `/api/study/progress/{student_id}` | GET | 获取学习进度 |
| `/api/study/progress/{student_id}` | PUT | 更新学习进度 |

## 健康检查

```bash
curl http://localhost:8000/api/health
```

响应示例：

```json
{
  "code": 200,
  "message": "OK",
  "service": "AI智学助手"
}
```

## 常见问题

### 1. MySQL连接失败

确保MySQL服务已启动，并且配置的用户名和密码正确。

### 2. Chroma向量库初始化失败

确保 `chroma_db` 目录有写入权限。

### 3. 前端无法连接后端

检查后端服务是否正常运行，以及前端 `.env.local` 配置的API地址是否正确。

## 日志

后端日志默认输出到控制台，可以通过配置logging模块进行日志持久化。

## 安全建议

1. 生产环境中使用HTTPS
2. 定期备份数据库和Chroma向量库
3. 限制文件上传大小和类型
4. 使用环境变量管理敏感信息