import json
import os

from flask_attachment.data import FileType, MediaType, OutputType
from flask_attachment.helper.snowflake.SnowflakeHelper import SnowflakeHelper
from flask_attachment.utils.file.file import get_file_type, get_file_md5
from flask_attachment.utils.file.image import get_image_size


class FileInfo(object):

    def __init__(self, code: str = None, tag: str = None, file_type: str = FileType.UNKNOWN.value,
                 media_type: int = MediaType.UNKNOWN.value, output_type: str = OutputType.NONE.value, md5: str = None,
                 path: str = None, size: int = 0, width: int = 0, height: int = 0, length: float = 0):
        self.code = code
        self.tag = tag
        self.file_type = file_type
        self.media_type = media_type
        self.output_type = output_type
        self.md5 = md5
        self.path = path
        self.size = size
        self.width = width
        self.height = height
        self.length = length

    def get_code(self) -> str:
        return self.code

    def set_code(self, code: str):
        self.code = code

    def get_tag(self) -> str:
        return self.tag

    def set_tag(self, tag: str):
        self.tag = tag

    def get_file_type(self) -> str:
        return self.file_type

    def set_file_type(self, file_type: str):
        self.file_type = file_type

    def get_media_type(self) -> int:
        return self.media_type

    def set_media_type(self, media_type: int):
        self.media_type = media_type

    def get_output_type(self) -> str:
        return self.output_type

    def set_output_type(self, output_type: str):
        self.output_type = output_type

    def get_md5(self) -> str:
        return self.md5

    def set_md5(self, md5: str):
        self.md5 = md5

    def get_path(self) -> str:
        return self.path

    def set_path(self, path: str):
        self.path = path

    def get_size(self) -> int:
        return self.size

    def set_size(self, size: int):
        self.size = size

    def get_width(self) -> int:
        return self.width

    def set_width(self, width: int):
        self.width = width

    def get_height(self) -> int:
        return self.height

    def set_height(self, height: int):
        self.height = height

    def get_length(self) -> float:
        return self.length

    def set_length(self, length: float):
        self.length = length

    def to_string(self) -> str:
        data = {
            'code': self.code,
            'tag': self.tag,
            'file_type': self.file_type,
            'media_type': self.media_type,
            'output_type': self.output_type,
            'md5': self.md5,
            'path': self.path,
            'size': self.size,
            'width': self.width,
            'height': self.height,
            'length': self.length,
        }
        return json.dumps(data, ensure_ascii=False)


class FileInfoBuilder(object):

    def __init__(self, tag: str, file_path: str, output_type: OutputType):
        self.tag = tag
        self.file_path = file_path
        self.output_type = output_type
        self.snowflake_helper = SnowflakeHelper()

    def get_tag(self) -> str:
        return self.tag

    def set_tag(self, tag: str):
        self.tag = tag

    def get_file_path(self) -> str:
        return self.file_path

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def get_output_type(self) -> OutputType:
        return self.output_type

    def set_output_type(self, output_type: OutputType):
        self.output_type = output_type

    def build(self) -> FileInfo:
        if not os.path.exists(self.file_path):
            raise Exception('the file is not found. file_path: {}'.format(self.file_path))
        code = self.snowflake_helper.generate_str()
        file_type_value = get_file_type(self.file_path)
        file_type = FileType.from_value(file_type_value)
        media_type = MediaType.from_file_type(file_type)
        output_type = self.output_type.value
        md5 = get_file_md5(self.file_path)
        size = os.path.getsize(self.file_path)
        width = 0
        height = 0
        length = 0
        if media_type == MediaType.IMAGE:
            width, height = get_image_size(self.file_path)
        elif media_type == MediaType.VIDEO:
            pass

        file_info = FileInfo(code=code, tag=self.tag, file_type=file_type.value, media_type=media_type.value,
                             output_type=output_type, md5=md5, path=self.file_path, size=size, width=width,
                             height=height, length=length)
        return file_info
