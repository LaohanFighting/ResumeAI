@echo off
chcp 65001 >nul
echo ========================================
echo 修复Git锁文件工具
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查锁文件是否存在...
if exist ".git\index.lock" (
    echo 发现锁文件：.git\index.lock
    echo.
    echo [2/3] 尝试删除锁文件...
    del /f /q ".git\index.lock" 2>nul
    if exist ".git\index.lock" (
        echo 错误：无法删除锁文件，可能被其他程序占用
        echo.
        echo 请执行以下操作：
        echo 1. 关闭所有可能使用Git的程序（Cursor、VS Code、Git GUI等）
        echo 2. 等待几秒钟
        echo 3. 重新运行此脚本
        pause
        exit /b 1
    ) else (
        echo 成功删除锁文件！
    )
) else (
    echo 未发现锁文件，无需修复
)

echo.
echo [3/3] 验证Git状态...
git status
echo.
echo ========================================
echo 修复完成！
echo ========================================
echo.
echo 现在可以执行：
echo   git add .
echo   git commit -m "Initial commit"
echo.
pause
