/**
 * 前端JavaScript逻辑（付费MVP版本）
 * 处理登录、支付和表单提交
 */

// API配置
// 在生产环境中，使用相对路径；开发环境使用localhost
const API_BASE_URL = window.location.origin;
const API_URL = `${API_BASE_URL}/generate`;

// 全局状态
let sessionToken = localStorage.getItem('session_token') || null;
let currentUser = null;

// DOM元素
const form = document.getElementById('generateForm');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const errorMessage = document.getElementById('errorMessage');
const results = document.getElementById('results');
const resumeContent = document.getElementById('resumeContent');
const coverLetterContent = document.getElementById('coverLetterContent');
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const loginEmail = document.getElementById('loginEmail');
const userInfo = document.getElementById('userInfo');
const userEmailSpan = document.getElementById('userEmail');
const userCreditsSpan = document.getElementById('userCredits');
const logoutBtn = document.getElementById('logoutBtn');
const upgradePrompt = document.getElementById('upgradePrompt');
const upgradeBtn = document.getElementById('upgradeBtn');

/**
 * 初始化：检查登录状态
 */
async function init() {
    if (sessionToken) {
        await checkAuth();
    } else {
        showLoginModal();
    }
}

/**
 * 检查认证状态并获取用户信息
 */
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'X-Session-Token': sessionToken
            }
        });

        if (response.ok) {
            const user = await response.json();
            currentUser = user;
            updateUserUI(user);
            hideLoginModal();
        } else {
            // Token无效，清除并显示登录
            sessionToken = null;
            localStorage.removeItem('session_token');
            showLoginModal();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        showLoginModal();
    }
}

/**
 * 更新用户UI
 */
function updateUserUI(user) {
    userEmailSpan.textContent = user.email;
    userCreditsSpan.textContent = `${user.remaining_credits} credits`;
    userInfo.style.display = 'flex';
    
    // 如果次数为0，显示升级提示
    if (user.remaining_credits === 0) {
        upgradePrompt.style.display = 'block';
    } else {
        upgradePrompt.style.display = 'none';
    }
}

/**
 * 显示登录模态框
 */
function showLoginModal() {
    loginModal.style.display = 'flex';
}

/**
 * 隐藏登录模态框
 */
function hideLoginModal() {
    loginModal.style.display = 'none';
}

/**
 * 登录处理
 */
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = loginEmail.value.trim();
    if (!email) {
        showError('Please enter your email');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (data.success) {
            sessionToken = data.session_token;
            localStorage.setItem('session_token', sessionToken);
            currentUser = {
                email: data.email,
                remaining_credits: data.remaining_credits
            };
            updateUserUI(currentUser);
            hideLoginModal();
        } else {
            showError(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        let errorMsg = 'Failed to login. Please try again.';
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg = 'Cannot connect to the server. Please make sure the backend is running on http://localhost:8000';
        } else if (error.message) {
            errorMsg = `Login error: ${error.message}`;
        }
        showError(errorMsg);
    }
});

/**
 * 登出处理
 */
logoutBtn.addEventListener('click', () => {
    sessionToken = null;
    localStorage.removeItem('session_token');
    currentUser = null;
    userInfo.style.display = 'none';
    upgradePrompt.style.display = 'none';
    showLoginModal();
});

/**
 * 显示错误消息
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    results.style.display = 'none';
    
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

/**
 * 隐藏错误消息
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * 设置加载状态
 */
function setLoading(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * 显示生成结果
 */
function displayResults(resume, coverLetter, remainingCredits) {
    resumeContent.textContent = resume;
    coverLetterContent.textContent = coverLetter;
    results.style.display = 'block';
    
    // 更新剩余次数
    if (currentUser && remainingCredits !== undefined) {
        currentUser.remaining_credits = remainingCredits;
        updateUserUI(currentUser);
    }
    
    // 添加品牌标识（如果不存在）
    let brandAttribution = document.querySelector('.brand-attribution');
    if (!brandAttribution) {
        brandAttribution = document.createElement('div');
        brandAttribution.className = 'brand-attribution';
        brandAttribution.innerHTML = '<p>Generated by <a href="/" id="brandLink">ResumeAI</a> - Tailor your resume for every job</p>';
        results.appendChild(brandAttribution);
    }
    
    // 滚动到结果区域
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * 复制内容到剪贴板
 */
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            btn.style.background = '#4caf50';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '#667eea';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            showError('Failed to copy to clipboard');
        });
    } else {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            btn.style.background = '#4caf50';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '#667eea';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
            showError('Failed to copy to clipboard');
        }
        
        document.body.removeChild(textArea);
    }
}

