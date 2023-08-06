import os
import shutil

from PIL import Image

from flask_attachment.handler.BaseHandler import BaseHandler
from flask_attachment.helper.snowflake.SnowflakeHelper import SnowflakeHelper


class CropSquareHandler(BaseHandler):

    def __init__(self, src_file_path, dest_file_path: str):
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path
        self.snowflake_helper = SnowflakeHelper()

    def handle(self):
        cropped_file_path = None
        try:
            # 获取原图信息
            src_path = os.path.dirname(self.src_file_path)
            image = Image.open(self.src_file_path)
            width, height = image.size
            if width <= 0:
                raise Exception('the width of src file less than or equal 0')
            if height <= 0:
                raise Exception('the heightof src file less than or equal 0')
            _format = image.format
            if (_format is None) or (_format.strip() == ''):
                raise Exception('the format of src file is empty')

            # 裁剪原图
            code = self.snowflake_helper.generate_str()
            cropped_filename = '{0}.{1}'.format(code, _format.lower())
            cropped_file_path = os.path.join(src_path, cropped_filename)
            if width > height:
                offset = (width - height) // 2
                left = offset
                right = width - offset
                top = 0
                bottom = height
                cropped_image = image.crop((left, top, right, bottom))
                cropped_image.save(cropped_file_path)
            elif width < height:
                offset = (height - width) // 2
                left = 0
                right = width
                top = offset
                bottom = height - offset
                cropped_image = image.crop((left, top, right, bottom))
                cropped_image.save(cropped_file_path)

            # 创建目标图
            shutil.move(cropped_file_path, self.dest_file_path)
        except Exception as exception:
            if os.path.exists(self.dest_file_path):
                os.remove(self.dest_file_path)
            raise exception
        finally:
            if (cropped_file_path is not None) and (os.path.exists(cropped_file_path)):
                os.remove(cropped_file_path)
