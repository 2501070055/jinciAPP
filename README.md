# jinciAPP
APP后端接口文件
# 锦词接口文档`API`

---

----

---

## TOKEN说明

`md5(秘钥|time.time())|time.time()`



### 例子

```python
import requests
import time
import hashlib

ctime = time.time()

key = '秘钥'
new_key = "%s|%s" % (key, ctime)

m = hashlib.md5()
m.update(bytes(new_key, encoding='utf-8'))
md5_key = m.hexdigest()
md5_key_key = "%s|%s" % (md5_key, ctime)
response = requests.get('API', headers={'auth-api': md5_key_key})
```

## 全局`CODE`

| status | Code |            描述            |
| :----: | :--: | :------------------------: |
|  404   | 404  | 您访问的内容不存在或被删除 |
|  400   | 400  |       参数格式不正确       |
|  405   | 405  |      表单请求方式错误      |
|  401   | 401  |           请登录           |
|  500   | 500  |   服务器正忙，请稍后重试   |

# 用户类`API`

## 用户注册`API`

- 请求`URL`(`POST`)

```http
/v1/users/user/api/register
```

- 请求参数

|   参数值   | 类型 | 描述 |
| :--------: | :--: | :--: |
|  `email`   | 必填 | 邮箱 |
| `password` | 必填 | 密码 |
| `nickname` | 必填 | 昵称 |

- 返回状态码`Status=201`

---

## 用户登录`API`

- 请求`URL`(`POST`)

```http
/v1/users/user/api/login
```

- 请求参数

|   参数值   | 类型 | 描述 |
| :--------: | :--: | :--: |
| `username` | 必填 | 邮箱 |
| `password` | 必填 | 密码 |

- 返回状态码`Status=201`

---

## 用户操作`API`(需要登录)

- 请求`URL`(`PUT,GET,DELETE,PATCH`)

```http
/v1/users/user/api/handle
```

1. `PUT`请求（用户登出）

- 返回状态码`Status=200`

2. `GET`请求(用户详细信息读取包括登录日志)

| 参数值  | 类型 |        描述         |
| :-----: | :--: | :-----------------: |
| `limit` | 选填 | 登录日志条数(默认3) |

- 返回实例(`Status=201`)

```json
{
    "user": {
        "uid": 1,
        "email": "2501070055@qq.com",
        "nickname": "ZRR",
        "last_login": "2021-08-14T01:20:50.924Z",
        "date_joined": "2021-08-04T13:21:43.032Z"
    },
    "user_info": {
        "username": "你好啊",
        "avatar": "http://localhost:8000/medias/avatar/20210807/20210807_103624.png",
        "email": "2501070055@qq.com",
        "signature": "个性",
        "sex": 1,
        "age": 10,
        "status": "隐身"
    },
    "user_login_records": {
        "user_login_records": [
            {
                "id": 32,
                "user_id": 1,
                "username": "你好啊",
                "ip": "127.0.0.1",
                "address": null,
                "source": "",
                "version": "",
                "created_at": "2021-08-14 01:20:50"
            },
            {
                "id": 31,
                "user_id": 1,
                "username": "你好啊",
                "ip": "127.0.0.1",
                "address": null,
                "source": "",
                "version": "",
                "created_at": "2021-08-13 15:46:27"
            },
            {
                "id": 26,
                "user_id": 1,
                "username": "你好啊",
                "ip": "127.0.0.1",
                "address": null,
                "source": "",
                "version": "",
                "created_at": "2021-08-13 12:13:58"
            }
        ]
    }
}
```

3. `DELETE`请求(用户注销)

- 请求参数

|   参数值    | 类型 | 描述 |
| :---------: | :--: | :--: |
| `is_active` | 选填 | 填0  |

- 返回状态码`Status=200`

4. `PATCH`请求(用户在线状态)

- 请求参数

|  参数值  | 类型 |            描述             |
| :------: | :--: | :-------------------------: |
| `status` | 选填 | 0表示在线，1表示隐身，默认0 |

- 返回状态码`Status=200`

---

## 用户详细信息更改`API`(需要登录)

- 请求`URL`(`POST`)

```http
/v1/users/user/api/detail
```

- 请求参数

|   参数值    | 类型 |           描述            |
| :---------: | :--: | :-----------------------: |
|    `age`    | 选填 |           年龄            |
|    `sex`    | 选填 | 性别，1为男，0为女，默认1 |
|  `avatar`   | 选填 |     头像（上传图片）      |
| `signature` | 选填 |         个性签名          |
| `username`  | 选填 |          用户名           |

