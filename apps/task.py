import requests


# import os
# import numpy as np
# from PIL import Image
#
#
# def loadImages(path, max_size):
#     imagesList = os.listdir(path)
#     loadedImages = []
#     temp_size = 0
#
#     for image in imagesList:
#         os.chdir(path)
#         temp_size += os.path.getsize(image)
#         if temp_size > max_size * 1000000:
#             break
#         img = Image.open(path + image)
#         arr = np.array(img)
#         loadedImages.append(arr)
#
#     return loadedImages
#
#
# loadImages(path, 50)


def download_image(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    file_size = int(response.headers.get('Content-Length', 0))

    if file_size < 10 * 1024 * 1024:
        raise ValueError("10 dan kam bolishi kerak")

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"image: {save_path}")
