# sdk

## 实现sdk调用中mqtt,http,rpc

## 如何写sdk调用其他服务http接口


要写A服务的sdk，A服务提供了1个http接口login，确定参数，在方法中实现具体的调用，如调用地址，使用post/get/put/patch等，最后返回结果
```
ret = SdkInterface.login(username="admin", password="c93ccd78b2076528346216b3b2f701e6", http_api_version="4.7.1")
```
要写A服务的sdk，A服务提供了1个rpc接口，确定参数，在方法中实现具体的调用，如调用地址，console服务名，最后返回结果

```
SdkInterface.query_check(data=param)

```
要写A服务的sdk，A服务需要一个topic，定义topic数据结构,
```
ret2 = SdkInterface.check(param=param)
```

订阅A服务topic,  定义回调函数，在回调函数中处理数据
```
SdkInterface.test_subscribe(lambda client, userdata, msg: print(msg.payload))
```

## 包制作
https://zhuanlan.zhihu.com/p/79164800
- python3.9 -m pip install --user --upgrade setuptools wheel twine
- python3.9 setup.py sdist bdist_wheel
- python3.9 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
