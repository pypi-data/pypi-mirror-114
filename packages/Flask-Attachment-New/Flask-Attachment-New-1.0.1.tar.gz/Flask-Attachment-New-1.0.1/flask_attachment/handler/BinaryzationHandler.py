import os
import shutil

from PIL import Image

from flask_attachment.handler.BaseHandler import BaseHandler
from flask_attachment.helper.snowflake.SnowflakeHelper import SnowflakeHelper


class BinaryzationHandler(BaseHandler):

    def __init__(self, src_file_path, dest_file_path: str):
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path
        self.snowflake_helper = SnowflakeHelper()

    def handle(self):
        binaryzation_file_path = None
        try:
            # 获取原图信息
            src_path = os.path.dirname(self.src_file_path)
            image = Image.open(self.src_file_path)
            _format = image.format
            if (_format is None) or (_format.strip() == ''):
                raise Exception('the format of src file is empty')

            code = self.snowflake_helper.generate_str()
            binaryzation_filename = '{0}.{1}'.format(code, _format.lower())
            binaryzation_file_path = os.path.join(src_path, binaryzation_filename)

            # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
            grayscale_image = image.convert('L')

            # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
            threshold = 200
            table = []
            for i in range(256):
                if i < threshold:
                    table.append(0)
                else:
                    table.append(1)

            # 图片二值化
            binaryzation_image = grayscale_image.point(table, '1')
            binaryzation_image.save(binaryzation_file_path)

            # 创建目标图
            shutil.move(binaryzation_file_path, self.dest_file_path)
        except Exception as exception:
            if os.path.exists(self.dest_file_path):
                os.remove(self.dest_file_path)
            raise exception
        finally:
            if (binaryzation_file_path is not None) and (os.path.exists(binaryzation_file_path)):
                os.remove(binaryzation_file_path)