/**
 * 创建支付会话
 */
async function createCheckoutSession() {
    if (!sessionToken) {
        showError('Please login first');
        return;
    }

    try {
        // 构建成功和取消URL（使用当前域名）
        const currentUrl = window.location.origin + '/app';
        const successUrl = `${currentUrl}?payment=success`;
        const cancelUrl = `${currentUrl}?payment=canceled`;

        const response = await fetch(`${API_BASE_URL}/create-checkout-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-Token': sessionToken
            },
            body: JSON.stringify({
                success_url: successUrl,
                cancel_url: cancelUrl
            })
        });

        const data = await response.json();

        if (data.checkout_url) {
            // 跳转到Stripe Checkout
            window.location.href = data.checkout_url;
        } else {
            showError('Failed to create checkout session');
        }
    } catch (error) {
        console.error('Checkout error:', error);
        showError('Failed to start checkout. Please try again.');
    }
}

/**
 * 升级按钮点击事件
 */
upgradeBtn.addEventListener('click', createCheckoutSession);

/**
 * 处理表单提交
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // 检查是否已登录
    if (!sessionToken) {
        showError('Please login first');
        showLoginModal();
        return;
    }
    
    // 隐藏之前的错误和结果
    hideError();
    results.style.display = 'none';
    
    // 获取表单数据
    const jobDescription = document.getElementById('jobDescription').value.trim();
    const candidateBackground = document.getElementById('candidateBackground').value.trim();
    
    // 验证输入
    if (!jobDescription) {
        showError('Please enter a job description');
        return;
    }
    
    if (!candidateBackground) {
        showError('Please enter candidate background information');
        return;
    }
    
    // 设置加载状态
    setLoading(true);
    
    try {
        // 调用后端API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-Token': sessionToken
            },
            body: JSON.stringify({
                job_description: jobDescription,
                candidate_background: candidateBackground
            })
        });
        
        // 检查响应状态
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const errorMsg = errorData.detail || `HTTP error! status: ${response.status}`;
            
            // 处理402 Payment Required错误
            if (response.status === 402) {
                upgradePrompt.style.display = 'block';
                showError('You have no credits remaining. Please upgrade to Pro.');
            } else if (response.status === 401) {
                showError('Please login first');
                showLoginModal();
            } else {
                throw new Error(errorMsg);
            }
            return;
        }
        
        // 解析响应数据
        const data = await response.json();
        
        if (data.success && data.resume && data.cover_letter) {
            // 显示结果
            displayResults(data.resume, data.cover_letter, data.remaining_credits);
        } else {
            throw new Error(data.error || 'Failed to generate resume and cover letter');
        }
        
    } catch (error) {
        console.error('Error:', error);
        
        let errorMsg = 'An error occurred while generating the resume and cover letter.';
        
        if (error.message && (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.message.includes('ERR_CONNECTION_REFUSED'))) {
            errorMsg = 'Cannot connect to the server. Please make sure the backend is running on http://localhost:8000. Check the browser console (F12) for more details.';
        } else if (error.message) {
            errorMsg = error.message;
        }
        
        showError(errorMsg);
    } finally {
        // 恢复按钮状态
        setLoading(false);
    }
});

/**
 * 检查URL参数（支付成功/取消）
 */
function checkPaymentStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const paymentStatus = urlParams.get('payment');
    
    if (paymentStatus === 'success') {
        // 支付成功，刷新用户信息
        setTimeout(() => {
            checkAuth();
            // 清除URL参数
            window.history.replaceState({}, document.title, window.location.pathname);
            alert('Payment successful! Your credits have been added. Please refresh the page.');
        }, 500);
    } else if (paymentStatus === 'canceled') {
        // 支付取消
        window.history.replaceState({}, document.title, window.location.pathname);
    }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    init();
    checkPaymentStatus();
});
