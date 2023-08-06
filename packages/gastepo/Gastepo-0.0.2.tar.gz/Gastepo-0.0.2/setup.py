# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gastepo',
 'gastepo.Core',
 'gastepo.Core.Base',
 'gastepo.Core.Extend',
 'gastepo.Core.Server',
 'gastepo.Core.Util',
 'gastepo.QA',
 'gastepo.TestSuite',
 'gastepo.TestSuite.TestMain',
 'gastepo.TestSuite.TestMain.Runner',
 'gastepo.TestSuite.TestMain.Starter']

package_data = \
{'': ['*'],
 'gastepo': ['Config/*',
             'Output/*',
             'Output/Coverage/*',
             'Output/Log/*',
             'Output/Record/*',
             'Resource/*',
             'Resource/Allure/*',
             'Resource/Ding/*',
             'Resource/Others/*'],
 'gastepo.TestSuite': ['TestCase/*']}

install_requires = \
['Flask>=1.1.1,<2.0.0',
 'PyHamcrest>=2.0.2,<3.0.0',
 'PyMySQL>=0.9.3,<0.10.0',
 'PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy>=1.3.9,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'allure_pytest>=2.8.6,<3.0.0',
 'allure_python_commons>=2.8.6,<3.0.0',
 'colorlog>=4.0.2,<5.0.0',
 'emoji>=1.2.0,<2.0.0',
 'fastapi>=0.58.1,<0.59.0',
 'jenkins>=1.0.2,<2.0.0',
 'jsonpath>=0.82,<0.83',
 'openpyxl>=3.0.0,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pycryptodome>=3.9.7,<4.0.0',
 'pymongo>=3.9.0,<4.0.0',
 'pytest>=5.3.2,<6.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.22.0,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'rsa>=4.0,<5.0',
 'selenium>=3.141.0,<4.0.0',
 'uvicorn>=0.11.5,<0.12.0',
 'xlrd>=1.2.0,<2.0.0',
 'xlutils>=2.0.0,<3.0.0',
 'xlwt>=1.3.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['gastepo = gastepo.Cli:cli']}

setup_kwargs = {
    'name': 'gastepo',
    'version': '0.0.2',
    'description': 'An base-on Schema DSL automation framework of Restful API.',
    'long_description': '### Description\n\n> **框架简介：** Gastepo ~ 基于Schema DSL语法规约的接口自动化测试框架\n\n> **测试类型：** 接口自动化测试\n\n***\n\n### Feature\n\n* **开发语言**：*Python 3.7*\n* **开发环境**：*PyCharm*\n* **开发工具**：\n  * 测试框架：*Pytest*\n  * 测试报告：*Allure*\n  * 数据处理：*Pandas*\n  * 请求工具：*Requests*\n  * 响应获取：*JsonPath*\n  * 断言工具：*Hamcrest*\n  * 单元测试：*Unittest*、*Coverage*\n  * 代码扫描：*SonarQube*\n  * Web服务：*Flask*、*FastApi*\n  * 部署方式：*Docker*、*Jenkins*\n\n***\n\n### Framework\n\n<img src="https://i.loli.net/2021/04/26/qsx8IdGPyQKc5fp.png" alt="Framework.png" style="zoom:55%;" />\n\n***\n\n\n### Schema\n\n- *Dependency Schema*\n\n```json\n[\n    {\n        "GET /v3_0/userInfo/searchContactUsers": {\n            "to_path": {},\n            "to_header": {},\n            "to_param": {},\n            "to_data": {\n                "$[\'idCardNo\']": {\n                  \t"GET /v3_0/getCardId": {\n                      \t"response": {\n                          \t"data": "$.data.cardId"\n                        }\n                    }\n                }\n            }\n        }\n    }\n]\n```\n\n- *Assertion Schema*\n\n```json\n[\n    {\n        "actual": "$.data[:].cardId",\n        "expect": [\n          {\n            "${fetchCardId(user)}": {\n              "user": {\n                "GET /v3_0/getUserName": {\n                  \t"response": {\n                      \t"data": "$.userName"\n                    }\n                }\n              }\n            }\n          }\n        ],\n        "matcher": "has_item",\n        "alert": "未发现指定用户标签ID",\n        "multi": false\n    }\n]\n```\n\n***\n\n### Test Runner\n\n```ini\n[pytest]\naddopts = -s -q --alluredir=./Common/Static/Result/Allure --disable-warnings\ntestpaths = ./Executor/Mente\npython_files = *Runner.py\npython_classes = Test*\npython_functions = test*\n```\n\n- **Automation Runtime**\n    - *Step_1*：自动分析指定扫描文件夹中所有Postman接口集合并聚合生成表格用例文件。\n    - *Step_2*：自动化测试用例支持用例筛选及BDD方式执行，单条用例支持激活或禁用。\n    - *Step_3*：自动化测试用例使用Dependency Schema规约结构的接口请求数据依赖。\n    - *Step_4*：自动化测试用例使用Assertion Schema规约结构的接口信息高级断言。\n    - *Step_5*：自动化测试运行支持前置清空历史测试数据，包括测试结果、用例结果等。\n    - *Step_6*：自动化测试运行的所有接口通过dispatch路由分发，可自动识别请求信息并注入依赖数据。\n    - *Step_7*：自动化测试报告使用Allure，并支持表格用例自动更新、接口信息实时录制、报告实时截图。\n    - *Step_8*：自动化测试推送通知方式支持传统邮件推送和钉钉机器人消息提醒。\n    - *Step_9*：自动化测试部署方式支持Jenkins流水线及Docker容器托管运行方式。\n\n***\n\n### Test Reporter\n\n```shell\nallure generate {json测试结果目录} -o {html测试报告目录} --clean\n```\n\n- <u>**Allure Test Report**</u>\n\n![Gastepo](https://i0.hdslb.com/bfs/album/5d05d78fb0f38fd9954d7e350ace89fe564c44d0.png)\n\n***\n\n### Test Deployment\n\n- <u>**Docker Container**</u>\n\n```shell\ndocker run -itd --name gastepo -p 端口号 -v {配置文件映射卷} -v {数据文件映射卷} automation/gastepo\n```\n\n- <u>**Jenkins Pipeline**</u>\n\n```groovy\npipeline {\n    agent any\n    options {\n        可选项配置\n    }\n    stages {\n         stage("Pull From GitLab") {\n        \t\t拉取指定Git分支源码\n        }\n        stage("Set PATH") {\n            设置Python3依赖信息\n        }\n        stage("Run Test") {\n            执行自动化测试\n        }\n        stage("Generate Report") {\n            报告生成及结果推送\n    }\n    post {\n        success {\n            println "[Done]: Gastepo Test Done"\n        }\n    }\n}\n```\n\n***\n\n### Wiki:\n\nGet me on [GitHub](https://github.com/bleiler1234/gastepo)\n\n***\n\n### Measure\n\n[![警报](http://10.16.168.70:9005/api/project_badges/measure?project=TaslyAutoTest&metric=alert_status)](http://10.16.168.70:9005/dashboard?id=TaslyAutoTest)[![SQALE评级](http://10.16.168.70:9005/api/project_badges/measure?project=TaslyAutoTest&metric=sqale_rating)](http://10.16.168.70:9005/dashboard?id=TaslyAutoTest)[![覆盖率](http://10.16.168.70:9005/api/project_badges/measure?project=TaslyAutoTest&metric=coverage)](http://10.16.168.70:9005/dashboard?id=TaslyAutoTest)\n\n[^QA]: 583512498@qq.com\n\n',
    'author': 'yuzhonghua',
    'author_email': '583512498@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bleiler1234/Gastepo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
