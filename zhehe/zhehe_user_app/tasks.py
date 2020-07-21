import inspect
import re
import sys
from typing import Callable, Dict, Union, TypeVar, List
from datetime import date, datetime
from pathlib import Path

from django.db import transaction
from django.utils import timezone
from pdf2image import convert_from_path

import pypandoc
from django.conf import settings
from pdf2image.exceptions import PDFPageCountError
from pypandoc.pandoc_download import download_pandoc
from .models import Document, DocumentPage

from django.core.files.storage import FileSystemStorage

import logging

logger = logging.getLogger(__name__)

# Each user has a separate folder inside MEDIA_ROOT
# This folder contains folders named by the date a document was uploaded
__usr_dir: Callable[[str], Path] = lambda usr_id: Path(
    settings.MEDIA_ROOT) / usr_id / f'documents_{date.today().isoformat()}'
__get_fss: Callable[[str], FileSystemStorage] = lambda: FileSystemStorage(__usr_dir)


# -----------------------------
# --------- Exceptions---------

class PandocException(Exception):
    """
    Exception is raised if any error occurs while converting text to pdf
    :example: wrong file format, file to large, syntax unknown etc..
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class ImgConvertError(Exception):
    """
    Exception is raised if any error occurs while converting pdf to img
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class FileNotFoundException(Exception):
    """
    Exception is raised if the user tries to save a document that's has not been converted
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

# ------------------------------
# ------ File Management -------
# ------------------------------


def __create_daily_dir(usr_id: str) -> None:
    """
    Creates a folder inside current user folder named by the current date if it doesn't already exists
    Also creates a temp folder for temporary files to be stored

    :param usr_id: The id of the user (pk of auth_user table)
    :type usr_id: str
    """
    if not __usr_dir(usr_id).exists():
        __usr_dir(usr_id).mkdir(parents=True, exist_ok=True)
    Path(__usr_dir(usr_id) / 'tmp').mkdir(parents=True, exist_ok=True)


def __clear_tmp(usr_id: str) -> None:
    """
    If temporary folder in daily folder of user already exists
    remove its content to clear up space.
    !Function should only be called from convert not save!

    :param usr_id: The id of the user (pk of auth_user table)
    :type usr_id: str
    """
    if (tmp_folder := Path(__usr_dir(usr_id) / 'tmp')).exists():
        for file in [file for file in tmp_folder.iterdir() if file.is_file()]:
            file.unlink()
            if file.suffix == '.pdf':
                DocumentPage.objects.filter(doc_fk=str(file)).delete()
                Document.objects.filter(document_path=str(file)).delete()
        for folder in [folder for folder in tmp_folder.iterdir() if file.is_dir()]:
            folder.rmdir()


def __create_empty_pdf(usr_id: str, tmp: bool = False) -> Path:
    """
    Creates an empty pdf file inside users daily folder, named by the current time

    :param usr_id: The id of the user (pk of auth_user table)
    :type usr_id: str
    :param tmp: If the file is only to be stored temporarily set to True. File will be stored in tmp folder
    :type tmp: bool
    :return: The path object of the created file
    :rtype: Path
    """
    if tmp:
        empty_file: Path = Path(__usr_dir(usr_id) / 'tmp' / f'{datetime.now().isoformat()}.pdf')
    else:
        empty_file: Path = Path(__usr_dir(usr_id) / f'{datetime.now().isoformat()}.pdf')
    empty_file.touch()
    return empty_file


def __usr_has_document(usr_id: str) -> bool:
    """
    Check whether the user currently has a temporary file created in his workspace

    :param usr_id: The id of the user (pk of auth_user table)
    :type usr_id: str
    :return: True if he has, else False
    :rtype: bool
    """
    tmp_dir: Path = Path(__usr_dir(usr_id) / 'tmp')
    return True if tmp_dir.exists() and len([file for file in tmp_dir.iterdir() if file.is_file()]) > 1 else False


def __store_doc_permanent(usr_id: str, doc_name: str, doc_info: str = None) -> None:

    def move_file_to_parent(file: Path) -> Path:
        """
        Moves provided file one folder up to parent dir

        :param file: The file to be moved
        :type file: Path
        :return: The new path of the file
        :rtype: Path
        """
        new_path: Path = Path(file).absolute()
        parent_dir: Path = new_path.parent.parent
        return new_path.rename(parent_dir / new_path.name)

    def insert_new_pdf(new_path: Path):
        __insert_into('Dokument')

    for doc in [doc for doc in Path(__usr_dir(usr_id) / 'tmp').iterdir() if doc.is_file()]:
        new_path: Path = move_file_to_parent(doc)
        if doc.suffix == '.pdf':
            old_doc = Document.objects.get(document_path=str(doc))

            __insert_into('Document', **{'document_name': doc_name,
                                         'document_path': str(new_path),
                                         'document_date_edit': timezone.make_aware(datetime.now()),
                                         'document_date_added': timezone.make_aware(datetime.now()),
                                         'document_info': doc_info,
                                         'document_owner': usr_id,
                                         'document_format': old_doc.document_format,
                                         'document_text': old_doc.document_text})
            new_doc = Document.objects.get(document_path=str(new_path))
            with transaction.atomic():
                old_img_list = DocumentPage.objects.filter(doc_fk=str(doc))
                for old_img in old_img_list:
                    old_img.doc_page_path = re.sub(r'/tmp', '', old_img.doc_page_path)
                    old_img.doc_fk = new_doc
                    old_img.save()
                old_doc.delete()
    return new_path


# ------------------------------
# ------ File Conversion -------
# ------------------------------

def __convert_to_pdf(text: str, input_format: str, output_file: Path):
    """
    Function tries to convert text to pdf format

    :param text:
    :type text:
    :param input_format:
    :type input_format:
    :return:
    :rtype:
    """
    try:
        pypandoc.convert_text(source=text,
                              format=input_format,
                              to='pdf',
                              outputfile=str(output_file),
                              extra_args=['-V', 'geometry:margin=.75in'])
    except Exception as e:
        raise PandocException('Es ist ein Fehler bei der Konvertierung Ihres Texts aufgetreten! Bitte kontaktieren Sie '
                              'uns mithilfe des Kontaktformulars.')


def __convert_to_images(pdf_file: Path) -> None:
    """
    Function converts a pdf file to PNG-Files and stores them in database

    :raises ImgConvertError: In case an error occurred while converting the pdf

    :param pdf_file: the path of the PDF-File
    :type pdf_file: Path
    """
    try:
        for idx, page in enumerate(convert_from_path(pdf_file)):
            page.save((tmp_path := Path(f"{pdf_file.parent / f'{pdf_file.stem!s}_{idx}'}.png")).absolute(), 'PNG')
            path: str = re.sub(r'(?<=^/)media_content(?=/)', 'media', f'{tmp_path.absolute()}')
            __insert_into('DocumentPage', **{'doc_page_path': path,
                                             'doc_page_no': idx,
                                             'doc_fk': Document.objects.get(document_path=str(pdf_file))})
    except PDFPageCountError:
        raise ImgConvertError('Es ist ein Fehler bei der Konvertierung Ihres Texts aufgetreten! Bitte kontaktieren Sie '
                              'uns mithilfe des Kontaktformulars.')


# -----------------------------
# ---- Public Functions -------
# -----------------------------

def convert_doc(text: str, input_format: str, usr_id: str) -> str:
    """
    Function converts string into pdf-document.
    However this is only temporary and the file will be removed once function is called again.

    :raises PandocException: If error occurred while converting text to pdf
    :raises ImgConvertError: In case an error occurred while converting the pdf
    :raises UnknownModel: If model was not found on database (theoretically not possible)

    :param text: The utf-8 text to be converted
    :type text: str
    :param input_format: the format of the text provided
    :type input_format: str
    :param usr_id: the user that is trying to convert the text
    :type usr_id: str
    :return: The path of the pdf created
    :rtype: str
    """
    # Setup basic structure
    __clear_tmp(usr_id=usr_id)
    __create_daily_dir(usr_id=usr_id)
    pdf_file: Path = __create_empty_pdf(usr_id=usr_id, tmp=True)

    # Convert text to images
    __convert_to_pdf(text=text, input_format=input_format, output_file=pdf_file)
    __insert_into(table_name='Document', **{'document_owner': usr_id,
                                            'document_name': pdf_file.stem,
                                            'document_text': text,
                                            'document_format': input_format,
                                            'document_path': str(pdf_file),
                                            'document_date_edit': timezone.make_aware(datetime.now()),
                                            'document_date_added': timezone.make_aware(datetime.now()),
                                            'document_info': ''})
    __convert_to_images(pdf_file=pdf_file)
    return str(pdf_file)


def save_doc(doc_name: str, doc_info: str, usr_id: str):
    if __usr_has_document(usr_id=usr_id):
        return str(__store_doc_permanent(usr_id=usr_id, doc_name=doc_name, doc_info=doc_info))
    else:
        raise FileNotFoundException('Keine Datei gefunden. Bitte stellen Sie sicher, dass Sie Ihren Text konvertiert haben.')


# -------------------------------------
# ------ Simplified model access ------
# -------------------------------------

MODEL_LOCATION: str = 'models'
MODELS: List[str] = []
ModelCls = TypeVar('ModelCls')


class UnknownModel(Exception):
    """
    Exception is raised if user tries to access unknown db-model
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


