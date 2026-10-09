login_test_data_json=[
    {
        "id":"001",
        "description":"正确的用户名+正确的密码+正确的验证码，登陆成功",
        "username":"admin",
        "code_type":"correct",
        "password":"HM_2023_test",
        "expected_code":200,
        "expected_msg":"操作成功",
        "check_token":True
    },
    {
        "id":"002",
        "description":"空的用户名+正确的密码+正确的验证码，登陆失败",
        "username":"",
        "code_type":"correct",
        "password":"HM_2023_test",
        "expected_code":500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
     },
    {
        "id":"003",
        "description":"正确的用户名+正确的密码+空的验证码，登陆失败",
        "username":"admin",
        "code_type":"",
        "password":"HM_2023_test",
        "expected_code":500,
        "expected_msg":"验证码错误",
        "check_token":False
    },
    {
        "id":"004",
        "description":"正确的用户名+错误的密码+正确的验证码，登陆失败",
        "username":"admin",
        "code_type":"correct",
        "password":"HM_2023",
        "expected_code":500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    },
    {
        "id":"005",
        "description":"正确的用户名+正确的密码+错误的验证码，登陆失败",
        "username":"admin",
        "code_type":"wrong",
        "password":"HM_2023_test",
        "expected_code":500,
        "expected_msg":"验证码错误",
        "check_token":False
    },
{
        "id":"006",
        "description":"错误的用户名+正确的密码+正确的验证码，登陆失败",
        "username":"admining",
        "code_type":"correct",
        "password":"HM_2023_test",
        "expected_code":500,
        "expected_msg":"用户不存在/密码错误",
        "check_token":False
    }
]






























