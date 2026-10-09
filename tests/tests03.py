import pytest
from data import test_login
from src.testsqingqiu import Apiclient

# 导入data文件下test_login里面的login_test_data_jso测试数据：一个列表，里面是一条条字典，每项代表一条用例
from data.test_login import login_test_data_json
"""
登录接口 —— 数据驱动测试
========================
数据驱动：把「测试数据」和「测试逻辑」拆开。
  - 测试数据：放在 data/test_login.py 的 LOGIN_TEST_DATA_JSON 里（列表，每项是一条用例）
  - 测试逻辑：本文件只写一份，用 pytest 的 @parametrize 把每条数据自动跑一遍

好处：新增一条用例，只需要在数据文件里加一个字典，不用改任何测试代码。
"""
class Test_login_data:
    correct_captcha=2     # 测试环境里「图片验证码code 的答案固定是 2（俗称万能验证码）。

    @pytest.fixture(scope="function")
    #"夹具1：准备一个「登录客户端」对象。
    def login_client(self):
        login_client=Apiclient()
        yield login_client
        login_client.close()

    @pytest.fixture(scope="function")
    def captcha_client(self,login_client):
        """夹具2：获取一个「新鲜」的验证码 uuid。

         注意：
           1) 依赖 login_client 夹具（见函数参数），pytest 会先把 login_client 准备好再传进来。
           2) 验证码是一次性的，每跑一条用例都要重新获取一个 uuid，所以也是 function 级别。
         """
        response=login_client.get_captcha()    #调用get_captcha接口获取验证码
        assert response.status_code==200    #断言HTTP连接成功,响应码为200
        data=response.json()          #把响应体内容（JSON 字符串）解析成字典
        return {"uuid":data["uuid"]}      #只把 uuid 返回给用例使用



    # @pytest.mark.parametrize：pytest 的「参数化」装饰器，作用是把多条数据喂给同一个测试函数。
    #   "test_case"          ：参数名，会传入下面测试函数的同名参数
    #   login_test_data_json ：数据来源（一个列表），列表里有几项，就会生成几条测试用例
    @pytest.mark.smoke
    @pytest.mark.parametrize("test_case",login_test_data_json)
    def test_login(self, login_client, captcha_client, test_case, ):
        """核心用例：一份代码，跑完数据文件里的所有场景。

                参数说明（都由 pytest 自动注入，不需要手动传）：
                  login_client  ：夹具1 提供的客户端对象
                  captcha_client：夹具2 提供的验证码信息（含 uuid）
                  test_case ：相当于一个列表，pytest 的 @pytest.mark.parametrize 装饰器会自动遍历数据源（login_test_data_json），
                            按你声明的名字 "test_case"，逐条把数据赋值给test_case
                """
        test_id=test_case["id"]
        description = test_case["description"]
        username= test_case["username"]
        password= test_case["password"]
        codec_type = test_case["code_type"]    #验证码类型 “correct”/"wrong"
        expected_code=test_case["expected_code"]  #期望的业务码：200=成功/500=失败
        """""
         #expected_msg用get()是因为有些用例没写这个字段，用get不会报错
         当字段不存在返回None
          check_token同理，并且给默认值False（没有token时不效验）
        """
        expected_msg= test_case.get("expected_msg")
        check_token = test_case.get("check_token",False)

         #变量 = 值1 if 条件 else 值2  翻译：如果条件成立，变量就等于值1；否则，变量就等于值2。
        code =self.correct_captcha if codec_type == "correct"  else 8888
        #uuid不在测试数据里，而是来自验证码夹具（每个用例重新获取一个）
        uuid = captcha_client["uuid"]

        # print(f"\nzhixingyongli")/

        print(f"\n执行用例：{test_id} - {description}")  # 打印当前执行哪条用例，方便观察
        response = login_client.login(
            username=username,
            password=password,
            uuid= uuid,
            code=code
        )
        assert response.status_code == 200
        data =response.json()
        # \（反斜杠）：表示续行符。因为这一行太长了，写不下，所以用 \ 告诉
        # Python：“我还没写完，下一行接着看。”如果不写 \，Python会报语法错误。
        assert  data["code"]==expected_code,\
            f"用例{test_id}失败：期望 code={expected_code},实际 code={data['code']}"

        if expected_msg:
            assert data["msg"]==expected_msg,\
                f"用例{test_id}失败 mag={expected_code},实际 code={[data['code']]}"

            if check_token:
                assert "token" in data
                assert data["token"]  is not None  and data["token"]!=""
                print(f"token:{check_token}")
            print(f"用例{test_id}通过！")














