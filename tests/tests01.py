import requests

#==================第一步:发送请求头=============

url="http://kdtx-test.itheima.net/api/captchaImage"
response=requests.get(url)

#===================第二步：定义请求头=============
headers={
    "user-Agent":"Mozilla/5.0",    #模拟成浏览器访问浏览器
    "Content-Type":"application/json"
}

#============================第三步：发送请求===================
response=requests.get(url,headers=headers)


#===============第四步：查看请求结果===================
#查看状态码
print("="*50)
print("状态码",response.status_code)
print("响应头",response.headers)
print("响应内容：",response.text[:100])  #只显示前两百个字符
print("json数据",response.json())

#========================如果返回的是json，解析成字典===============
if response.status_code==200:
    try:
        data=response.json()
        print("json数据：",data)

        #从字典中提取需要的字段
        code=data.get("code")
        uuid=data.get("uuid")
        print(f"验证文字：{code}")
        print(f"唯一标识：{uuid}")

    except Exception as e:
        print("josn解析失败")
else:
    print(f"请求失败，状态码：{response.status_code}")


print("="*50)


#=============登录==============
login_url="http://kdtx-test.itheima.net/api/login"
#登录的参数
login_data={
    "username": "admin",
    "password": "HM_2023_test",
    "code": "2",
    "uuid": uuid
}
login_response=requests.post(login_url,json=login_data,headers=headers)

print("登陆状态",login_response.status_code)
print("登录的结果",login_response.json())


if login_response.status_code==200:
    login_result=login_response.json()
    if login_result.get("code")== 200:
        token = login_result.get("token")
        print(f"登陆成功:{token}")
    else:
        print(f"登陆失败",login_result.get('msg'))













