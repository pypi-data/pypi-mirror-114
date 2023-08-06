# sanic_rest_framework 框架文档

### 概述

​	sanic_rest_framework 是基于 Sanic 与 TortoiseORM 实现的 RestAPI 快速开发框架，实现原理参考于Django_rest_framework,

内部接口及对应的函数也与DRF大同小异，熟悉DRF者可以快速上手

```sequence
Title: SRF处理数据的基础流程
User->Web Server: 用户发起请求
Web Server->View: 异步处理请求
View->View: 通过`dispatch`分发请求并处理
View->serializers: 传入待验证的数据进行处理
serializers->View: 传出验证结果及处理后的数据
View->Web Server: 处理数据curd
Web Server->User: 输出 Json Or Raw 

```

### 最小样例

①、安装sanic_rest_framework 

`pip install sanic`

`pip install tortoise-orm`

`pip install sanic_rest_framework `



②、运行如下代码

##### Model.py

```python
from tortoise import Model, fields

class UserModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)

    def __str__(self):
        return f"User {self.id}: {self.name}"
```

##### Main.py

```python
import logging

from models import UserModel
from sanic import Sanic, response
from sanic_rest_framework.request import SRFRequest
from sanic_rest_framework.routes import ViewSetRouter
from sanic_rest_framework.serializers import ModelSerializer
from sanic_rest_framework.views import ModelViewSet
from tortoise import Model, fields
from tortoise.contrib.sanic import register_tortoise

logging.basicConfig(level=logging.DEBUG)
app = Sanic(__name__, request_class=SRFRequest)


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        read_only_fields = ('id')


class TestView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel
    search_fields = ('@question',)


route = ViewSetRouter()
route.register(TestView, '/TestView', 'test', True)
for i in route.urls:
    i.pop('is_base')
    app.add_route(**i)

register_tortoise(
    app, db_url="sqlite://:memory:", modules={"models": ['models']}, generate_schemas=True
)

if __name__ == "__main__":
    app.run(port=5000)

```

##### 访问 http://127.0.0.1:5000/TestView 即可看到运行结果 可以使用 PostMan 发起Post等请求

```json
// 结果如下
{
    "data": {
        "count": 0,
        "next": null,
        "next_page_num": null,
        "previous": null,
        "previous_num": 0,
        "results": []
    },
    "message": "Success",
    "status": 1
}
```
 
 