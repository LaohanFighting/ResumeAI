# Fly.io 部署步骤（ResumeAI）

用同一套 GitHub 代码在 Fly.io 上部署，约 30 分钟。Fly 的出口 IP 与 Railway 不同，有机会正常连上 OpenAI。

---

## 一、前置准备

- 已安装 **Git**（你已有）
- **GitHub 仓库** 已包含最新代码（你已有）
- 准备好 **OPENAI_API_KEY**、**STRIPE_SECRET_KEY**（Stripe Webhook 部署后再配）

---

## 二、安装 Fly CLI

### Windows（PowerShell）

```powershell
# 使用官方安装脚本
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

安装完成后**新开一个终端**，执行：

```powershell
fly version
```

能显示版本号即安装成功。

### 若安装脚本失败，可手动下载

1. 打开：https://github.com/superfly/flyctl/releases  
2. 下载最新版 `flyctl_xxx_windows_amd64.zip`  
3. 解压得到 `flyctl.exe`，放到 PATH 目录（如 `C:\Windows` 或项目目录），终端里用 `fly` 或 `.\flyctl.exe` 调用。

---

## 三、登录 Fly.io

```powershell
fly auth login
```

会打开浏览器，用 **GitHub** 或 **Email** 登录并授权。成功后终端会提示 “Successfully logged in”.

---

## 四、在项目目录创建/确认配置

1. **进入项目根目录**（与 `Dockerfile`、`fly.toml` 同级）：

```powershell
cd "C:\Users\eahahns\OneDrive - Ericsson\Desktop\WORKSHOP\GitHub_Copilot"
```

2. **确认文件存在**：
   - `Dockerfile` ✅
   - `fly.toml` ✅（项目里已提供）

3. **（可选）修改应用名**：  
   打开 `fly.toml`，把第一行 `app = "resumeai"` 改成你喜欢的名字（如 `my-resume-ai`），域名将变为 `你的名字.fly.dev`。不改也可以。

---

## 五、首次创建应用（不部署）

```powershell
fly launch --no-deploy
```

按提示操作：

- **App Name**：直接回车用 `resumeai`，或输入新名字（需唯一）。
- **Region**：选一个离你或用户近的（如 `nrt` 东京、`iad` 美东）。
- **Postgres / Redis**：都选 **No**（我们不用）。
- **Deploy now?**：选 **No**（我们先设环境变量再部署）。

完成后会生成/更新 `fly.toml`，不会立刻部署。

---

## 六、设置环境变量（密钥）

在项目根目录执行（把值换成你自己的）：

```powershell
fly secrets set OPENAI_API_KEY=你的OpenAI密钥
fly secrets set STRIPE_SECRET_KEY=你的Stripe测试密钥
```

**注意**：

- 等号前后不要空格。
- 密钥不要加引号（除非密钥里含空格）。
- `STRIPE_WEBHOOK_SECRET` 等部署拿到域名后再设（见第八步）。

---

## 七、部署

```powershell
fly deploy
```

首次会构建镜像并上传，约 3～8 分钟。成功后会显示类似：

```
--> v0 deployed successfully
```

查看状态和域名：

```powershell
fly status
fly open
```

`fly open` 会打开浏览器访问你的应用（如 `https://resumeai.fly.dev`）。

---

## 八、配置 Stripe Webhook（支付后次数才会增加）

1. **记下 Fly 域名**  
   例如：`https://resumeai.fly.dev`（以 `fly status` 或控制台显示为准）。

2. **在 Stripe 添加 Webhook**  
   - 打开：https://dashboard.stripe.com/webhooks（保持 **Test mode**）  
   - **Add endpoint**  
   - **Endpoint URL**：`https://你的app名.fly.dev/stripe-webhook`  
   - **Events**：勾选 `checkout.session.completed`、`invoice.payment_succeeded`  
   - 保存后，复制 **Signing secret**（`whsec_...`）

3. **把 Webhook Secret 设到 Fly**  

```powershell
fly secrets set STRIPE_WEBHOOK_SECRET=whsec_你复制的密钥
```

Fly 会重新部署一次，无需再执行 `fly deploy`。

---

## 九、自测

- 首页：`https://你的app名.fly.dev/`  
- 应用页：`https://你的app名.fly.dev/app`  
- 健康检查：`https://你的app名.fly.dev/api/health`  
- 登录、生成简历、用测试卡支付，确认支付后次数增加。

---

## 十、常用命令

| 命令 | 说明 |
|------|------|
| `fly status` | 查看应用状态和域名 |
| `fly open` | 在浏览器打开应用 |
| `fly logs` | 查看实时日志（排错用） |
| `fly secrets list` | 查看已设的 secrets（不显示值） |
| `fly deploy` | 重新部署（代码或配置变更后） |

---

## 十一、故障排查

### 部署失败

- 执行 `fly logs` 看报错。
- 确认本机 Docker 未占用 8080，或 Fly 使用远程构建（默认会）。

### 打开网页报错

- `fly logs` 看是否有 Python/uvicorn 报错。
- 确认 `fly.toml` 里 `[http_service]` 的 `internal_port = 8080` 与 `start.sh` 里用的 `PORT` 一致（已设为 8080）。

### 生成简历仍报 Connection error

- 说明 Fly 当前区域出口 IP 仍可能被 OpenAI 限制；可尝试 `fly regions list` 后换一个 region 再 `fly deploy`。

---

部署完成后，用 **Fly 的域名** 访问即可；Railway 可保留或停用。若某一步报错，把命令和完整报错贴出来即可继续排查。
