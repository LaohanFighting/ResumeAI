# Stripe CLI 安装详细指南

Stripe CLI是一个命令行工具，用于与Stripe API交互和测试Webhook。

---

## 🪟 Windows 安装方法

### 方法1：使用 Scoop（推荐，最简单）

**步骤1：安装Scoop（如果还没有）**

1. 打开PowerShell（以管理员身份运行）
2. 运行以下命令：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

**步骤2：使用Scoop安装Stripe CLI**
```powershell
scoop install stripe
```

**步骤3：验证安装**
```powershell
stripe --version
```

应该显示版本号，例如：`stripe version 1.x.x`

---

### 方法2：使用 Chocolatey

**步骤1：安装Chocolatey（如果还没有）**

1. 打开PowerShell（以管理员身份运行）
2. 运行：
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**步骤2：使用Chocolatey安装Stripe CLI**
```powershell
choco install stripe
```

**步骤3：验证安装**
```powershell
stripe --version
```

---

### 方法3：手动下载安装（适用于所有Windows版本）

**步骤1：下载Stripe CLI**

1. 访问：https://github.com/stripe/stripe-cli/releases/latest
2. 找到 "Assets" 部分
3. 下载Windows版本：
   - 64位：`stripe_X.X.X_windows_x86_64.zip`
   - 32位：`stripe_X.X.X_windows_i386.zip`（较少见）

**步骤2：解压文件**

1. 解压下载的zip文件
2. 你会得到一个 `stripe.exe` 文件

**步骤3：添加到PATH（重要）**

**选项A：添加到用户PATH（推荐）**

1. 将 `stripe.exe` 复制到一个固定位置，例如：
   ```
   C:\Users\eahahns\stripe-cli\
   ```

2. 添加到PATH：
   - 按 `Win + R`，输入 `sysdm.cpl`，按回车
   - 点击 "高级" 标签
   - 点击 "环境变量"
   - 在 "用户变量" 部分，找到 `Path`，点击 "编辑"
   - 点击 "新建"，输入：`C:\Users\eahahns\stripe-cli`
   - 点击 "确定" 保存所有窗口

3. **重新打开PowerShell**（重要！）

**选项B：使用PowerShell临时添加（每次需要）**

```powershell
$env:Path += ";C:\Users\eahahns\stripe-cli"
```

**步骤4：验证安装**

打开**新的**PowerShell窗口，运行：
```powershell
stripe --version
```

---

## 🍎 macOS 安装方法

### 方法1：使用 Homebrew（推荐）

```bash
brew install stripe/stripe-cli/stripe
```

### 方法2：使用 MacPorts

```bash
sudo port install stripe-cli
```

### 方法3：手动下载

1. 访问：https://github.com/stripe/stripe-cli/releases/latest
2. 下载macOS版本：`stripe_X.X.X_macos_x86_64.tar.gz` 或 `stripe_X.X.X_macos_arm64.tar.gz`（M1/M2芯片）
3. 解压并移动到 `/usr/local/bin`：
```bash
tar -xzf stripe_X.X.X_macos_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

---

## 🐧 Linux 安装方法

### 方法1：使用包管理器

**Ubuntu/Debian:**
```bash
# 下载并安装
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_X.X.X_linux_x86_64.tar.gz
tar -xzf stripe_X.X.X_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

**Fedora/RHEL:**
```bash
# 类似Ubuntu，下载对应版本
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_X.X.X_linux_x86_64.tar.gz
tar -xzf stripe_X.X.X_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

### 方法2：使用Snap

```bash
sudo snap install stripe
```

---

## ✅ 验证安装

安装完成后，打开新的终端窗口，运行：

```bash
stripe --version
```

应该显示版本号，例如：
```
stripe version 1.18.0
```

---

## 🔐 首次使用：登录Stripe

安装完成后，需要登录你的Stripe账号：

```bash
stripe login
```

**登录流程：**

1. 运行 `stripe login` 命令
2. 会自动打开浏览器
3. 在浏览器中授权Stripe CLI访问你的账号
4. 授权成功后，终端会显示：`Done! The Stripe CLI is configured for your account.`

**如果浏览器没有自动打开：**
- 终端会显示一个URL
- 复制URL到浏览器手动打开
- 完成授权

---

## 🧪 测试安装

运行以下命令测试Stripe CLI是否正常工作：

```bash
# 查看帮助
stripe --help

# 测试API连接
stripe api version

# 查看当前登录的账号
stripe config --list
```

---

## 🔧 常见问题

### Q1: 命令未找到（command not found）

**Windows:**
- 确保已添加到PATH
- 重新打开PowerShell窗口
- 检查 `stripe.exe` 文件是否存在

**Mac/Linux:**
- 确保 `/usr/local/bin` 在PATH中
- 运行：`echo $PATH` 检查
- 可能需要重启终端

### Q2: 权限被拒绝（Permission denied）

**Mac/Linux:**
```bash
sudo chmod +x /usr/local/bin/stripe
```

### Q3: 登录失败

- 确保Stripe账号已注册
- 检查网络连接
- 尝试使用 `stripe login --interactive`

### Q4: Windows PowerShell执行策略错误

如果遇到执行策略错误，运行：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 下一步：配置Webhook

安装并登录后，可以开始配置Webhook：

```bash
# 转发Webhook到本地服务器
stripe listen --forward-to localhost:8000/stripe-webhook
```

这会：
- 监听Stripe事件
- 转发到你的本地服务器
- 显示webhook signing secret（需要添加到.env文件）

---

## 🎯 快速参考

**常用命令：**

```bash
# 登录
stripe login

# 转发Webhook
stripe listen --forward-to localhost:8000/stripe-webhook

# 触发测试事件
stripe trigger checkout.session.completed

# 查看API版本
stripe api version

# 查看配置
stripe config --list

# 查看帮助
stripe --help
```

---

## 📚 官方资源

- **Stripe CLI文档**：https://stripe.com/docs/stripe-cli
- **GitHub Releases**：https://github.com/stripe/stripe-cli/releases
- **Stripe Dashboard**：https://dashboard.stripe.com

---

**安装完成后，记得运行 `stripe login` 登录你的账号！**
