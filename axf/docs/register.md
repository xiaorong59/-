####请求地址：/api/user/auth/register/

####请求方式：POST

####请求参数：
```
username 用户名 str 必填
password 密码 str 必填
password2 确认密码 str 必填
email 邮箱 str 必填
sex 性别 bool 
icon 头像 image
is_delete 是否删除 bool
```

####响应内容：

**成功响应**
```
{
    "code": 200,
    "msg": "请求成功",
    "data": {
        "user_id":1,
    }
}
```
**失败响应**

1.账户和密码和邮箱没填写
```
    "code":1002,
    "msg":"账号或密码信息错误，请确认注册信息",
    "data": {
        "error":{
            "username":[
                "账号必填"
            ],
            "password":[
                "密码必填"
            ],
            "password2":[
                "确认密码必填"
            ],
            "email":[
                "邮箱必填"
            ]
        }
    }
```
2.账号和密码和邮箱长度输入或格式不符合规范的情况
``` 
{
    "code":1002,
    "msg":"账号或密码或邮箱错误，请确认登录信息",
    "data":{
        "error":{
            "username":[
               "用户名不能超过4字符"
            ],
            "password":[
                "密码不能短于6字符"
            ],
            "password2":[
                "密码不能短于6字符"
            ],
            "email":[
                "邮箱格式不符合规范"
            ]
        }
    }
}
```
3.账号和密码的输入符合规范，账号已存在的情况和密码以及确认密码不一致的情况
``` 
{
    "code":1003,
    "msg":"注册账号已存在，请更换账号",
    "data":{}
}

{
    "code":1004,
    "msg":"注册密码和确认密码不一致",
    "data":{}
}

{
    "code":1005,
    "msg":"邮箱已注册"
    "data":{}
}
```
####响应参数：
``` 
user_id int 注册用户的ID值
```