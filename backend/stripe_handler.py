"""
Stripe支付处理模块
使用Stripe Checkout处理支付
"""
import os
import stripe
from typing import Optional

# 注意：环境变量应该在main.py中加载，这里不重复加载
# 但为了安全，在函数调用时再次检查

# 产品配置（可配置化）
PRODUCT_NAME = "Resume Pro"
PRODUCT_PRICE = 990  # $9.90，单位：分（cents）
PRODUCT_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")  # 如果已创建Price，可以设置ID
CREDITS_PER_MONTH = 100  # Pro用户每月100次


def create_checkout_session(email: str, success_url: str, cancel_url: str) -> dict:
    """
    创建Stripe Checkout会话
    
    Args:
        email: 用户邮箱
        success_url: 支付成功后的跳转URL
        cancel_url: 取消支付后的跳转URL
        
    Returns:
        checkout session对象
    """
    # 确保Stripe API密钥已设置
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_secret_key:
        return {
            'error': 'STRIPE_SECRET_KEY is not configured. Please set it in backend/.env file and restart the server.',
            'success': False
        }
    
    # 设置API密钥（每次调用时设置，确保使用最新值）
    stripe.api_key = stripe_secret_key
    
    try:
        # 如果没有设置Price ID，使用内联价格
        line_items = []
        
        if PRODUCT_PRICE_ID:
            # 使用已创建的Price ID
            line_items.append({
                'price': PRODUCT_PRICE_ID,
                'quantity': 1,
            })
        else:
            # 使用内联价格（临时创建）
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': PRODUCT_NAME,
                        'description': f'{CREDITS_PER_MONTH} resume generations per month',
                    },
                    'unit_amount': PRODUCT_PRICE,  # $9.90
                    'recurring': {
                        'interval': 'month',  # 月度订阅
                    },
                },
                'quantity': 1,
            })
        
        # 创建Checkout Session
        session = stripe.checkout.Session.create(
            customer_email=email,  # 预填用户邮箱
            payment_method_types=['card'],
            line_items=line_items,
            mode='subscription',  # 订阅模式
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'user_email': email,  # 在metadata中保存用户邮箱，用于webhook
            },
            # 允许用户在支付页面修改邮箱
            allow_promotion_codes=True,
        )
        
        return {
            'session_id': session.id,
            'url': session.url,
            'success': True
        }
    
    except stripe.error.StripeError as e:
        # 返回详细的错误信息
        error_msg = f"Stripe API error: {str(e)}"
        if hasattr(e, 'user_message'):
            error_msg += f" - {e.user_message}"
        return {
            'error': error_msg,
            'success': False
        }
    except Exception as e:
        # 捕获其他异常
        return {
            'error': f"Unexpected error: {str(e)}",
            'success': False
        }


def verify_webhook_signature(payload: bytes, signature: str, webhook_secret: str) -> Optional[dict]:
    """
    验证Stripe Webhook签名
    
    Args:
        payload: 请求体（bytes）
        signature: Stripe签名头
        webhook_secret: Webhook密钥
        
    Returns:
        解析后的事件数据或None
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, webhook_secret
        )
        return event
    except ValueError as e:
        # 无效的payload
        return None
    except stripe.error.SignatureVerificationError as e:
        # 签名验证失败
        return None


def handle_payment_success(event_data: dict) -> dict:
    """
    处理支付成功事件
    
    Args:
        event_data: Stripe事件数据
        
    Returns:
        处理结果
    """
    try:
        # 从事件中提取用户邮箱
        session = event_data.get('data', {}).get('object', {})
        customer_email = session.get('customer_details', {}).get('email')
        
        # 如果session中没有邮箱，尝试从metadata获取
        if not customer_email:
            customer_email = session.get('metadata', {}).get('user_email')
        
        # 如果还是没有，尝试从customer对象获取
        if not customer_email and session.get('customer'):
            try:
                customer = stripe.Customer.retrieve(session['customer'])
                customer_email = customer.get('email')
            except:
                pass
        
        if not customer_email:
            return {
                'success': False,
                'error': 'Could not find customer email in event data'
            }
        
        return {
            'success': True,
            'email': customer_email,
            'credits': CREDITS_PER_MONTH
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
