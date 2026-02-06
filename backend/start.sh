#!/bin/sh
# Railway 启动脚本：确保 PORT 从环境变量正确传入 uvicorn
PORT=${PORT:-8000}
echo "Starting uvicorn on 0.0.0.0:$PORT"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
