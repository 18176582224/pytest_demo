import pytest
from data.course_data import ADD_COURSE_TEST_DATA,QUERY_COURSE_TEST_DATA

class TestCourseADD:
    @pytest.mark.parametrize("test_case",ADD_COURSE_TEST_DATA)
    def test_add_course_data_driven(self, logged_in_client, test_case):
        """""
        新增课程用例
        参数（都由pytest自动注入）
        logged_in_client:conftest.py里定义好的【已经登录客户端】夹具
        test_case  : 一个空字典（pytest会把data.course_data引用的数据都加入到这个字典里面）
        """
        #==========第一步：从测试数据里取字段=============
        test_id=test_case["id"]
        description = test_case["description"]
        course = test_case["course"]
        experience = test_case["experience"]
        check_exists= test_case["check_exists"]


        print("="*50)
        print(f"执行测试用例：{test_id}-{description}")
        print(f"请求参数：{course}")


        #==================第二步：发送新增课程请求=========================
        #注意：数据里的applicableperson字段没有下划线
        #但是接口参数applicable_person有下划线，这是做了映射
        response = logged_in_client.add_course(
            name=course["name"],
            subject=course["subject"],
            price=course["price"],
            applicable_person = course["applicableperson"],
            info = course.get("info")    #info是可选字段，用get取，缺省给空字符串
        )


        #================第三步：验证响应==============
        assert response.status_code ==200
        data = response.json()
        print(f"响应数据{data}")

        #断言业务状态码和提示信息和期望一致
        assert data["code"] == experience["code"],\
            f"用例{test_id}失败：期望 msg={experience['msg']},实际code={data['code']}"

        if "msg" in experience:  #期望里写了msg才效验
            assert data["msg"] == experience["msg"],\
                f"用例{test_id}失败：期望msg={experience['msg']}，实际msg={data['msg']}"

        print(f"断言通过：code={data['code']},msg={data['msg']}")


    #=====================第四步：如果需要，验证课程是否真的成功======================
        if check_exists and  experience["code"] == 200:
            # 用课程名称去查列表，确认能查到刚添加的课程
            list_response =logged_in_client.get_course_list(name=course["name"])
            list_data= list_response.json()
            assert list_data["code"] == 200 #查询接口业务成功
            # 列表接口返回 {"total":N, "rows":[...]}，rows 是课程数组
            assert len(list_data.get("rows",[]))>0,\
                f"课程{course['name']}未在列表中找到"

            #验证查到的第一条课程信息是否正确
            found_course  = list_data["rows"][0]
            assert found_course["name"]==course["name"],\
                f"课程名称不匹配：{found_course['name']} != {course['name']}"
            assert found_course["price"] == course["price"], \
                f"课程价格不匹配：{found_course['price']} != {course['price']}"

            course_id = found_course["id"]
            print(f"验证通过：课程已存在，ID={course_id}")
        print(f"用例{test_id}通过")






























