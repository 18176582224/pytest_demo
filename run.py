import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
print(f"项目根目录: {BASE_DIR}")

# 路径定义
RESULTS = BASE_DIR / "reports" / "allure-results"    # 存放Allure原始测试JSON数据
REPORT_DIR = BASE_DIR / "reports" / "allure-report"  # 存放最终生成的静态HTML报告
ALLURE_PATH = r"D:\xuexiruanjian\Python\Python313\allure-2.46.1\bin\allure.bat"

def main():
    # 🔹 新增：自动提前创建所有需要的目录，避免目录不存在报错
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("执行测试，生成Allure原始结果数据...")
    # 🔹 核心修复：给pytest加上--alluredir参数，指定原始结果输出路径，同时加--clean-alluredir自动清空历史旧数据
    pytest_run = subprocess.run(
        [sys.executable, "-m", "pytest", f"--alluredir={str(RESULTS)}", "--clean-alluredir", "-vs"],
        cwd=BASE_DIR,
        shell=True
    )

    # 兼容pytest用例失败返回非0退出码的场景，不中断后续报告生成
    if pytest_run.returncode != 0:
        print(f"测试执行完成，退出码: {pytest_run.returncode}，继续生成报告。")

    print("生成可视化Allure报告...")
    subprocess.run(
        [ALLURE_PATH, "generate", str(RESULTS), "-o", str(REPORT_DIR), "--clean"],
        cwd=BASE_DIR,
        shell=True,
        check=True # 新增：如果allure generate执行失败直接抛出异常，方便定位问题
    )

    print("启动本地预览服务，自动打开报告...")
    # 🔹 替换allure open为allure serve，启动本地预览服务，和你之前控制台输出的启动服务逻辑完全匹配
    subprocess.run(
        [ALLURE_PATH, "serve", str(RESULTS)],
        cwd=BASE_DIR,
        shell=True
    )

if __name__ == "__main__":
    main()