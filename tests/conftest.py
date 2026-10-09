import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from src.testsqingqiu import   Apiclient

@pytest.fixture(scope="function")
def client():
    client=Apiclient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def captcha_info(client):
    #获取验证码和uuid
    response = client.get_captcha()
    assert response.status_code == 200
    data=response.json()
    # 返回验证码信息：
    #   code : 验证码答案，测试环境固定是 "2"
    #   uuid : 验证码唯一标识（登录时要一起提交）
    # 注意：接口返回的 data["code"] 是「业务状态码」200，不是验证码答案，别混用。
    return {
        "code":"2",
        "uuid":data["uuid"]
    }

@pytest.fixture(scope="function")
def logged_in_client(client,captcha_info):
    #"自动完成【拿验证码-登录】，返回一个已经登录好的客户端"
    code=captcha_info["code"]
    uuid=captcha_info["uuid"]

    # 登录（用系统内置的 admin 账号
    response = client.login(
        "admin","HM_2023_test",code,uuid
    )
    assert response.status_code==200
    data=response.json()
    # 2) 业务层成功；失败时断言会报错，并显示服务器返回的原因
    assert data["code"]==200,f"登陆失败：{data.get('msg')}"
    # 把登录返回的 token 存到客户端，后续请求会自动带上登录态
    client.set_token(data["token"])


    return client  #返回已登录的客户端

@pytest.fixture(scope="function")
def created_course_id(logged_in_client):
#创建一个课程，返回他的ID，拿来后续查询/删除/修改
    import time
    course_name=f"test课程{int(time.time())}"
    #新增课程
    response=logged_in_client.add_course(
        name=course_name,
        subject="6",
        price=888,
        applicable_person="2",
        info="由fixture创建的测试课程"
    )
    assert response.status_code==200
    data=response.json()
    assert data["code"]==200
    #按照课程名字进行查询，拿到新创建的课程ID
    list_response = logged_in_client.get_course_list(name=course_name)
    list_data=list_response.json()

    # 列表接口返回结构：{"total": N, "rows": [ {...}, {...} ]}
    if list_data.get("row")  and len(list_data.get("row")) >0:
        course_id = list_data.get("row")[0].get("id")   #获取第一条课程id
        print(f"\n创建测试课程成功，ID{course_id}")
        return course_id
    else:
        # 查不到就主动让用例失败，并给出明确提示
        pytest.fail("无法获取新建的课程id")


@pytest.fixture(scope="function")
def get_list_phone(logged_in_client):
#创建一个线索，返回他的phone，拿来后续查询
    import time
    new_phone=f"test手机号{int(time.time())}"
    #新增线索
    response=logged_in_client.add_file(
        name="老三",
        phone=new_phone,
        channel="0",
        sex="1",
        age="18",
        qq=None,
        weixin=None,
        activityld=None
    )
    assert response.status_code==200
    data=response.json()
    assert data["code"]==200
    #按照电话号码进行查询
    list_response = logged_in_client.query_file(phone=new_phone)
    list_data=list_response.json()

    # 列表接口返回结构：{"total": N, "rows": [ {...}, {...} ]}
    if list_data.get("row")  and len(list_data.get("row")) >0:
        file_phone = list_data.get("row").get("phone")
        print(f"\n查询失败{file_phone}")
        return file_phone
    else:
        # 查不到就主动让用例失败，并给出明确提示
        pytest.fail("查询新增失败")









