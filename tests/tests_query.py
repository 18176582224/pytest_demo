"""
============================
调用「查询课程」接口，
  1. 单条件查询：一次只传一个查询条件
  2. 多条件查询：一次同时传多个条件（多个条件之间是「并且」AND 的关系）

查询接口：GET /api/clues/course/list
查询参数（都可选）：name、subject、price、applicable_person、info
"""
import pytest


class TestCourseQuery:
    """查询课程 测试类。"""

    # ==================== 单条件查询 ====================
    # 每个元组是：(用例描述, 查询参数字典)
    single_query_cases = [
        ("按课程名称查询", {"name": "自动化测试实战课"}),
        ("按课程学科查询", {"subject": "6"}),
        ("按适用人群查询", {"applicable_person": "2"}),
        ("按课程价格查询", {"price": 900}),
    ]

    # ids 用来给每条用例起个可读的名字，否则 pytest 会显示成 desc0/desc1 这种
    # "desc, params" 这是一个字符串，里面用逗号分隔了参数名。意思是：single_query_cases
    # 里的每条数据（应该是个元组或列表）会被拆成两部分，分别赋值给desc和params这两个变量，传给下面的测试函数
    @pytest.mark.parametrize(
        "desc, params",   # 告诉 pytest：我要传入两个参数，分别叫 desc 和 params
        single_query_cases,  # 一个列表/元组的集合，里面存放着所有测试数据
        ids=[case[0] for case in single_query_cases],   #  用每条数据的第0个元素作为测试用例名
    )
    def test_query_single_condition(self, logged_in_client, desc, params):
        """单条件查询：一次只传一个查询条件。"""
        print(f"\n {desc}")#打印用例描述

        # **params   ** 两个星号：用来解包字典（按关键字传参）
        #  比如：**dict={"id":"999"} 里面的数据会变成dict={id = “999”}
        response = logged_in_client.get_course_list(**params)
        # ---- 断言 ----
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "查询成功"
        # 至少查到 1 条，rows 是课程列表
        assert len(data.get("rows", [])) > 0, f"{desc}：没有查到数据"  #断言失败时才显示的错误消息，告诉你哪条用例挂了
        print(f"查到 {data.get('total')} 条")

    # ==================== 多条件查询 ====================
    multi_query_cases = [
        ("学科+适用人群", {"subject": "6", "applicable_person": "2"}),
        ("学科+价格", {"subject": "6", "price": 900}),
        ("名称+学科", {"name": "自动化测试实战课", "subject": "6"}),
        ("适用人群+价格", {"applicable_person": "2", "price": 900}),
    ]

    @pytest.mark.parametrize(
        "desc, params",
        multi_query_cases,
        ids=[case[0] for case in multi_query_cases],
    )
    def test_query_multi_condition(self, logged_in_client, desc, params):
        """多条件查询：一次同时传多个条件。

        多个条件之间是「并且」（AND）关系：要同时满足所有条件，才会被查出来。
        比如 {"subject":"6", "price":900} 表示「学科是 6 且 价格是 900」。
        """
        print(f"\n {desc}")

        response = logged_in_client.get_course_list(**params)

        # ---- 断言 ----
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "查询成功"
        assert len(data.get("rows", [])) > 0, f"{desc}  ：没有查到数据"
        print(f" 查到 {data.get('total')} 条")
