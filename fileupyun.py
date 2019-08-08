from flask import g, current_app
from flask_restful.reqparse import RequestParser
from models import db
from .storage import upload_file
from .checkimage import image_file



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
