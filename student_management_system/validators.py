import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".png",
        ".jpeg",
        ".csv",
        ".ppt",
        ".pptx",
        ".img",
        ".xlsx",
        ".xls",
    ]
    # valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension.Please upload appropriate extensions"
        )


def pdf_file_validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".pdf"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension.You Can Upload Only PDF Files"
        )


def img_pdf_file_validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [
        ".pdf",
        ".img",
        ".jpg",
        ".png",
        ".jpeg",
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension.You Can Upload Only PDF and IMAGE Files"
        )


def img_pdf_doc_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [
        ".pdf",
        ".jpg",
        ".png",
        ".jpeg",
        ".img",
        ".doc",
        ".docx"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension.You Can Upload Only PDF,IMGES,.DOC,.DOCX"
        )
