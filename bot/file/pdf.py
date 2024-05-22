from pdf2image import convert_from_path

def pdf_to_images(pdf_file_path):
    try:
        images = convert_from_path(pdf_file_path)
        return images
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
