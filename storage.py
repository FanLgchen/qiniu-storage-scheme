
from qiniu import Auth, put_data

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



