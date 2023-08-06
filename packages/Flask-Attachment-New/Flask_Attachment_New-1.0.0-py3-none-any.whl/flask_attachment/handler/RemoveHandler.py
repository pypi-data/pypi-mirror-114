import os

from flask_attachment.handler.BaseHandler import BaseHandler


class RemoveHandler(BaseHandler):

    def __init__(self, src_file_path: str):
        self.src_file_path = src_file_path

    def handle(self):
        os.remove(self.src_file_path)
