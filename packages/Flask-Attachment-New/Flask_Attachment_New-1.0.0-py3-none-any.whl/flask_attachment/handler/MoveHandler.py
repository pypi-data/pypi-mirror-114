import shutil

from flask_attachment.handler.BaseHandler import BaseHandler


class MoveHandler(BaseHandler):

    def __init__(self, src_file_path, dest_file_path: str):
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path

    def handle(self):
        shutil.move(self.src_file_path, self.dest_file_path)
