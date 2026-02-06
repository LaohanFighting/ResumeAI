@echo off
echo ========================================
echo Stripe CLI 快速安装脚本 (Windows)
echo ========================================
echo.

echo 正在检查是否已安装 Stripe CLI...
stripe --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Stripe CLI 已安装
    stripe --version
    echo.
    echo 运行 'stripe login' 开始使用
    pause
    exit /b
)

echo.
echo 请选择安装方法：
echo.
echo [1] 使用 Scoop 安装（推荐，需要先安装Scoop）
echo [2] 使用 Chocolatey 安装（需要先安装Chocolatey）
echo [3] 手动下载安装（适用于所有Windows版本）
echo [4] 退出
echo.
set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" goto scoop
if "%choice%"=="2" goto chocolatey
if "%choice%"=="3" goto manual
if "%choice%"=="4" exit /b
goto invalid

:scoop
echo.
echo [方法1] 使用 Scoop 安装...
echo.
echo 检查是否已安装 Scoop...
scoop --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Scoop 未安装
    echo.
    echo 正在安装 Scoop...
    powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; irm get.scoop.sh | iex"
    if %errorlevel% neq 0 (
        echo ❌ Scoop 安装失败，请手动安装
        pause
        exit /b
    )
    echo ✅ Scoop 安装成功
)
echo.
echo 正在安装 Stripe CLI...
scoop install stripe
if %errorlevel% == 0 (
    echo ✅ Stripe CLI 安装成功！
    stripe --version
) else (
    echo ❌ 安装失败
)
goto end

:chocolatey
echo.
echo [方法2] 使用 Chocolatey 安装...
echo.
echo 检查是否已安装 Chocolatey...
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Chocolatey 未安装
    echo.
    echo 请先安装 Chocolatey：
    echo 访问: https://chocolatey.org/install
    pause
    exit /b
)
echo.
echo 正在安装 Stripe CLI...
choco install stripe -y
if %errorlevel% == 0 (
    echo ✅ Stripe CLI 安装成功！
    stripe --version
) else (
    echo ❌ 安装失败
)
goto end

:manual
echo.
echo [方法3] 手动下载安装
echo.
echo 正在打开下载页面...
start https://github.com/stripe/stripe-cli/releases/latest
echo.
echo 请按照以下步骤操作：
echo.
echo 1. 在浏览器中找到 "Assets" 部分
echo 2. 下载: stripe_X.X.X_windows_x86_64.zip
echo 3. 解压文件
echo 4. 将 stripe.exe 复制到以下目录（或任意目录）：
echo    C:\Users\%USERNAME%\stripe-cli\
echo.
echo 5. 添加到PATH：
echo    - 按 Win+R，输入 sysdm.cpl
echo    - 高级 → 环境变量
echo    - 编辑用户变量 Path
echo    - 添加: C:\Users\%USERNAME%\stripe-cli
echo    - 确定保存
echo.
echo 6. 重新打开PowerShell，运行: stripe --version
echo.
pause
goto end

:invalid
echo 无效选项，请重新运行脚本
pause
exit /b

:end
echo.
echo ========================================
echo 安装完成！
echo.
echo 下一步：
echo 1. 运行: stripe login
echo 2. 运行: stripe listen --forward-to localhost:8000/stripe-webhook
echo ========================================
pause
