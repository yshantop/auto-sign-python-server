from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "http://sxsx.jxeduyun.com:7779"

# 模型定义
class LoginData(BaseModel):
    loginAccount: str
    password: str
    rememberMe: bool = True
    loginUserType: str = "student"
    enrollmentYear: str = "2025"

class SignData(BaseModel):
    autonomyId: str
    userId: str
    nickName: str
    clockAddress: str
    fileId: str
    clockTime: str
    clockType: str
    clockContent: str = ""

# 登录接口
@app.post("/api/login")
async def login(data: LoginData):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://sxsx.jxeduyun.com:7779",
            "Referer": "http://sxsx.jxeduyun.com:7779/web/login",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(
            f"{BASE_URL}/portal-api/login",
            headers=headers,
            json=data.dict()
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 退出登录接口
@app.post("/api/logout")
async def logout(token: str):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Global-Year-Head": "2025",
            "Origin": "http://sxsx.jxeduyun.com:7779",
            "Referer": "http://sxsx.jxeduyun.com:7779/web/index",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(
            f"{BASE_URL}/portal-api/logout",
            headers=headers
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取用户信息接口
@app.get("/api/user/info")
async def get_user_info(token: str):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Global-Year-Head": "2025",
            "Origin": "http://sxsx.jxeduyun.com:7779",
            "Referer": "http://sxsx.jxeduyun.com:7779/web/index",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.get(
            f"{BASE_URL}/portal-api/app/index/getStudentPlan",
            headers=headers
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 上传图片接口
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), token: str = Form(...)):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "com.ecom.renrentong",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        files = {
            'file': (file.filename, await file.read(), file.content_type)
        }
        
        response = requests.post(
            f"{BASE_URL}/portal-api/common/uploadFileUrl",
            headers=headers,
            files=files
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 签到接口
@app.post("/api/sign")
async def add_sign(data: SignData, token: str):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; 2407FRK8EC Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.71 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/36.307693)",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "com.ecom.renrentong",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origin": "http://sxsx.jxeduyun.com:7779",
            "referer": "http://sxsx.jxeduyun.com:7779/web/index",
            "Global-Year-Head": "2025"
        }
        
        response = requests.post(
            f"{BASE_URL}/portal-api/practice/autonomyClock/add",
            headers=headers,
            json=data.dict()
        )
        
        response_json = response.json()
        
        # 如果是token过期，返回401状态码
        if response_json.get('code') == 401:
            raise HTTPException(status_code=401, detail="登录已过期")
            
        return response_json
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# 获取打卡情况接口
@app.get("/api/sign/status")
async def get_sign_status(
    token: str,
    autonomyId: str,
    userId: str,
    queryDate: str,
    beginQueryDate: Optional[str] = None,
    endQueryDate: Optional[str] = None
):
    try:
        headers = {
            "Host": "sxsx.jxeduyun.com:7779",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; 2407FRK8EC Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.71 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/36.307693)",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "com.ecom.renrentong",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "request-timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Global-Year-Head": "2025"
        }
        
        params = {
            "autonomyId": autonomyId,
            "userId": userId,
            "queryDate": queryDate
        }
        
        if beginQueryDate:
            params["beginQueryDate"] = beginQueryDate
        if endQueryDate:
            params["endQueryDate"] = endQueryDate
            
        response = requests.get(
            f"{BASE_URL}/portal-api/practice/autonomyClock/getStuDailyClock",
            headers=headers,
            params=params
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