- 返回状态码`Status=201`

---

## 用户关注与取消关注`API`(需要登录)

- 请求URL

```http
/v1/users/user/api/follow/<int:pk>
```

- `pk=uid`

- 关注返回`Status=201`，取消关注返回`Status=200`

----

## 用户关注列表`API`

- 请求`URL`(`GET`)

```http
/v1/users/user/api/attentionlist/<int:pk>
```

- `pk=uid`
- 返回实例(`Status=200`)

```json
{    "user": [        {            "id": 1,            "user_id": 7,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-07 03:37:14"        },        {            "id": 24,            "user_id": 9,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-14 03:13:59"        },        {            "id": 25,            "user_id": 10,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-14 03:15:16"        }    ]}{    "user_follow": [        {            "id": 1,            "user_id": 7,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-07 03:37:14"        },        {            "id": 24,            "user_id": 9,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-14 03:13:59"        },        {            "id": 25,            "user_id": 10,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-14 03:15:16"        }    ]}
```

---

## 粉丝列表`API`

- 请求`URL`(`GET`)

```http
/v1/users/user/api/fanslist/<int:pk>
```

- `pk=uid`
- 返回实例(`Status=200`)

```json
{    "user": [        {            "id": 1,            "user_id": 7,            "follow_id": 1,            "status": 1,            "follow_time": "2021-08-07 03:37:14"        }    ]}
```

---

## 获取用户详细信息`API`

- 请求`URL`(`GET`)

```http
/v1/users/user/api/userdetail/<int:pk>
```

- `pk=uid`
- 返回实例(`Status=200`)

```json
{    "user": {        "nickname": "ZRR",        "last_login": "2021-08-14T02:19:08.541Z",        "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",        "signature": "",        "sex": 1,        "age": 18    }}
```

---

# 板块主题类`API`

## 获取板块类`API`

- 请求`URL`(`GET`)

```http
/v1/plates/plate/api/plate/list
```

- 返回实例(`Status=200`)

```json
{    "plates": [        {            "id": 1,            "plate_title": "热门",            "plate_dp": null,            "created_at": "2021-08-07 14:20:35",            "updated_at": "2021-08-07 14:20:37",            "status": 1        },        {            "id": 2,            "plate_title": "诗词",            "plate_dp": null,            "created_at": "2021-08-07 14:20:59",            "updated_at": "2021-08-07 14:21:02",            "status": 1        },        {            "id": 3,            "plate_title": "治愈",            "plate_dp": null,            "created_at": "2021-08-07 14:41:07",            "updated_at": "2021-08-07 14:41:11",            "status": 1        },        {            "id": 4,            "plate_title": "生活",            "plate_dp": null,            "created_at": "2021-08-07 14:41:26",            "updated_at": "2021-08-07 14:41:28",            "status": 1        },        {            "id": 5,            "plate_title": "句子",            "plate_dp": null,            "created_at": "2021-08-07 14:41:44",            "updated_at": "2021-08-07 14:41:48",            "status": 1        },        {            "id": 6,            "plate_title": "语录",            "plate_dp": null,            "created_at": "2021-08-07 14:42:01",            "updated_at": "2021-08-07 14:42:03",            "status": 1        }    ]}
```

---

## 书写帖子`API`(需要登录)

- 请求`URL`(`POST`)

```http
/v1/plates/plate/api/dparticle
```

- 请求参数

|     参数值     | 类型 |           描述           |
| :------------: | :--: | :----------------------: |
|    `plate`     | 必填 |          板块ID          |
|  `post_title`  | 必填 |         帖子标题         |
| `post_content` | 必填 |         帖子内容         |
|    `label`     | 选填 | 标签，已英文半角符号分开 |

- 返回状态码`Status=201`

---

## 某一板块下帖子展示`API`

- 请求`URL`(`GET`)

```http
/v1/plates/plate/api/plate/article/list
```

- 请求参数

|    参数值     | 类型 |         描述         |
| :-----------: | :--: | :------------------: |
| `plate_title` | 必填 |       板块标题       |
| `post_title`  | 选填 | 模糊查询（文章标题） |
|    `page`     | 选填 |         页码         |
|    `limit`    | 选填 |      每一页大小      |

- 返回实例(`Status=200`)

