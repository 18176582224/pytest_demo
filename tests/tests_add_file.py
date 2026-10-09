import pytest
from data.list_daa import add_list

class TestFileAdd:
    @pytest.mark.parametrize("test_case",add_list)
    def test_list_add(self,logged_in_client,test_case):
        name=test_case["name"]
        phone=test_case["phone"]
        channel=test_case["channel"]
        sex=test_case["sex"]
        age=test_case["age"]
        qq=test_case["qq"]
        weixin=test_case["weixin"]
        activityld=test_case["activityld"]

        response=logged_in_client.add_file(
            name=name,
            phone = phone,
            channel = channel,
            sex = sex,
            age = age,
            qq = qq,
            weixin = weixin,
            activityld = activityld
        )


        assert response.status_code == 200
        data = response.json()
        print(f"响应数据{data}")

        assert data["code"] == 200, f"操作失败：{data.get('msg')}"
        print("操作成功")

