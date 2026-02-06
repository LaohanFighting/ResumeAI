@echo off
chcp 65001 >nul
echo ========================================
echo Git提交工具
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查Git状态...
git status
echo.

echo [2/4] 添加所有文件到暂存区...
git add .
if %errorlevel% neq 0 (
    echo 错误：git add 失败
    pause
    exit /b 1
)
echo 文件添加成功！
echo.

echo [3/4] 创建提交...
git commit -m "Initial commit - Ready for deployment"
if %errorlevel% neq 0 (
    echo 错误：git commit 失败
    pause
    exit /b 1
)
echo 提交创建成功！
echo.

echo [4/4] 验证提交状态...
git status
echo.

echo ========================================
echo 完成！
echo ========================================
echo.
echo 下一步：推送到GitHub
echo   1. 在GitHub创建新仓库
echo   2. 执行：git remote add origin https://github.com/YOUR_USERNAME/resumeai.git
echo   3. 执行：git push -u origin main
echo.
pause
