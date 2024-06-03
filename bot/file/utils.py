import os
import aiohttp
from PIL import Image, ImageOps, ImageChops
import numpy as np
from pdf2image import convert_from_path
from logger import logger


async def download_file(file_url, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                with open(destination, "wb") as f:
                    f.write(await response.read())
            else:
                logger.error(f"Failed to download file from {file_url}")


def pdf_to_images(pdf_file_path):
    try:
        images = convert_from_path(pdf_file_path)
        return images
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def normalize_image(image_path):
    # Open the image and convert it to grayscale
    img = Image.open(image_path).convert("L")

    # Create a binary (black and white) version of the image
    threshold = 128
    binary_image = img.point(lambda p: p > threshold and 255)

    # Invert the image to handle white text on black background
    inverted_image = ImageOps.invert(img)
    inverted_binary_image = inverted_image.point(lambda p: p > threshold and 255)
    inverted_binary_image = ImageOps.invert(inverted_binary_image)

    # Combine the original binary image and the inverted binary image
    combined_image = ImageChops.lighter(binary_image, inverted_binary_image)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    combined_image.save(f"{current_dir}/normalized_image.png")

    return combined_image