```json
{    "data": {        "meta": {            "total_count": 11,            "page_count": 3,            "current_page": 1        },        "objects": [            {                "uid": 1,                "user": "ZRR",                "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",                "plate_title": "治愈",                "pid": 82,                "post_title": "文章标题1",                "post_content": "文章内容1",                "created_at": "2021-08-15T01:21:11.201Z",                "updated_at": "2021-08-15T01:21:11.201Z",                "labels": []            },            {                "uid": 1,                "user": "ZRR",                "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",                "plate_title": "治愈",                "pid": 81,                "post_title": "文章标题1",                "post_content": "文章内容1",                "created_at": "2021-08-15T01:18:14.803Z",                "updated_at": "2021-08-15T01:18:14.803Z",                "labels": [                    {                        "id": 72,                        "user_id": 1,                        "label_title": "标签11",                        "label_dp": null,                        "created_at": "2021-08-15 01:18:14",                        "updated_at": "2021-08-15 01:18:14",                        "status": 1                    },                    {                        "id": 73,                        "user_id": 1,                        "label_title": "标签21",                        "label_dp": null,                        "created_at": "2021-08-15 01:18:14",                        "updated_at": "2021-08-15 01:18:14",                        "status": 1                    }                ]            },            {                "uid": 1,                "user": "ZRR",                "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",                "plate_title": "治愈",                "pid": 80,                "post_title": "文章标题1",                "post_content": "文章内容1",                "created_at": "2021-08-15T01:17:20.730Z",                "updated_at": "2021-08-15T01:17:20.730Z",                "labels": [                    {                        "id": 70,                        "user_id": 1,                        "label_title": "标签11",                        "label_dp": null,                        "created_at": "2021-08-15 01:17:20",                        "updated_at": "2021-08-15 01:17:20",                        "status": 1                    },                    {                        "id": 71,                        "user_id": 1,                        "label_title": "标签21",                        "label_dp": null,                        "created_at": "2021-08-15 01:17:20",                        "updated_at": "2021-08-15 01:17:20",                        "status": 1                    }                ]            },            {                "uid": 1,                "user": "ZRR",                "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",                "plate_title": "治愈",                "pid": 79,                "post_title": "文章标题1",                "post_content": "文章内容1",                "created_at": "2021-08-15T01:16:41.179Z",                "updated_at": "2021-08-15T01:16:41.179Z",                "labels": [                    {                        "id": 68,                        "user_id": 1,                        "label_title": "标签11",                        "label_dp": null,                        "created_at": "2021-08-15 01:16:41",                        "updated_at": "2021-08-15 01:16:41",                        "status": 1                    },                    {                        "id": 69,                        "user_id": 1,                        "label_title": "标签21",                        "label_dp": null,                        "created_at": "2021-08-15 01:16:41",                        "updated_at": "2021-08-15 01:16:41",                        "status": 1                    }                ]            },            {                "uid": 1,                "user": "ZRR",                "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",                "plate_title": "治愈",                "pid": 78,                "post_title": "文章标题1",                "post_content": "文章内容1",                "created_at": "2021-08-15T01:16:03.923Z",                "updated_at": "2021-08-15T01:16:03.923Z",                "labels": [                    {                        "id": 66,                        "user_id": 1,                        "label_title": "标签11",                        "label_dp": null,                        "created_at": "2021-08-15 01:16:03",                        "updated_at": "2021-08-15 01:16:03",                        "status": 1                    },                    {                        "id": 67,                        "user_id": 1,                        "label_title": "标签21",                        "label_dp": null,                        "created_at": "2021-08-15 01:16:03",                        "updated_at": "2021-08-15 01:16:03",                        "status": 1                    }                ]            }        ]    }}
```

---

## 收藏与取消收藏帖子及帖子列表`API`(需要登录)

- 请求`URL`(`POST`,`GET`)

```http
/plates/plate/api/collect/article/en/<int:pk>
```

1. `POST`请求(收藏与取消收藏)

- `pk=pid`
- 返回(`Status=200`)取消收藏，返回(`Status=201`)收藏

2. `GET`请求(获取收藏列表)

- `pk=limit`(限制输出条数，默认5)
- 返回实例(`Status=200`)

```json
{    "collect_list": [        {            "id": 1,            "user_id": 1,            "post_id": 75,            "created_at": "2021-08-08 16:34:02",            "updated_at": "2021-08-08 16:34:04",            "status": 1        },        {            "id": 2,            "user_id": 1,            "post_id": 73,            "created_at": "2021-08-08 08:55:53",            "updated_at": "2021-08-08 08:55:53",            "status": 1        },        {            "id": 3,            "user_id": 1,            "post_id": 72,            "created_at": "2021-08-08 09:37:54",            "updated_at": "2021-08-08 09:37:54",            "status": 1        }    ]}
```

