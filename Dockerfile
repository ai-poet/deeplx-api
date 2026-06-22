# 设置基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用代码和启动脚本
COPY . .

# 设置启动脚本权限
RUN chmod +x start.sh

# 安装构建依赖（gevent 需要 C 编译器）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential python3-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 环境变量
ENV OPENAI_BASE_URL=https://api.openai.com/v1
ENV OPENAI_MODEL=gpt-4o-mini
ENV OPENAI_API_KEY=""

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["./start.sh"]
