from fastapi import HTTPException
import math
import hashlib
from pathlib import Path
from PIL import Image
import uuid
from app.crud import post as post_crud


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


def save_images(images, post_id, db):
    roads = []
    try:
        for image in images:
            image_hash = hashlib.md5(image.file.read()).hexdigest()
            road = "/" + "/".join([str(image_hash[i] + str(image_hash[i + 1])) for i in range(0, 7, 2)])
            road += f"/{uuid.uuid4()}"
            roads.append(road)
            im = Image.open(image.file).convert("RGB")
            save_image_with_watermark(image=im, road=road)
            save_image_square_thumbnails(image=im, road=road)
    except Exception:
        return False
    post_crud.write_post_images_roads(db=db, post_id=post_id, images_roads=roads)
    post_crud.change_post_status(post_id=post_id, status_id=4, db=db)
    return True


def update_images(images, db_post, db):
    roads = []
    try:
        for image in images:
            if isinstance(image, int):
                road = next(iter([x.road for x in db_post.photos if x.id == image]))
                roads.append(road)
            else:
                image_hash = hashlib.md5(image.file.read()).hexdigest()
                road = "/" + "/".join([str(image_hash[i] + str(image_hash[i + 1])) for i in range(0, 7, 2)])
                road += f"/{uuid.uuid4()}"
                roads.append(road)
                im = Image.open(image.file).convert("RGB")
                save_image_with_watermark(image=im, road=road)
                save_image_square_thumbnails(image=im, road=road)
    except Exception:
        return False

    # post_crud.delete_post_images_roads(asdasdasd)
    # post_crud.write_post_images_roads(db=db, post_id=db_post, images_roads=roads)
    # post_crud.change_post_status(post_id=db_post.id, status_id=4, db=db)

    return True


def validate_updated_images(images, db_post, db):

    not_verified_images = checking_images_for_validity(
        [image for image in images if not isinstance(image, int)]
    )
    if len(not_verified_images) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Image has not been validated",
                                                     "not_verified_images": not_verified_images})

    db_post_images_ids = [x.id for x in db_post.photos]
    updated_images_ids = [x for x in images if isinstance(x, int)]
    not_verified_images_ids = [x for x in updated_images_ids if x not in db_post_images_ids]
    if len(not_verified_images_ids) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Image ids has not been validated",
                                                     "not_verified_images_ids": not_verified_images_ids})

    if len(updated_images_ids) != len(set(updated_images_ids)):
        raise HTTPException(status_code=400, detail={"msg": "Image ids duplicate"})
