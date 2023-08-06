import os
from enum import Enum

from flask_attachment.data import OutputType


class Mode(Enum):
    NONE = 'none'
    MOVE = 'move'
    REMOVE = 'remove'
    CROP_SQUARE = 'crop_square'
    RESIZE = 'resize'
    BINARYZATION = 'binaryzation'


class Operation(object):

    ORIGINAL_FILENAME = 'original'

    def __init__(self, mode: Mode = None, src_path: str = None, src_file: str = None,
                 dest_path: str = None, dest_file: str = None, dest_width: int = None, dest_height: int = None,
                 output_type: OutputType = OutputType.NONE):
        self.mode = mode
        self.src_path = src_path
        self.src_file = src_file
        self.dest_path = dest_path
        self.dest_file = dest_file
        self.dest_width = dest_width
        self.dest_height = dest_height
        self.output_type = output_type

    def get_mode(self) -> Mode:
        return self.mode

    def set_mode(self, mode: Mode):
        self.mode = mode

    def get_src_path(self) -> str:
        return self.src_path

    def set_src_path(self, src_path: str):
        self.src_path = src_path

    def get_src_file(self) -> str:
        return self.src_file

    def set_src_file(self, src_file: str):
        self.src_file = src_file

    def get_dest_path(self) -> str:
        return self.dest_path

    def set_dest_path(self, dest_path: str):
        self.dest_path = dest_path

    def get_dest_file(self) -> str:
        return self.dest_file

    def set_dest_file(self, dest_file: str):
        self.dest_file = dest_file

    def get_dest_width(self) -> int:
        return self.dest_width

    def set_dest_width(self, dest_width: int):
        self.dest_width = dest_width

    def get_dest_height(self) -> int:
        return self.dest_height

    def set_dest_height(self, dest_height: int):
        self.dest_height = dest_height

    def get_output_type(self) -> OutputType:
        return self.output_type

    def set_output_type(self, output_type: OutputType):
        self.output_type = output_type

    def get_src_file_path(self) -> str:
        src_file_path = None
        if (self.src_path is not None) and (self.src_file is not None):
            src_file_path = os.path.join(self.src_path, self.src_file)
        return src_file_path

    def get_dest_file_path(self) -> str:
        dest_file_path = None
        if (self.dest_path is not None) and (self.dest_file is not None):
            dest_file_path = os.path.join(self.dest_path, self.dest_file)
        return dest_file_path
