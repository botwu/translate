# 🌐 AI翻译助手

一个基于大模型的智能中英文翻译应用，支持翻译和关键词提取功能。

## 功能特点

- **中英翻译**：智能将中文翻译成英文
- **关键词提取**：自动提取3个核心关键词
- **现代UI**：美观的深色主题界面
- **快速响应**：基于 FastAPI 的高性能后端

## 🛠️ 技术栈

### 后端
- Python 3.9+
- FastAPI - 现代高性能 Web 框架
- httpx - 异步 HTTP 客户端
- DeepSeek API - 大模型翻译能力

### 前端
- React 18 - UI 框架
- Vite - 构建工具
- 纯 CSS - 自定义样式

## 项目结构

```
task_best/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI 主程序
│   ├── requirements.txt    # Python 依赖
│   └── env_example.txt     # 环境变量示例
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── App.jsx        # 主组件
│   │   ├── main.jsx       # 入口文件
│   │   └── index.css      # 样式文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── README.md               # 项目说明
```

## 快速开始

### 1. 获取 DeepSeek API Key

1. 访问 [DeepSeek开放平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 创建 API Key（新用户有免费额度）

### 2. 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 将 env_example.txt 复制为 .env 并填入你的 API Key
cp env_example.txt .env
# 编辑 .env 文件，填入 DEEPSEEK_API_KEY=你的密钥

# 启动服务
python main.py
```

后端服务将在 http://localhost:8000 运行

### 3. 启动前端服务

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 运行

### 4. 使用应用

1. 打开浏览器访问 http://localhost:3000
2. 在输入框中输入中文内容
3. 点击"开始翻译"按钮
4. 查看英文翻译结果和提取的关键词

## 📡 API 文档

启动后端后，访问 http://localhost:8000/docs 查看交互式 API 文档。

### POST /translate

**请求示例：**
```json
{
  "text": "人工智能正在改变我们的生活方式"
}
```

**响应示例：**
```json
{
  "translation": "Artificial intelligence is changing the way we live.",
  "keywords": ["人工智能", "改变", "生活方式"]
}
```

## 💡 开发说明

- 后端使用 FastAPI 框架，支持异步处理
- 前端使用 Vite 作为构建工具，开发体验良好
- API 调用使用 DeepSeek 大模型，价格便宜且效果好

## 📝 注意事项

1. 请确保 `.env` 文件不要提交到代码仓库
2. API Key 请妥善保管，避免泄露
3. 翻译内容限制在 5000 字以内


