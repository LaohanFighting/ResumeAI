# 快速启动指南（付费MVP版本）

## ⚡ 3步启动

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `backend/.env`：
```env
OPENAI_API_KEY=sk-proj-your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

### 3. 启动服务

**终端1（后端）：**
```bash
python backend/main.py
```

**终端2（前端）：**
```bash
cd frontend
python -m http.server 8080
```

**终端3（Stripe Webhook - 可选）：**
```bash
stripe listen --forward-to localhost:8000/stripe-webhook
```

## 🧪 测试支付

**测试卡号：** `4242 4242 4242 4242`  
**有效期：** 任意未来日期  
**CVC：** 任意3位数字

## 📝 主要变更

- ✅ 新增 `/login` 接口（邮箱登录）
- ✅ 新增 `/create-checkout-session` 接口（Stripe支付）
- ✅ 新增 `/stripe-webhook` 接口（处理支付事件）
- ✅ `/generate` 接口需要登录，检查次数限制
- ✅ 前端添加登录模态框和升级提示

## 🔍 关键文件

- `backend/auth.py` - 用户认证（内存存储）
- `backend/stripe_handler.py` - Stripe支付处理
- `backend/main.py` - API端点（已更新）
- `frontend/script.js` - 前端逻辑（已重写）

详细说明请查看 `PAID_MVP_SETUP.md`
