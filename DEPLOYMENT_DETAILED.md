# 详细部署指南 - 从0到上线

本指南将详细指导你如何将ResumeAI部署到Railway，让网站可以在公网访问。预计时间：30-45分钟。

---

## 📋 目录

1. [前置准备](#前置准备)
2. [步骤1：准备代码仓库](#步骤1准备代码仓库)
3. [步骤2：创建Railway账号和项目](#步骤2创建railway账号和项目)
4. [步骤3：配置环境变量](#步骤3配置环境变量)
5. [步骤4：配置Stripe Webhook](#步骤4配置stripe-webhook)
6. [步骤5：测试部署](#步骤5测试部署)
7. [步骤6：自定义域名（可选）](#步骤6自定义域名可选)
8. [故障排查](#故障排查)

---

## 📋 前置准备

### 必需账号和密钥

在开始之前，确保你已经准备好：

- [ ] **Railway账号**：访问 https://railway.app 注册（免费，使用GitHub账号登录）
- [ ] **GitHub账号**：用于代码仓库（如果没有，访问 https://github.com 注册）
- [ ] **OpenAI API密钥**：格式 `sk-proj-...`（从 https://platform.openai.com/api-keys 获取）
- [ ] **Stripe账号**：访问 https://stripe.com 注册（免费）
- [ ] **Stripe测试密钥**：从Stripe Dashboard获取（格式 `sk_test_...`）

### 检查清单

- [ ] 本地代码可以正常运行
- [ ] 所有功能已测试通过
- [ ] `.env` 文件已添加到 `.gitignore`（不会提交到Git）
- [ ] 已准备好所有密钥

---

## 步骤1：准备代码仓库

### 1.1 检查项目文件

确保以下文件存在：

```
项目根目录/
├── Dockerfile              ✅ 必需
├── railway.toml           ✅ 必需
├── .dockerignore           ✅ 推荐
├── .gitignore              ✅ 必需
├── backend/
│   ├── main.py
│   ├── ai.py
│   ├── auth.py
│   ├── stripe_handler.py
│   └── requirements.txt
└── frontend/
    ├── landing.html
    ├── index.html
    ├── share.html
    └── ... (其他文件)
```

### 1.2 检查 .gitignore

打开 `.gitignore` 文件，确保包含：

```
.env
backend/.env
*.env
```

**重要：** 不要将包含真实密钥的 `.env` 文件提交到Git！

### 1.3 初始化Git仓库（如果还没有）

**什么是"项目根目录"？**
- 项目根目录就是包含 `Dockerfile`、`backend/`、`frontend/` 等文件夹的最外层目录
- 在你的情况下，应该是：`C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot\`

**如何打开项目根目录？**

**方法1：使用Cursor/VS Code**
1. 在Cursor中，点击菜单栏 "Terminal" → "New Terminal"
2. 终端会自动打开在项目根目录

**方法2：使用Windows PowerShell**
1. 按 `Win + R`，输入 `powershell`，回车
2. 使用 `cd` 命令切换到项目目录：
```powershell
cd "C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot"
```

**方法3：使用文件资源管理器**
1. 打开文件资源管理器，导航到项目文件夹
2. 在地址栏输入 `powershell` 或 `cmd`，回车
3. 终端会自动在当前位置打开

---

**检查是否已有Git仓库：**

在终端中执行：
```powershell
git status
```

**情况A：如果显示 "fatal: not a git repository"**
→ 说明还没有Git仓库，需要初始化（继续下面的步骤）

**情况B：如果显示 "nothing added to commit but untracked files present"**
→ ✅ **说明已有Git仓库，但文件还没有提交**
→ 这是正常状态，继续下面的步骤添加文件

**情况C：如果显示文件列表或 "nothing to commit, working tree clean"**
→ 说明已有Git仓库且文件已提交，可以直接推送到GitHub

---

**初始化Git仓库（如果还没有）：**

**步骤1：打开终端并切换到项目根目录**
```powershell
# 确认当前位置（应该显示项目路径）
pwd

# 如果不在项目目录，切换到项目目录
cd "C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot"
```

**步骤2：初始化Git仓库**
```powershell
# 初始化Git仓库（会在项目根目录创建 .git 文件夹）
git init
```

**步骤3：添加所有文件到暂存区**
```powershell
# 添加所有文件（.gitignore会自动排除.env等文件）
git add .
```

**步骤4：创建首次提交**
```powershell
# 提交所有文件，创建初始版本
git commit -m "Initial commit - Ready for deployment"
```

**验证初始化成功：**
```powershell
# 查看Git状态（应该显示 "nothing to commit, working tree clean"）
git status

# 查看提交历史（应该看到刚才的提交）
git log
```

---

**如果已经有Git仓库但文件未提交：**

**步骤1：检查当前状态**
```powershell
# 查看哪些文件还未跟踪
git status
```

**如果看到 "nothing added to commit but untracked files present"：**

**步骤2：添加所有文件**
```powershell
# 添加所有未跟踪的文件（.gitignore会自动排除.env等文件）
git add .
```

**步骤3：创建首次提交**
```powershell
# 提交所有文件
git commit -m "Initial commit - Ready for deployment"
```

**步骤4：验证提交成功**
```powershell
# 查看状态（应该显示 "nothing to commit, working tree clean"）
git status

# 查看提交历史
git log --oneline
```

**如果遇到 "unable to unlink .git/index.lock" 或 "File exists" 错误：**

这个错误表示Git的索引文件被锁定了，通常是因为：
- 另一个Git进程正在运行
- 之前的Git操作异常退出，留下了锁文件

**解决方法：**

**方法1：使用批处理脚本（推荐）**
1. 双击运行项目根目录下的 `修复Git锁文件.bat`
2. 脚本会自动删除锁文件并验证Git状态

**方法2：手动删除锁文件**

**步骤1：关闭所有Git相关程序**
- 关闭Cursor/VS Code
- 关闭所有终端窗口
- 关闭Git GUI工具（如果有）

**步骤2：删除锁文件**
```powershell
# 在PowerShell中执行
cd "C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot"
Remove-Item -Force .git/index.lock -ErrorAction SilentlyContinue
```

**如果文件被占用无法删除：**
1. 打开任务管理器（`Ctrl + Shift + Esc`）
2. 查找并结束所有 `git.exe` 进程
3. 等待几秒后重试删除

**步骤3：验证并继续**
```powershell
# 检查Git状态
git status

# 如果正常，继续添加文件
git add .
```

**方法3：如果仍然无法删除**
```powershell
# 使用管理员权限的PowerShell
# 右键点击PowerShell → "以管理员身份运行"
cd "C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot"
Remove-Item -Force .git/index.lock
```

---

**如果已经有Git仓库且文件已提交：**

**步骤1：检查当前状态**
```powershell
# 查看哪些文件有更改
git status
```

**步骤2：如果有未提交的更改**
```powershell
# 添加所有更改的文件
git add .

# 提交更改
git commit -m "Ready for production deployment"
```

**步骤3：查看提交历史**
```powershell
# 查看所有提交记录
git log --oneline
```
