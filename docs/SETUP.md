# 自由图书 - 本地部署指南

基于 Vue 3 + Element Plus + FastAPI + MySQL 的电子书网盘下载分享平台。

## 功能特性

- 用户前台：首页推荐、分类浏览、搜索、图书详情、网盘链接下载
- 管理后台：图书 CRUD、分类管理、数据统计
- Facebook 蓝色风格 UI
- 支持多网盘链接（夸克网盘、城通网盘等）

## 技术栈

| 前端 | 后端 | 数据库 |
|------|------|--------|
| Vue 3 + Vite + TypeScript | FastAPI + SQLAlchemy | MySQL 8.0 |
| Element Plus + Pinia | JWT 鉴权 + Pydantic | Docker |

## 快速启动

### 1. 启动 MySQL

```bash
docker-compose up -d
```

### 2. 启动后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
python init_db.py
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问

| 地址 | 说明 |
|------|------|
| http://localhost:5173 | 用户前台 |
| http://localhost:5173/admin/login | 管理后台 |
| http://localhost:8000/docs | API 文档 |

**默认管理员账号：** `admin` / `admin123`

## 批量导入电子书

```bash
cd backend
python import_books.py              # 增量导入
python import_books.py --clear      # 清空后重新导入
```

## 重新生成 README 图书目录

```bash
cd backend
python generate_readme.py
```

## 环境变量

复制 `backend/.env.example` 为 `backend/.env` 并按需修改。
