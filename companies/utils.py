from pdf2image import convert_from_path
from .models import CataloguePagePdf
from django.core.files.base import ContentFile
from io import BytesIO
import logging

def convert_pdf_to_images(catalogue_instance):
    try:
        print(f"Converting PDF file {catalogue_instance.pdf_file.path}")
        pages = convert_from_path(catalogue_instance.pdf_file.path)

        for index, page in enumerate(pages):
            print(f"Saving image for page {index + 1}")
            img_io = BytesIO()
            page.save(img_io, 'JPEG')
            img_io.seek(0)

          
            new_page = CataloguePagePdf.objects.create(
                catalogue=catalogue_instance,
                page_number=index + 1
            )
            new_page.image.save(f"{catalogue_instance.id}_page_{index + 1}.jpg", ContentFile(img_io.read()), save=True)
            print(f"Page {index + 1} image saved successfully.")
    except Exception as e:
        logging.error(f"Error converting PDF to images: {e}")
        print(f"Error converting PDF to images: {e}")
