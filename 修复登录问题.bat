@echo off
echo ========================================
echo 修复登录问题 - 一键脚本
echo ========================================
echo.

echo [1/4] 停止所有Python进程...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo ✅ Python进程已停止
echo.

echo [2/4] 清理Python缓存文件...
cd backend
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo ✅ 已删除 __pycache__ 文件夹
) else (
    echo ℹ️  __pycache__ 文件夹不存在
)
del /q *.pyc 2>nul
echo ✅ 缓存文件已清理
cd ..
echo.

echo [3/4] 验证代码文件...
findstr /C:"created_at: Optional[str] = None" backend\auth.py >nul
if %errorlevel% == 0 (
    echo ✅ 代码文件已更新
) else (
    echo ❌ 警告：代码文件可能未更新，请检查 backend\auth.py
)
echo.

echo [4/4] 启动后端服务器...
echo.
echo ⚠️  请在新窗口中手动启动前端服务器：
echo    cd frontend
echo    python -m http.server 8080
echo.
echo ========================================
echo 正在启动后端服务器...
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

cd backend
python main.py
