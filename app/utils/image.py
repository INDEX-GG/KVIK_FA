import math
import hashlib
from pathlib import Path

from PIL import Image
import uuid


def checking_images_for_validity(images):
    not_verified = []
    for index, image in enumerate(images):
        try:
            img = Image.open(image.file)
            img.verify()
        except Exception:
            not_verified.append({"index": index, "filename": image.filename})
    return not_verified


def save_file_in_folder(image, road, resolution):
    Path(f"./files/{road}").mkdir(parents=True, exist_ok=True)
    image.save(f"./files/{road}/{resolution}.webp", format="webp")


def add_watermark(image, size, step):
    watermark = Image.open("./static/watermark.png")
    watermark = watermark.resize(size)
    image.paste(watermark, (image.size[0] - size[0] - step, image.size[1] - size[1] - step), watermark)
    pass


def save_image_with_watermark(image, road):
    width, height = image.size
    aspect_ratio = height / width
    if aspect_ratio > 0.75:
        new_height = 960
        new_width = math.ceil(new_height / aspect_ratio)
    elif aspect_ratio < 0.75:
        new_width = 1280
        new_height = math.ceil(new_width * aspect_ratio)
    else:
        new_width = 1280
        new_height = 960
    im1 = image.resize((new_width, new_height))
    add_watermark(image=im1, size=(120, 66), step=20)
    save_file_in_folder(image=im1, road=road, resolution="1280x960")
    im2 = image.resize((math.ceil(new_width / 2), math.ceil(new_height / 2)))
    add_watermark(image=im2, size=(90, 50), step=10)
    save_file_in_folder(image=im2, road=road, resolution="640x480")


def save_image_square_thumbnails(image, road):
    width, height = image.size
    if width > height:
        cropped = (width - height) / 2
        im = image.crop((cropped, 0, width - cropped, height))
        im = im.resize((300, 300))
    elif width < height:
        cropped = (height - width) / 2
        im = image.crop((0, cropped, width, height - cropped))
        im = im.resize((300, 300))
    else:
        im = image.resize((300, 300))
    save_file_in_folder(image=im, road=road, resolution="300x300")
    im.thumbnail((200, 200))
    save_file_in_folder(image=im, road=road, resolution="200x200")
    im.thumbnail((100, 100))
    save_file_in_folder(image=im, road=road, resolution="100x100")


def save_images(images):
    roads = []
    try:
        for image in images:
            image_hash = hashlib.md5(image.file.read()).hexdigest()
            road = "/".join([str(image_hash[i] + str(image_hash[i + 1])) for i in range(0, 7, 2)])
            road += f"/{uuid.uuid4()}"
            roads.append(road)
            im = Image.open(image.file).convert("RGB")
            save_image_with_watermark(image=im, road=road)
            save_image_square_thumbnails(image=im, road=road)
    except Exception:
        return False
    return roads
