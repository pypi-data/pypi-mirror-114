from PIL import Image


def get_image_size(image_path) -> (int, int):
    original_image = Image.open(image_path)
    return original_image.size