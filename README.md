# qiniu-storage-scheme
在项目里实现七牛云第三方存储图片方案及Demo说明
## 使用说明
### 七牛云第三方存储方案
* 注册
* 新建存储空间
* 使用七牛SDK完成代码实现https://developer.qiniu.com/kodo/sdk/1242/python
* 安装 pip install qiniu
### 上传代码demo
```python
def upload_file(data):
    """
    上传文件到七牛云
    :param data: 上传的二进制数据
    :return: 上传的文件名
    """

    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'QINIU_ACCESS_KEY'
    secret_key = 'QINIU_SECRET_KEY'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'QINIU_BUCKET_NAME'

    # 上传后保存的文件名  如果key设置为None,会自动生成文件名称
    key = None
    # 生成上传 Token，可以指定过期时间等

    token = q.upload_token(bucket_name, key, 3600 * 1000)

    # 上传文件
    ret, info = put_data(token, key, data)

    if info.status_code == 200:

        return ret.get('key')

    else:

        raise Exception(info.error)

```
### 检测图片demo
```python

def image_file(value):
    """
    检查是否是图片文件
    :param value:
    :return:
    """
    try:
        file_type = imghdr.what(value)
    except Exception:
        raise ValueError('Invalid image.')
    else:
        if not file_type:
            raise ValueError('Invalid image.')
        else:
            return value
```
### 具体接口实现demo
```python
    def patch(self):
        """用户头像的上传"""

        # 获取参数
        parser = RequestParser()
        parser.add_argument('photo', location='files', required=True, type=image_file)
        args = parser.parse_args()


        # 读取上传的数据
        img_bytes = args.photo.read()

        # 将数据上传到七牛云
        try:

            file_name = upload_file(img_bytes)

        except BaseException as e:

            current_app.logger.error(e)  # 将数据记录到日志中

            return {"message": "Third Error"}, 500


        # 将头像的URL保存到数据库
        User.query.filter(User.id==g.user_id).update({'profile_photo': file_name})


        # 提交会话
        db.session.commit()


        # 将URL返回给前端
        return {'photo_url': current_app.config["QINIU_DOMAIN"] + file_name}

```
