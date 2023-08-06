import os
import shutil
import sys
import traceback
from typing import List

from flask import current_app
from werkzeug.datastructures import FileStorage

from flask_attachment.data import OutputType
from flask_attachment.data.FileInfo import FileInfo, FileInfoBuilder
from flask_attachment.data.Operation import Operation, Mode
from flask_attachment.handler.BinaryzationHandler import BinaryzationHandler
from flask_attachment.handler.CropSquareHandler import CropSquareHandler
from flask_attachment.handler.MoveHandler import MoveHandler
from flask_attachment.handler.RemoveHandler import RemoveHandler
from flask_attachment.handler.ResizeHandler import ResizeHandler


class Options(object):

    def __init__(self, source_path: str = None, archive_path: str = None):
        self.source_path = source_path
        self.archive_path = archive_path

    def get_source_path(self) -> str:
        return self.source_path

    def set_source_path(self, source_path: str):
        self.source_path = source_path

    def get_archive_path(self) -> str:
        return self.archive_path

    def set_archive_path(self, archive_path: str):
        self.archive_path = archive_path


class Manager(object):

    def __init__(self, options: Options):
        self.options = options

    def download(self, tag: str, data: bytes, operations: List[Operation], limit_size: int = 0) -> List[FileInfo]:
        download_files = []
        file_paths = []
        try:
            # 建立下载文件夹
            source_path = self.options.get_source_path()
            download_path = os.path.join(source_path, tag)
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            # 保存下载文件
            original_file_path = os.path.join(download_path, Operation.ORIGINAL_FILENAME)
            with open(original_file_path, "wb") as code:
                code.write(data)

            file_size = os.stat(original_file_path).st_size
            if (limit_size > 0) and (file_size > limit_size):
                raise Exception('download file is too large. size: {}'.format(file_size))

            # 按步骤处理文件
            for operation in operations:
                mode = operation.get_mode()
                output_type = operation.get_output_type()

                # 处理文件
                file_path = None
                if mode == Mode.NONE:
                    file_path = self._handle_none(operation)
                elif mode == Mode.MOVE:
                    file_path = self._handle_move(operation)
                elif mode == Mode.REMOVE:
                    self._handle_remove(operation)
                elif mode == Mode.CROP_SQUARE:
                    file_path = self._handle_crop_square(operation)
                elif mode == Mode.RESIZE:
                    file_path = self._handle_resize(operation)
                elif mode == Mode.BINARYZATION:
                    file_path = self._handle_binaryzation(operation)

                # 是否保留目标文件
                if (output_type is not None) and (output_type != OutputType.NONE) and (file_path is not None):
                    builder = FileInfoBuilder(tag, file_path, output_type)
                    download_file = builder.build()
                    download_files.append(download_file)

                file_paths.append(file_path)
        except Exception as exception:
            self._clear_files(file_paths)
            current_app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                     str(exception))
            current_app.logger.error(traceback.format_exc())
            raise exception
        return download_files

    def upload(self, tag: str, file: FileStorage, operations: List[Operation], limit_size: int = 0) -> List[FileInfo]:
        upload_files = []
        file_paths = []
        try:
            # 建立上传文件夹
            _upload_path = self.options.get_source_path()
            upload_path = os.path.join(_upload_path, tag)
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            # 保存上传文件
            original_file_path = os.path.join(upload_path, Operation.ORIGINAL_FILENAME)
            file.save(original_file_path)

            file_size = os.stat(original_file_path).st_size
            if (limit_size > 0) and (file_size > limit_size):
                raise Exception('upload file is too large. size: {}'.format(file_size))

            # 按步骤处理文件
            for operation in operations:
                mode = operation.get_mode()
                output_type = operation.get_output_type()

                # 处理文件
                file_path = None
                if mode == Mode.NONE:
                    file_path = self._handle_none(operation)
                elif mode == Mode.MOVE:
                    file_path = self._handle_move(operation)
                elif mode == Mode.REMOVE:
                    self._handle_remove(operation)
                elif mode == Mode.CROP_SQUARE:
                    file_path = self._handle_crop_square(operation)
                elif mode == Mode.RESIZE:
                    file_path = self._handle_resize(operation)
                elif mode == Mode.BINARYZATION:
                    file_path = self._handle_binaryzation(operation)

                # 是否保留目标文件
                if (output_type is not None) and (output_type != OutputType.NONE) and (file_path is not None):
                    builder = FileInfoBuilder(tag, file_path, output_type)
                    upload_file = builder.build()
                    upload_files.append(upload_file)

                file_paths.append(file_path)
        except Exception as exception:
            self._clear_files(file_paths)
            current_app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                     str(exception))
            current_app.logger.error(traceback.format_exc())
            raise exception
        return upload_files

    def archive(self, tag: str, operations: List[Operation]) -> List[FileInfo]:
        archive_files = []
        file_paths = []
        try:
            # 建立归档文件夹
            archive_path = self.options.get_archive_path()
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)

            # 按步骤处理文件
            for operation in operations:
                mode = operation.get_mode()
                output_type = operation.get_output_type()

                # 处理文件
                file_path = None
                if mode == Mode.NONE:
                    file_path = self._handle_none(operation)
                elif mode == Mode.MOVE:
                    file_path = self._handle_move(operation)
                elif mode == Mode.REMOVE:
                    self._handle_remove(operation)
                elif mode == Mode.CROP_SQUARE:
                    file_path = self._handle_crop_square(operation)
                elif mode == Mode.RESIZE:
                    file_path = self._handle_resize(operation)
                elif mode == Mode.BINARYZATION:
                    file_path = self._handle_binaryzation(operation)

                # 是否保留目标文件
                if (output_type is not None) and (output_type != OutputType.NONE) and (file_path is not None):
                    builder = FileInfoBuilder(tag, file_path, output_type)
                    archive_file = builder.build()
                    archive_files.append(archive_file)

                file_paths.append(file_path)
        except Exception as exception:
            self._clear_files(file_paths)
            current_app.logger.error('(%s.%s) exception: %s', self.__class__.__name__, sys._getframe().f_code.co_name,
                                     str(exception))
            current_app.logger.error(traceback.format_exc())
            raise exception
        return archive_files

    def clear(self, tag: str):
        # 获取源目录
        source_path = self.options.get_source_path()
        clear_path = os.path.join(source_path, tag)

        # 删除源目录
        if os.path.exists(clear_path):
            shutil.rmtree(clear_path)

    def _handle_none(self, operation: Operation) -> str:
        src_file_path = operation.get_src_file_path()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        return src_file_path

    def _handle_move(self, operation: Operation) -> str:
        src_file_path = operation.get_src_file_path()
        dest_file_path = operation.get_dest_file_path()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        move_handler = MoveHandler(src_file_path, dest_file_path)
        move_handler.handle()

        return dest_file_path

    def _handle_remove(self, operation: Operation):
        src_file_path = operation.get_src_file_path()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        remove_handler = RemoveHandler(src_file_path)
        remove_handler.handle()

    def _handle_crop_square(self, operation: Operation) -> str:
        src_file_path = operation.get_src_file_path()
        dest_file_path = operation.get_dest_file_path()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        crop_square_handler = CropSquareHandler(src_file_path, dest_file_path)
        crop_square_handler.handle()

        return dest_file_path

    def _handle_resize(self, operation: Operation) -> str:
        src_file_path = operation.get_src_file_path()
        dest_file_path = operation.get_dest_file_path()
        dest_width = operation.get_dest_width()
        dest_height = operation.get_dest_height()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        resize_handler = ResizeHandler(src_file_path, dest_file_path, dest_width, dest_height)
        resize_handler.handle()

        return dest_file_path

    def _handle_binaryzation(self, operation: Operation) -> str:
        src_file_path = operation.get_src_file_path()
        dest_file_path = operation.get_dest_file_path()

        if not os.path.exists(src_file_path):
            raise Exception('src file not exists. src_file_path: {}'.format(src_file_path))

        binaryzation_handler = BinaryzationHandler(src_file_path, dest_file_path)
        binaryzation_handler.handle()

        return dest_file_path

    def _clear_files(self, file_paths: List[str]):
        for file_path in file_paths:
            os.unlink(file_path)