---

## 获取热门列表`API`

- 请求`URL`(`GET`)

```http
/v1/plates/plate/api/hot/article/<int:pk>
```

- `pk=limit`
- 返回实例(`Status=200`)

```json
{    "hot": [        {            "id": 1,            "title_id": 72,            "created_at": "2021-08-08 10:04:01",            "updated_at": "2021-08-08 10:04:01",            "status": 1        },        {            "id": 2,            "title_id": 73,            "created_at": "2021-08-08 10:04:25",            "updated_at": "2021-08-08 10:04:25",            "status": 1        },        {            "id": 3,            "title_id": 74,            "created_at": "2021-08-08 10:04:34",            "updated_at": "2021-08-08 10:04:34",            "status": 1        },        {            "id": 4,            "title_id": 75,            "created_at": "2021-08-08 10:04:41",            "updated_at": "2021-08-08 10:04:41",            "status": 1        }    ]}
```

---

## 通过`PID`获取帖子`API`

- 请求`URL`(`GET`)

```http
/v1/plates/plate/api/article/detail/<int:pk>
```

- `pk=pid`
- 返回实例(`Status=200`)

```json
{    "uid": 1,    "user": "ZRR",    "avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",    "plate_title": "治愈",    "post_title": "文章标题1",    "post_content": "文章内容1",    "created_at": "2021-08-08T03:02:25.952Z",    "updated_at": "2021-08-08T03:02:25.952Z",    "labels": [        {            "id": 56,            "user_id": 1,            "label_title": "标签11",            "label_dp": null,            "created_at": "2021-08-08 03:02:25",            "updated_at": "2021-08-08 03:02:25",            "status": 1        },        {            "id": 57,            "user_id": 1,            "label_title": "标签21",            "label_dp": null,            "created_at": "2021-08-08 03:02:25",            "updated_at": "2021-08-08 03:02:25",            "status": 1        }    ]}
```

---

# 系统模块`API`

## 文件上传与删除`API`(需要登录)

- 请求`URL`(`POST,DELETE`)
- `POST`请求(上传文件)

```http
/v1/system/file/upload
```

- 请求参数

| 参数值 | 类型 |  描述  |
| :----: | :--: | :----: |
| `pid`  | 选填 | 帖子ID |
| `file` | 必填 |  文件  |

- 返回实例(`Status=201`)

```json
{    "file_id": 11,    "file_post": "http://localhost:8000/medias/file/20210816/45714620210816_120041.png"}
```

- `DELETE`请求(删除文件)

- 请求参数

| 参数值 | 类型 |  描述  |
| :----: | :--: | :----: |
|  `pk`  | 必填 | 文件ID |

- 返回实例(`Status=201`)

---

# 评论类`API`

## 一级评论`API`(需要登录)

- 请求`URL`(`POST,DELET`)

```http
/v1/comments/comment/api/comment/one/to
```

- `POST`请求(一级评论)
- 请求参数

|  参数值   | 类型 |   描述   |
| :-------: | :--: | :------: |
|   `pid`   | 必填 |  帖子ID  |
| `content` | 必填 | 评论内容 |

- 返回状态码`Status=201`
- `DELET`请求(删除评论)
- 请求参数

| 参数值 | 类型 |  描述  |
| :----: | :--: | :----: |
|  `pk`  | 必填 | 帖子ID |

- 返回状态码`Status=200`

---

## 二级评论`API`(需要登录)

- 请求`URL`(`POST,DELET`)

```http
/v1/comments/comment/api/comment/two/to
```

- `POST`请求(一级评论)
- 请求参数

|    参数值     | 类型 |    描述    |
| :-----------: | :--: | :--------: |
| `comment_one` | 必填 | 一级评论ID |
|   `user_to`   | 必填 | 被评论人ID |
|   `content`   | 必填 |  评论内容  |

- 返回状态码`Status=201`

