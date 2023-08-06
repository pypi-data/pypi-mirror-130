# 前置
1. 安装allure并配置好环境变量
2. 项目根目录新建 hooks.py 实现动态扩展函数
3. 编写测试文件代码
4. 执行测试

# 作用
graphql, restful 
HTTP/HTTPS 接口测试工具，需要编写代码

# example

```python
# testcase.py

from gruntest.grunner import Grunner
from gruntest.schemas import Config, TestStep, RequestSchema


class TestRunner(Grunner):
    config = Config(
        base_header={"Host": "49.232.203.244:1339"}
    )
    steps = [
        TestStep(
            name='百度',
            request=RequestSchema(
                url='http://www.httpbin.org/get',
                method='get',
                headers={"token": "123"},
                params={"limit": 5, "page": 1}
            ),
            extra={"code": "$.args.limit"}
        ),
        TestStep(
            name='百度',
            request=RequestSchema(
                url='http://www.httpbin.org/get',
                method='get',
                headers={"token": "123"},
                params={"limit": 5, "page": "${sum2('$code')}"}
            ),
            extra={"code": "$.args.limit"},
            expect={"$.code": "code"}
        )
    ]
```