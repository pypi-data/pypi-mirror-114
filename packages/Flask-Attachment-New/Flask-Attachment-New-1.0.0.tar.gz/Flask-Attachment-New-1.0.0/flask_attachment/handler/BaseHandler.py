from abc import ABCMeta, abstractmethod


class BaseHandler(object, metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        pass
