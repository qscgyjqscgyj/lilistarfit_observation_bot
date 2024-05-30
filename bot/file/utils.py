import aiohttp
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
