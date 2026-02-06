# 使用Python官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 创建static目录并复制前端文件
RUN mkdir -p static
COPY frontend/ ./static/

# 暴露端口（Railway会自动设置PORT环境变量）
ENV PORT=8000

# 运行应用
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
