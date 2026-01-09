"""
AI翻译助手 - 后端API服务
使用 FastAPI 框架，调用 DeepSeek API 实现中英文翻译
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv("api.env")

app = FastAPI(
    title="AI翻译助手",
    description="一个基于大模型的中英文翻译API",
    version="1.0.0"
)

# 配置CORS，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslateRequest(BaseModel):
    """翻译请求模型"""
    text: str


class TranslateResponse(BaseModel):
    """翻译响应模型"""
    translation: str
    keywords: list[str]


# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")


async def call_deepseek_api(text: str) -> dict:
    """
    调用 DeepSeek API 进行翻译和关键词提取
    
    Args:
        text: 需要翻译的中文文本
        
    Returns:
        包含翻译结果和关键词的字典
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="未配置 DEEPSEEK_API_KEY，请在 .env 文件中设置"
        )
    
    # 构建提示词，让AI同时完成翻译和关键词提取
    prompt = f"""请将以下中文翻译成英文，并提取3个最重要的关键词。

中文内容：
{text}

请严格按照以下JSON格式返回结果（不要添加任何其他内容）：
{{"translation": "英文翻译结果", "keywords": ["关键词1", "关键词2", "关键词3"]}}
"""
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的翻译助手，擅长中英文翻译和关键词提取。请始终以有效的JSON格式返回结果。"
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,  # 较低的温度使输出更稳定
        "max_tokens": 1000
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 解析返回的JSON
            import json
            # 尝试清理可能的markdown代码块标记
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            parsed_result = json.loads(content)
            
            return {
                "translation": parsed_result.get("translation", ""),
                "keywords": parsed_result.get("keywords", [])[:3]  # 确保最多3个关键词
            }
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"DeepSeek API 调用失败: {e.response.text}"
            )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="AI返回的结果格式解析失败"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"翻译服务出错: {str(e)}"
            )


@app.get("/")
async def root():
    """健康检查接口"""
    return {"message": "AI翻译助手API运行中", "status": "ok"}


@app.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    翻译接口
    
    - **text**: 需要翻译的中文内容
    
    返回英文翻译结果和3个关键词
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="翻译内容不能为空")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="翻译内容过长，请限制在5000字以内")
    
    result = await call_deepseek_api(request.text)
    
    return TranslateResponse(
        translation=result["translation"],
        keywords=result["keywords"]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