def __get_models():
    """
    Returns all available models found in project.
    In case models are not stored in models.py, change global MODELS var.

    :return: List of available Models
    :rtype: List[str]
    """
    global MODELS
    if not MODELS:
        MODELS = [clsname for clsname, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass)
                  if MODEL_LOCATION in cls.__module__]
    return MODELS


def __find_model(model_name: str) -> str:
    """
    Try getting the specified model from database

    :raises UnknownModel: If model was not found on database (theoretically not possible)

    :param model_name: The name of the relation
    :type model_name: str
    :return: Relation-Name if found
    :rtype: str
    """
    try:
        return [mdl for mdl in __get_models() if model_name.lower() == mdl.lower()][0]
    except IndexError:
        raise UnknownModel(f'Relation {model_name} nicht gefunden in Datenbank')


def __insert_into(table_name: str, **kwargs: Dict[str, Union[str, int, float]]) -> None:
    """
    Insert values into model

    :param table_name: The name of the model (needs to be imported)
    :type table_name: str
    :param kwargs: the values to be inserted with their matching attributes
    :type kwargs: Dict[str, Union[str, int, float]]
    :return: Nothing
    :rtype: None
    """
    model: ModelCls = getattr(sys.modules.get(Document.__module__), __find_model(table_name))
    model.objects.create(**kwargs)
