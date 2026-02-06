"""
用户认证模块（内存存储版本）
简化版用户系统，使用字典存储用户数据
生产环境可轻松切换到Supabase或数据库
"""
from typing import Dict, Optional
from datetime import datetime
import secrets

# 内存存储：email -> user_data
# 生产环境建议切换到数据库
users_db: Dict[str, dict] = {}

# Session存储：session_token -> email
# 用于验证用户登录状态
sessions: Dict[str, str] = {}


class User:
    """用户数据模型"""
    def __init__(self, email: str, remaining_credits: int = 1, is_pro: bool = False, 
                 created_at: Optional[str] = None, last_login: Optional[str] = None):
        self.email = email
        self.remaining_credits = remaining_credits
        self.is_pro = is_pro
        # 如果提供了时间戳则使用，否则使用当前时间
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.last_login = last_login if last_login else datetime.now().isoformat()


def create_user(email: str) -> User:
    """
    创建新用户（免费用户，默认1次）
    
    Args:
        email: 用户邮箱
        
    Returns:
        User对象
    """
    if email in users_db:
        # 用户已存在，更新最后登录时间
        users_db[email]['last_login'] = datetime.now().isoformat()
        return User(**users_db[email])
    
    # 创建新用户
    user = User(email=email, remaining_credits=1, is_pro=False)
    users_db[email] = {
        'email': user.email,
        'remaining_credits': user.remaining_credits,
        'is_pro': user.is_pro,
        'created_at': user.created_at,
        'last_login': user.last_login
    }
    return user


def get_user(email: str) -> Optional[User]:
    """
    获取用户信息
    
    Args:
        email: 用户邮箱
        
    Returns:
        User对象或None
    """
    if email not in users_db:
        return None
    return User(**users_db[email])


def update_user_credits(email: str, credits: int):
    """
    更新用户剩余次数
    
    Args:
        email: 用户邮箱
        credits: 新的剩余次数
    """
    if email in users_db:
        users_db[email]['remaining_credits'] = credits
        if credits >= 100:  # Pro用户
            users_db[email]['is_pro'] = True


def deduct_credit(email: str) -> bool:
    """
    扣除用户1次使用次数
    
    Args:
        email: 用户邮箱
        
    Returns:
        True: 扣除成功，False: 次数不足
    """
    if email not in users_db:
        return False
    
    if users_db[email]['remaining_credits'] <= 0:
        return False
    
    users_db[email]['remaining_credits'] -= 1
    return True


def add_credits(email: str, amount: int):
    """
    给用户增加使用次数（支付成功后调用）
    
    Args:
        email: 用户邮箱
        amount: 增加的次数（Pro用户每月100次）
    """
    if email not in users_db:
        # 如果用户不存在，创建用户
        create_user(email)
    
    current_credits = users_db[email]['remaining_credits']
    users_db[email]['remaining_credits'] = current_credits + amount
    users_db[email]['is_pro'] = True  # 标记为Pro用户


def create_session(email: str) -> str:
    """
    创建用户会话token
    
    Args:
        email: 用户邮箱
        
    Returns:
        session_token
    """
    token = secrets.token_urlsafe(32)
    sessions[token] = email
    return token


def get_email_from_session(token: str) -> Optional[str]:
    """
    从session token获取用户邮箱
    
    Args:
        token: session token
        
    Returns:
        用户邮箱或None
    """
    return sessions.get(token)


def delete_session(token: str):
    """
    删除会话（登出）
    
    Args:
        token: session token
    """
    if token in sessions:
        del sessions[token]


# 辅助函数：用于调试和测试
def get_all_users():
    """获取所有用户（仅用于调试）"""
    return users_db.copy()


def reset_user_credits(email: str, credits: int = 1):
    """重置用户次数（用于测试）"""
    if email in users_db:
        users_db[email]['remaining_credits'] = credits
