"""
AI生成模块
使用OpenAI API生成简历和求职信
"""
from openai import OpenAI
import os
import asyncio


async def generate_resume_and_cover_letter(
    job_description: str,
    candidate_background: str,
    api_key: str,
    model: str = "gpt-4o-mini"
) -> tuple[str, str]:
    """
    使用OpenAI API生成简历和求职信
    
    Args:
        job_description: 岗位描述
        candidate_background: 候选人背景信息
        api_key: OpenAI API密钥
        model: 使用的模型名称，默认为gpt-4o-mini
        
    Returns:
        (resume, cover_letter) 元组
    """
    client = OpenAI(api_key=api_key)
    
    # 构造高质量的Prompt
    system_prompt = """You are a senior HR professional at a top Silicon Valley tech company with 15+ years of experience in talent acquisition and resume optimization. You excel at matching candidates to job requirements and crafting compelling, authentic career narratives.

Your expertise includes:
- Identifying key skills and experiences that align with job requirements
- Using the STAR method (Situation, Task, Action, Result) to highlight achievements
- Writing clear, impactful bullet points that demonstrate value
- Creating personalized cover letters that feel genuine and professional
- Avoiding generic phrases and clichés

Always focus on:
- Quantifiable achievements and concrete results
- Relevance to the specific job description
- Clear, professional language
- Authenticity and avoiding exaggeration"""

    user_prompt = f"""Please generate a tailored resume and cover letter for the following candidate based on the job description.

**Job Description:**
{job_description}

**Candidate Background:**
{candidate_background}

**Requirements:**

1. **Resume Section:**
   - Format as bullet points (not paragraphs)
   - Use the STAR method to highlight achievements
   - Focus on quantifiable results and impact
   - Tailor each point to match the job requirements
   - Organize into clear sections (e.g., Experience, Skills, Education)
   - Avoid generic phrases like "team player" or "hard worker"
   - Keep it concise and impactful

2. **Cover Letter Section:**
   - Write a professional, natural-sounding cover letter
   - Address why the candidate is a good fit for this specific role
   - Reference specific requirements from the job description
   - Show genuine interest and enthusiasm
   - Keep it concise (3-4 paragraphs)
   - Use a professional but warm tone
   - Avoid clichés and generic statements

**Output Format:**
Please provide your response in the following exact format:

===RESUME===
[Resume content here]

===COVER_LETTER===
[Cover letter content here]
===

Make sure to use the exact markers "===RESUME===" and "===COVER_LETTER===" to separate the two sections."""

    try:
        # 调用OpenAI API（使用run_in_executor避免阻塞事件循环）
        def _call_openai():
            return client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,  # 平衡创造性和准确性
                max_tokens=2000   # 足够生成完整内容
            )
        
        # 在线程池中执行同步API调用
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, _call_openai)
        
        # 提取生成的内容
        content = response.choices[0].message.content
        
        # 解析输出，分离简历和求职信
        if "===RESUME===" in content and "===COVER_LETTER===" in content:
            parts = content.split("===RESUME===")[1].split("===COVER_LETTER===")
            resume = parts[0].strip()
            cover_letter = parts[1].replace("===", "").strip()
        else:
            # 如果格式不符合预期，尝试其他解析方式
            # 或者直接返回整个内容，让前端处理
            if "RESUME" in content.upper() and "COVER" in content.upper():
                # 尝试按段落分割
                lines = content.split("\n")
                resume_lines = []
                cover_letter_lines = []
                in_resume = True
                
                for line in lines:
                    if "COVER" in line.upper() or "LETTER" in line.upper():
                        in_resume = False
                    if in_resume:
                        resume_lines.append(line)
                    else:
                        cover_letter_lines.append(line)
                
                resume = "\n".join(resume_lines).strip()
                cover_letter = "\n".join(cover_letter_lines).strip()
            else:
                # 如果无法解析，将内容分成两部分
                mid_point = len(content) // 2
                resume = content[:mid_point].strip()
                cover_letter = content[mid_point:].strip()
        
        return resume, cover_letter
    
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")
