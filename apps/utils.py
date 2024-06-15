from random import randint
from qiniu import Auth, put_data, etag, BucketManager
from werkzeug.datastructures import FileStorage

from .exts import db
from .const_bf import SECRET_KEY, ACCESS_KEY

class BaseModel(db.Model):
    __abstract__ = True

    def yes(self):  # add and update user
        db.session.add(self)
        db.session.commit()

    def ono(self):  # physical delete user
        db.session.delete(self)
        db.session.commit()


def upload_to_qiniu(pic: FileStorage):
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY
    q = Auth(access_key, secret_key)
    bucket_name = 'bloghah'  # 空间名

    # 上传后保存的文件名
    file_name = pic.filename
    the_suffix = file_name.rsplit('.')[-1]
    the_name = file_name.rsplit('.')[0]

    # key = 'my-python-logo.png'
    key = the_name + '_' + str(randint(1, 9999)) + '.' + the_suffix
    print('the key is', key)
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_data(token, key, pic.read())
    return ret, info


def delete_to_qiniu(filename):
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY

    # 初始化Auth状态
    q = Auth(access_key, secret_key)

    # 初始化BucketManager
    bucket = BucketManager(q)

    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = 'bloghah'  # 空间名
    key = filename

    # 删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    return info
