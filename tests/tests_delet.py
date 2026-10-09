import pytest
class TestCourseDelete:
    """删除课程 测试类。
    @pytest.mark.skip：告诉 pytest：“这个测试用例先别跑，跳过它
    reason = “ 这里写为什么不跑这个测试用例的原因 ”
    """
    # 先跳过：删除是不可逆操作，确认要执行时删掉下面这行 skip 即可
    @pytest.mark.skip(reason="删除操作不可逆，确认后再运行（删掉本行即可执行）")
    def test_delete_earliest_10_courses(self, logged_in_client):
        """从最早创建时间开始，删除 10 条课程。"""
        # 1) 查询所有课程（不传参数 = 查全部）
        list_response=logged_in_client.get_course_list()
        assert list_response.status_code == 200
        list_data = list_response.json()
        all_rows = list_data.get("rows",[])
        # 2) 只保留「有创建时间」的课程，并按创建时间升序排序（最早的在最前面）
        courses=[row for row in all_rows if row.get("createTime")]
        """"等价于
        courses = []
        for row in all_rows:
            if row.get("createTime")
                courses.append(row)/5
        """
        # (3) 只取最早的10条
        to_delete = courses[:10]
        print(f"\n一共{len(courses)}条有创建时间的课程，本次删除最早的{len(to_delete)}条")

        #（4）逐条删除

        deletd = 0
        for row in to_delete:
            course_id = row["id"]
            resp = logged_in_client.delete_course(course_id)
            assert resp.status_code == 200
            data = resp.json()
            assert data["code"] == 200,f"删除课程 id ={course_id}失败：{data.get("msg")}"
            print(f"已删除 id ={course_id} 创建时间{row["createTime"]}")
            deletd +=1

        print(f"成功删除{deletd}条课程")



































