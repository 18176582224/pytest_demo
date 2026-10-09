import pytest

class Query_list:
    query_all_list=[
        ("按电话号码查询",{"phone":"new_phone"}),
        ("按名字查询",{"namae":"name"}),
    ]

    @pytest.mark.parametrize(
        "desc,params",
        query_all_list,
        ids=[case[0] for case in query_all_list],
    )

    def clue_query(self,logged_in_client,desc,params):

        print(f"\n{desc}")
        response=logged_in_client.query_file(**params)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "查询成功"
        # 至少查到 1 条，rows 是课程列表
        assert len(data.get("rows", [])) > 0, f"{desc}：没有查到数据"  # 断言失败时才显示的错误消息，告诉你哪条用例挂了
        print(f"查到 {data.get('total')} 条")
