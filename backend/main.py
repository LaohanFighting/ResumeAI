"""
FastAPI后端主文件
提供简历和求职信生成API（付费MVP版本）
"""
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from dotenv import load_dotenv

# 首先加载.env文件中的环境变量（必须在导入其他模块之前）
load_dotenv(dotenv_path='backend/.env')

from ai import generate_resume_and_cover_letter
from auth import (
    create_user, get_user, deduct_credit, add_credits,
    create_session, get_email_from_session, User
)
from stripe_handler import (
    create_checkout_session, verify_webhook_signature, handle_payment_success
)

app = FastAPI(title="AI Resume & Cover Letter Generator")

# 配置CORS，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 数据模型 ====================

class GenerateRequest(BaseModel):
    """生成请求数据模型"""
    job_description: str
    candidate_background: str


class GenerateResponse(BaseModel):
    """生成响应数据模型"""
    resume: str
    cover_letter: str
    success: bool
    error: Optional[str] = None
    remaining_credits: Optional[int] = None  # 剩余次数


class LoginRequest(BaseModel):
    """登录请求数据模型"""
    email: EmailStr


class LoginResponse(BaseModel):
    """登录响应数据模型"""
    success: bool
    session_token: Optional[str] = None
    email: Optional[str] = None
    remaining_credits: Optional[int] = None
    error: Optional[str] = None


class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    email: str
    remaining_credits: int
    is_pro: bool


class CheckoutRequest(BaseModel):
    """创建支付会话请求"""
    success_url: str
    cancel_url: str


# ==================== 依赖项 ====================

def get_current_user(session_token: Optional[str] = Header(None, alias="X-Session-Token")) -> Optional[User]:
    """
    获取当前登录用户（依赖项）
    如果未登录，返回None（允许未登录用户使用1次）
    """
    if not session_token:
        return None
    
    email = get_email_from_session(session_token)
    if not email:
        return None
    
    user = get_user(email)
    return user


@app.get("/")
async def root():
    """Landing Page - 返回Landing页面"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    landing_path = os.path.join(static_dir, 'landing.html')
    
    # 优先返回landing.html
    if os.path.exists(landing_path):
        return FileResponse(landing_path)
    
    # Fallback到index.html
    index_path = os.path.join(static_dir, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # 否则返回API信息
    return {"message": "AI Resume & Cover Letter Generator API is running"}


@app.get("/app")
async def app_page():
    """应用页面 - 返回主应用界面"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    index_path = os.path.join(static_dir, 'index.html')
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    raise HTTPException(status_code=404, detail="App page not found")