- DELET`请求(删除评论)
- 请求参数

| 参数值 | 类型 |  描述  |
| :----: | :--: | :----: |
|  `pk`  | 必填 | 帖子ID |

- 返回状态码`Status=200`

---

## 评论获取`API`

- 请求`URL`(`GET`)
- 请求参数

| 参数值  | 类型 |   描述   |
| :-----: | :--: | :------: |
|  `pid`  | 必填 |  帖子ID  |
| `page`  | 选填 |   页码   |
| `limit` | 选填 | 限制条数 |

- 返回实例(`Status=200`)

```json
{    "meta": {        "total_count": 62,        "page_count": 31,        "current_page": 1    },    "objects": [        {            "pid": 72,            "comment_one_id": 3,            "comment_one_user_id": 1,            "comment_one_user_nickname": "ZRR",            "comment_one_user_avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",            "comment_two_all": [                {                    "id": 28,                    "user_id": 1,                    "comment_one_id": 3,                    "user_to_id": 1,                    "content": "二级评论",                    "created_at": "2021-08-10 08:23:41",                    "updated_at": "2021-08-10 08:23:41",                    "status": 1                },                {                    "id": 29,                    "user_id": 1,                    "comment_one_id": 3,                    "user_to_id": 1,                    "content": "二级评论",                    "created_at": "2021-08-10 08:23:41",                    "updated_at": "2021-08-10 08:23:41",                    "status": 1                },                {                    "id": 30,                    "user_id": 1,                    "comment_one_id": 3,                    "user_to_id": 1,                    "content": "二级评论",                    "created_at": "2021-08-10 08:23:42",                    "updated_at": "2021-08-10 08:23:42",                    "status": 1                }            ]        },        {            "pid": 72,            "comment_one_id": 4,            "comment_one_user_id": 1,            "comment_one_user_nickname": "ZRR",            "comment_one_user_avatar": "http://localhost:8000/medias/avatar/20210814/79265620210814_104330.png",            "comment_two_all": []        }    ]}
```

---

# 邮件类

## 发送公共邮件， 查询公共邮件`API`(需要登录)

- 请求`URL`(`POST,GET`)

```http
/v1/emaillist/emaillist/api/send/open/email
```

- `POST`请求(发送公共邮件)
- 请求参数

|  参数值   | 类型 |   描述    |
| :-------: | :--: | :-------: |
|  `title`  | 必填 | 邮件标题  |
| `content` | 必填 |   内容    |
|  `audio`  | 选填 | 音频`URL` |

- 返回状态码(`Status=201`)

- `GET`请求(查询公共邮件)
- 返回实例(`Status=200`)

```json
{    "open_email": [        {            "id": 1,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-10 10:43:01",            "updated_at": "2021-08-10 10:43:01",            "status": 1        },        {            "id": 2,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-10 10:43:03",            "updated_at": "2021-08-10 10:43:03",            "status": 1        },        {            "id": 3,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-10 10:43:04",            "updated_at": "2021-08-10 10:43:04",            "status": 1        },        {            "id": 4,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-16 13:33:26",            "updated_at": "2021-08-16 13:33:26",            "status": 1        },        {            "id": 5,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-16 13:33:40",            "updated_at": "2021-08-16 13:33:40",            "status": 1        },        {            "id": 6,            "user_id": 1,            "title": "公共邮件",            "content": "公共邮件内容",            "audio": "",            "created_at": "2021-08-16 13:33:41",            "updated_at": "2021-08-16 13:33:41",            "status": 1        }    ]}
```

---

## 发送私人邮件， 查询已发送和已收到邮件`API`(需要登录)

- 请求`URL`(`POST,GET`)

```http
/v1/emaillist/emaillist/api/send/open/email
```

- `POST`请求(发送私人邮件)
- 请求参数

|  参数值   | 类型 |   描述   |
| :-------: | :--: | :------: |
| `to_user` | 必填 | 被邮件人 |
| `content` | 必填 |   内容   |
|  `title`  | 必填 |   标题   |

- 返回状态码(`Status=201`)

- `GET`请求(查询已发送和已收到邮件)
- 返回实例(`Status=200`)

```json
{    "email": [        {            "id": 1,            "user_id": 1,            "user_to_id": 7,            "title": "私人邮件",            "content": "私人邮件内容",            "created_at": "2021-08-10 10:47:55",            "updated_at": "2021-08-10 10:47:55",            "status": 1        },        {            "id": 2,            "user_id": 1,            "user_to_id": 7,            "title": "私人邮件",            "content": "私人邮件内容",            "created_at": "2021-08-16 13:42:01",            "updated_at": "2021-08-16 13:42:01",            "status": 1        },        {            "id": 3,            "user_id": 1,            "user_to_id": 7,            "title": "私人邮件",            "content": "私人邮件内容",            "created_at": "2021-08-16 13:42:45",            "updated_at": "2021-08-16 13:42:45",            "status": 1        }    ],    "email_go_to": []}
```

