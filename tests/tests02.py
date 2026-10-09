import pytest
from src.testsqingqiu import Apiclient

class Testlogin:    #注意：类名以 Test 开头，pytest 才会把它识别成测试类。
    valid_username="admin"   #在构造函数里定义了两个实例属性（变量），分别赋值为登录用的账号和密码。
    valid_password="HM_2023_test"

    # 夹具fixture 用来「准备测试前需要的东西」，测试方法通过参数名来引用它。
    @pytest.fixture(scope="function")  # scope='function'：每个测试方法执行前都会重新运行一次
    def client(self):
        """"
        夹具1：准备一个Aipclient客户端对象
        yield之前是[测试前的准备]，yield之后是[测试之后的清理]
        """
        client=Apiclient()  # 准备：创建客户端（内部会自动建立 Session）
        yield client    # 把 client 交给测试方法使用
        client.close()   # 清理：测试结束后关闭会话

    @pytest.fixture(scope="function")
    def captch_info(self,client):
        response=client.get_captcha()    # 调接口拿验证码
        assert response.status_code == 200  #断言返回的code是200
        data = response.json()        #把响应体解析成字典
        return {"uuid":data["uuid"]}       #只把uuid返回给用例

    def test_login(self,client:Apiclient,captch_info:dict):
        username = "admin"
        password = "HM_2023_test"
        uuid = captch_info["uuid"]         # 从夹具拿到验证码唯一标识
        response = client.login(username=username,password=password,code="2",uuid=uuid)
        data = response.json()
        # ---- 开始断言：检查结果是否符合预期 ----
        assert response.json()
        assert data["code"]==200   #业务响应码是200（操作成功）
        assert "token" in data    #返回的内容包含token
        assert data["token"] is not None and data["token"] != ""  #断言token不为空
        print(f"登陆成功,token:{data['token']}")























