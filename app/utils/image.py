from PIL import Image


def checking_images_for_validity(images):
    not_verified = []
    for index, image in enumerate(images):
        try:
            img = Image.open(image.file)
            img.verify()
        except Exception:
            not_verified.append({"index": index, "filename": image.filename})
    return not_verified
