import os
import shutil

from PIL import Image

from flask_attachment.handler.BaseHandler import BaseHandler
from flask_attachment.helper.snowflake.SnowflakeHelper import SnowflakeHelper


class ResizeHandler(BaseHandler):

    def __init__(self, src_file_path, dest_file_path: str, dest_width: int, dest_height: int):
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path
        self.dest_width = dest_width
        self.dest_height= dest_height
        self.snowflake_helper = SnowflakeHelper()

    def handle(self):
        resize_file_path = None
        try:
            # 获取原图信息
            src_path = os.path.dirname(self.src_file_path)
            image = Image.open(self.src_file_path)
            _format = image.format
            if (_format is None) or (_format.strip() == ''):
                raise Exception('the format of src file is empty')

            code = self.snowflake_helper.generate_str()
            resize_filename = '{0}.{1}'.format(code, _format.lower())
            resize_file_path = os.path.join(src_path, resize_filename)

            resize_image = image.resize((self.dest_width, self.dest_height), Image.ANTIALIAS)
            resize_image.save(resize_file_path)

            # 创建目标图
            shutil.move(resize_file_path, self.dest_file_path)
        except Exception as exception:
            if os.path.exists(self.dest_file_path):
                os.remove(self.dest_file_path)
            raise exception
        finally:
            if (resize_file_path is not None) and (os.path.exists(resize_file_path)):
                os.remove(resize_file_path)
