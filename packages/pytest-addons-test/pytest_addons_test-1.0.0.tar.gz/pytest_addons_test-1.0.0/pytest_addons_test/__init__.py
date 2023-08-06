import pytest
import time
import logging


# 修改用例使用参数化时中文的名称问题
def pytest_collection_modifyitems(
        session, config, items
):
    for item in items:
        # 用例的名字
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        # 用例的路径
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')


@pytest.fixture(scope="session", autouse=True)
def manage_logs(request):
    """Set log file name same as test name"""
    now = time.strftime("%Y-%m-%d %H-%M-%S")
    log_name = './output/log/' + now + '.logs'

    request.config.pluginmanager.get_plugin("logging-plugin") \
        .set_log_path(log_name)


@pytest.fixture(scope="session")
def addon_logger():
    logging.basicConfig(level=logging.INFO,
                        # 日志格式
                        # 时间、代码所在文件名、代码行号、日志级别名字、日志信息
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        # 打印日志的时间
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        # 日志文件存放的目录（目录必须存在）及日志文件名
                        filename='report.log',
                        # 打开日志文件的方式
                        filemode='w'
                        )
    logger = logging.getLogger(__name__)
    return logger
