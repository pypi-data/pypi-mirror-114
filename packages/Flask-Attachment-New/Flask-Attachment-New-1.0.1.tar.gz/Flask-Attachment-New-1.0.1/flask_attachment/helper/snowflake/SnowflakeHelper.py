import base64

from flask_attachment.utils.decorator.Singleton import singleton
from flask_attachment.utils.snowflake.Snowflake import Snowflake


@singleton
class SnowflakeHelper(object):

    def __init__(self, data_center_id: int = 0, worker_id: int = 0):
        self.snowflake = Snowflake(data_center_id, worker_id)

    def generate(self) -> int:
        code = self.snowflake.take()
        return code

    def generate_str(self) -> str:
        code = self.generate()
        return str(code)

    def generate_base64(self) -> str:
        code = self.generate_str()
        code_bytes = base64.b64encode(str.encode(code))
        return bytes.decode(code_bytes)


def main():
    snowflake_helper = SnowflakeHelper()
    code = snowflake_helper.generate_base64()
    print(code)
    pass


if __name__ == '__main__':
    main()
