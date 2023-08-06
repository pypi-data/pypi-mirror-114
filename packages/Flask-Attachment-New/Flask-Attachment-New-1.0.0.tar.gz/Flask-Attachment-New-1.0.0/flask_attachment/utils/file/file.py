import hashlib
import os


file_type_dict = {
    '89504e470d0a1a0a': 'png',
    'ffd8ffe0': 'jpeg',
    'ffd8': 'jpg',
    '424d': 'bmp',
    '474946383761': 'gif',
    '474946383961': 'gif',
    '667479704d534e56': 'mp4',
    '6674797069736f6d': 'mp4',

    '49492a00227105008037': 'tif',
    '41433130313500000000': 'dwg',
    '3c21444f435459504520': 'html',
    '3c68746d6c3e0': 'html',
    '3c21646f637479706520': 'htm',
    '48544d4c207b0d0a0942': 'css',
    '696b2e71623d696b2e71': 'js',
    '7b5c727466315c616e73': 'rtf',
    '38425053000100000000': 'psd',
    '46726f6d3a203d3f6762': 'eml',
    'd0cf11e0a1b11ae10000': 'doc',
    '5374616e64617264204a': 'mdb',
    '252150532d41646f6265': 'ps',
    '255044462d312e350d0a': 'pdf',
    '2e524d46000000120001': 'rmvb',
    '464c5601050000000900': 'flv',
    '49443303000000002176': 'mp3',
    '000001ba210001000180': 'mpg',
    '3026b2758e66cf11a6d9': 'wmv',
    '52494646e27807005741': 'wav',
    '52494646d07d60074156': 'avi',
    '4d546864000000060001': 'mid',
    '504b0304140000000800': 'zip',
    '526172211a0700cf9073': 'rar',
    '235468697320636f6e66': 'ini',
    '504b03040a0000000000': 'jar',
    '4d5a9000030000000400': 'exe',
    '3c25402070616765206c': 'jsp',
    '4d616e69666573742d56': 'mf',
    '3c3f786d6c2076657273': 'xml',
    '494e5345525420494e54': 'sql',
    '7061636b616765207765': 'java',
    '406563686f206f66660d': 'bat',
    '1f8b0800000000000000': 'gz',
    '6c6f67346a2e726f6f74': 'properties',
    'cafebabe0000002e0041': 'class',
    '49545346030000006000': 'chm',
    '04000000010000001300': 'mxp',
    '504b0304140006000800': 'docx',
    '6431303a637265617465': 'torrent',
    '6d6f6f76': 'mov',
    'ff575043': 'wpd',
    'cfad12fec5fd746f': 'dbx',
    '2142444e': 'pst',
    'ac9ebd8f': 'qdf',
    'e3828596': 'pwl',
    '2e7261fd': 'ram',
}


def _bytes_to_hex(src: bytes) -> str:
    num = len(src)
    hex_str = u""
    for i in range(num):
        t = u"%x" % src[i]
        if len(t) % 2:
            hex_str += u"0"
        hex_str += t
    return hex_str.lower()


def _get_file_type(src: bytes) -> str:
    file_type = None
    code = _bytes_to_hex(src)
    for key, value in file_type_dict.items():
        if (code in key) or (key in code):
            file_type = value
            break
    return file_type


def get_file_type(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        size = 10
        src = file.read(size)
        file_type = _get_file_type(src)
        return file_type


def get_file_md5(file_path: str) -> str:
    md5_obj = hashlib.md5()  # 创建md5对象
    with open(file_path, 'rb') as file_obj:
        while True:
            data = file_obj.read(65536)
            if not data:
                break
            md5_obj.update(data)  # 更新md5对象
    hash_code = md5_obj.hexdigest()  # 返回md5对象
    return str(hash_code).lower()


def main():
    # os.path相关函数
    curr_path = os.path.abspath(__file__)
    print('curr_path: %s', curr_path)
    curr_dirname = os.path.dirname(curr_path)
    print('curr_dirname: %s', curr_dirname)
    a_file_path = os.path.join(curr_dirname, 'a.txt')
    print('a_file_path: %s', a_file_path)

    # 文件类型
    file_path = '/Users/zhangchi/Downloads/images/python.png'
    file_type = get_file_type(file_path)
    print('file_type: {}'.format(file_type))


if __name__ == '__main__':
    main()