@app.get("/share")
async def share_page():
    """分享页面"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    share_path = os.path.join(static_dir, 'share.html')
    
    if os.path.exists(share_path):
        return FileResponse(share_path)
    
    raise HTTPException(status_code=404, detail="Share page not found")


@app.get("/api/health")
def health():
    """健康检查端点"""
    return {"message": "AI Resume & Cover Letter Generator API is running", "status": "healthy"}


# ==================== API端点 ====================

@app.post("/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    生成简历和求职信的主API端点（需要登录或使用免费次数）
    
    Args:
        request: 包含岗位描述和候选人背景的请求
        current_user: 当前登录用户（可选）
        
    Returns:
        包含简历和求职信的响应
    """
    try:
        # 验证输入
        if not request.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty")
        if not request.candidate_background.strip():
            raise HTTPException(status_code=400, detail="Candidate background cannot be empty")
        
        # 处理用户认证和次数检查
        user_email = None
        if current_user:
            # 已登录用户：检查剩余次数
            user_email = current_user.email
            if current_user.remaining_credits <= 0:
                raise HTTPException(
                    status_code=402,  # Payment Required
                    detail="Please upgrade to Pro to continue generating resumes"
                )
        else:
            # 未登录用户：创建临时用户，使用免费1次
            # 这里简化处理：未登录用户每次都需要提供邮箱
            # 实际应用中可以在前端先登录
            raise HTTPException(
                status_code=401,
                detail="Please login first. Use /login endpoint with your email"
            )
        
        # 检查API密钥
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="OPENAI_API_KEY environment variable is not set"
            )
        
        # 调用AI生成函数
        resume, cover_letter = await generate_resume_and_cover_letter(
            job_description=request.job_description,
            candidate_background=request.candidate_background,
            api_key=api_key
        )
        
        # 扣除用户次数
        if user_email:
            deduct_credit(user_email)
            user = get_user(user_email)
            remaining = user.remaining_credits if user else 0
        else:
            remaining = 0
        
        return GenerateResponse(
            resume=resume,
            cover_letter=cover_letter,
            success=True,
            remaining_credits=remaining
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating resume and cover letter: {str(e)}"
        )


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    用户登录（简化版：仅需邮箱）
    
    Args:
        request: 包含邮箱的登录请求
        
    Returns:
        登录响应，包含session_token和用户信息
    """
    try:
        email = request.email.lower().strip()
        
        # 创建或获取用户
        user = create_user(email)
        
        # 创建session
        session_token = create_session(email)
        
        return LoginResponse(
            success=True,
            session_token=session_token,
            email=user.email,
            remaining_credits=user.remaining_credits
        )
    
    except Exception as e:
        return LoginResponse(
            success=False,
            error=str(e)
        )


@app.get("/auth/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user: Optional[User] = Depends(get_current_user)):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前登录用户
        
    Returns:
        用户信息
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return UserInfoResponse(
        email=current_user.email,
        remaining_credits=current_user.remaining_credits,
        is_pro=current_user.is_pro
    )


@app.post("/create-checkout-session")
async def create_checkout(
    request: CheckoutRequest,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    创建Stripe支付会话
    
    Args:
        request: 包含成功和取消URL的请求
        current_user: 当前登录用户
        
    Returns:
        Stripe Checkout会话URL
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Please login first")
    
    # 检查Stripe配置
    stripe_secret = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_secret:
        raise HTTPException(
            status_code=500,
            detail="STRIPE_SECRET_KEY is not configured"
        )
    
    # 创建Checkout会话
    result = create_checkout_session(
        email=current_user.email,
        success_url=request.success_url,
        cancel_url=request.cancel_url
    )
    
    if not result.get('success'):
        raise HTTPException(
            status_code=500,
            detail=result.get('error', 'Failed to create checkout session')
        )
    
    return {
        "checkout_url": result['url'],
        "session_id": result['session_id']
    }


@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    """
    处理Stripe Webhook事件（支付成功等）
    
    注意：在生产环境中，需要配置Stripe Webhook URL指向此端点
    并使用stripe CLI进行本地测试：stripe listen --forward-to localhost:8000/stripe-webhook
    """
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(
            status_code=500,
            detail="STRIPE_WEBHOOK_SECRET is not configured. Please set it in backend/.env file and restart the server."
        )
    
    # 验证签名并解析事件
    event = verify_webhook_signature(payload, signature, webhook_secret)
    
    if not event:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
    # 处理不同类型的事件
    event_type = event.get('type')
    
    if event_type == 'checkout.session.completed':
        # 支付成功：给用户增加次数
        result = handle_payment_success(event)
        
        if result.get('success'):
            email = result['email']
            credits = result['credits']
            add_credits(email, credits)
            
            return {
                "status": "success",
                "message": f"Added {credits} credits to user {email}"
            }
        else:
            return {
                "status": "error",
                "message": result.get('error', 'Unknown error')
            }
    
    elif event_type == 'invoice.payment_succeeded':
        # 订阅续费成功：每月自动增加次数
        # 这里简化处理，实际应该从invoice中提取customer信息
        # 暂时返回成功，具体实现可根据需求完善
        return {"status": "success", "message": "Subscription renewed"}
    
    # 其他事件类型暂时忽略
    return {"status": "received", "event_type": event_type}


if __name__ == "__main__":
    import uvicorn
    # 支持Railway等平台的PORT环境变量
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
