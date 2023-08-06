from enum import Enum, unique


# 文件类型
@unique
class FileType(Enum):

    UNKNOWN = 'unknown'
    PNG = 'png'
    JPEG = 'jpeg'
    JPG = 'jpg'
    BMP = 'bmp'
    GIF = 'gif'
    MP4 = 'mp4'

    @classmethod
    def from_value(cls, value: str):
        file_type = cls.UNKNOWN
        if value is not None:
            for _file_type in cls:
                if value.lower() == _file_type.value:
                    file_type = _file_type
                    break
        return file_type



# 媒体类型
@unique
class MediaType(Enum):

    UNKNOWN = -1
    IMAGE = 0
    VIDEO = 1

    @classmethod
    def from_value(cls, value: int):
        media_type = cls.UNKNOWN
        if value is not None:
            for _media_type in cls:
                if value == _media_type.value:
                    media_type = _media_type
                    break
        return media_type


    @classmethod
    def from_file_type(cls, file_type: FileType):
        media_type = cls.UNKNOWN
        if file_type in [FileType.PNG, FileType.JPEG, FileType.JPG, FileType.BMP, FileType.GIF]:
            media_type = cls.IMAGE
        elif file_type in [FileType.MP4]:
            media_type = cls.VIDEO
        return media_type


# 输出类型
@unique
class OutputType(Enum):

    NONE = ''
    ORIGINAL = 'original'
    THUMBNAIL = 'thumbnail'

    @classmethod
    def from_value(cls, value: str):
        output_type = cls.NONE
        if value is not None:
            for _output_type in cls:
                if value == _output_type.value:
                    output_type = _output_type
                    break
        return output_type


def main():
    file_type = FileType.from_value('png')
    media_type = MediaType.from_file_type(file_type)
    print(media_type)

    output_type = OutputType.ORIGINAL
    print(output_type.value)


if __name__ == '__main__':
    main()
