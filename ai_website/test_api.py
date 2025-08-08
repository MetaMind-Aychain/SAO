#!/usr/bin/env python3
import requests
import json
import time

def test_api():
    base_url = "http://localhost:8001"
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(3)
    
    # 测试各个API端点
    endpoints = [
        "/api/dynamics",
        "/api/developer/updates", 
        "/api/stats",
        "/api/ai/status"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n=== 测试 {endpoint} ===")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"返回数据数量: {len(data)}")
                    if data:
                        print(f"第一条数据: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
                    else:
                        print("数据为空")
                else:
                    print(f"返回数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                print(f"错误: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到服务器 {endpoint}")
        except Exception as e:
            print(f"❌ 测试 {endpoint} 时出错: {e}")

if __name__ == "__main__":
    test_api()