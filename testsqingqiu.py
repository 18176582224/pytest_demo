import requests
class Apiclient(object):
    ''''
    AIPClient：对被测系统接口的统一封装。
    凡是「获取验证码、登录」等接口，都通过这个类来调用。
    好处：URL、请求头等公共信息只写一次，测试代码更简洁
    '''
    # 被测系统的根地址（所有接口地址都从这里拼接）
    base_url="https://kdtx-test.itheima.net"

    def __init__(self):
        self.session=requests.Session()   #创建一个“会话对象”，后续返回的token可以一直保存在session里面不会丢失，让后面的可以使用
        self.headers={
    "user-Agent":"Mozilla/5.0",
    "Content-Type":"application/json"
    }

    def get_captcha(self):
        """"
           获取验证码。
        返回：response（requests 的响应对象）
        响应体里主要有两个字段：
          - uuid：本次验证码的唯一标识（登录时要一起提交）
          - img
        """
        url=self.base_url + "/api/captchaImage"    #拼接完整链接
        response=self.session.get(url,headers=self.headers)
        return response


    def login(self,username,password,code,uuid):
        """""  登录接口
        参数：
        username: 用户名
        password: 密码
        code: 验证码（图片里看到的数字）
        uuid: 验证码唯一标识（来自get_captcha）

        返回：response（登录结果，成功时body里会带token）
        """
        url = self.base_url + "/api/login"
        data = {
            "username": username,
            "password": password,
            "code": code,
            "uuid": uuid
        }
        """"
        关键点：用json= 而不是data= 发送
        因为json = 会把字典自动转成json字符串;误用data= 会被当成表单提交，服务器无法识别
        """

        response = self.session.post(url,json=data,headers=self.headers)
        return response


    #获取登录接口产生的token
    def set_token(self,token):
        """"
        登陆成功后把token存起来，并放进请求头header里
        （相当于postman里往header传token）：Authorization: Bearer <token>
        后续所有需要登录的接口，请求头都会自动带上
        服务器看到请求头才知道你是谁
        """
        self.token=token  #存token
        self.headers["Authorization"]=f"Bearer {self.token}"   #把token放进请求头header里面

    #======================课程管理接口=============================
    def add_course(self,name,subject,price,applicable_person,info=""):
        """"
        新增课程（需要先登录）
        参数：
        name：课程名字
        subject ： 学科
        price  ： 价格
        applicable_person ：适用人群
        info  : 课程介绍
        """
        url = self.base_url + "/api/clues/course"
        data={
            "name":name,
            "subject":subject,
            "price":price,
            "applicable_person":applicable_person,
           " info":info
        }
        response=self.session.post(url,json=data,headers=self.headers)
        return response


    def get_course_list(self,name=None,subject=None,price=None,applicable_person=None,info=None):
        """""
        查询课程列表（需要先登录）
        所有参数都是可选的：传了就按条件过滤，不传就查全部
        """
        url=self.base_url +"/api/clues/course/list"
        #查询接口用GET，参数用 params 拼接在URL后面（像postman里在url后面传搜索的内容）
        params={}
        if name:     #如果传了名字，就按名字过滤
            params["name"]=name
        if subject:
            params["subject"]=subject
        if price is not None:
            params["price"]=price
        if applicable_person:
            params["applicable_person"]=applicable_person
        if info:
            params["info"]=info

        response = self.session.get(url,params=params,headers=self.headers)
        return response


    #根据课程id查询单条课程
    def get_course_by_id(self,course_id):
        #把课程id拼进url里面进行查询，比如/api/clues/course/id={{id999}}
        url = self.base_url+f"/api/clues/course/{course_id}"
        response = self.session.get(url,headers=self.headers)
        return response

    def updata_course(self,course_id="",name="",subject="",price=None,applicable_person="",info=""):
        """修改课程（需先登录）。

               参数：
                 course_id        : 课程 id（必填，指定要修改哪门课）
                 name             : 新的课程名称
                 subject          : 新的课程学科
                 price            : 新的课程价格
                 applicable_person: 新的适用人群
                 info             : 新的课程介绍
               """
        url = self.base_url+"/api/clues/course"
        data={
            "id": course_id,
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicable_person,
            "info": info,
        }
        response=self.session.put(url,json=data,headers=self.headers)
        return response


    def delet_course(self,course_id):
        """"
        删除课程
        通过参数course_id 去删除课程
        """
        url = self.base_url+ f'/api/clues/course/{course_id}'
        response = self.session.delete(url,headers=self.headers)
        return response


    #关闭会话，释放连接资源
    def close(self):
        self.session.close()




















