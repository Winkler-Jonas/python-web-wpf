from typing import Callable
from datetime import date, datetime
from pathlib import Path
from pdf2image import convert_from_path

import pypandoc
from django.conf import settings
from pypandoc.pandoc_download import download_pandoc

from django.core.files.storage import FileSystemStorage

import logging
logger = logging.getLogger(__name__)

__usr_dir: Callable[[str], Path] = lambda usr_id: Path(settings.MEDIA_ROOT) / usr_id / f'documents_{date.today().isoformat()}'
__get_fss: Callable[[str], FileSystemStorage] = lambda: FileSystemStorage(__usr_dir)


def __create_dir(usr_id: str):
    if not __usr_dir(usr_id).exists():
        __usr_dir(usr_id).mkdir(parents=True, exist_ok=True)


def __create_empty_pdf(usr_id: str) -> Path:
    empty_file: Path = Path(__usr_dir(usr_id) / f'{datetime.now().isoformat()}.pdf')
    empty_file.touch()
    return empty_file


def store_as_pdf(text: str, input_format: str, usr_id: str):
    try:
        __create_dir(usr_id)
        empty_file: Path = __create_empty_pdf(usr_id)
        output = pypandoc.convert_text(source=text,
                                       format=input_format,
                                       to='pdf',
                                       outputfile=str(empty_file),
                                       extra_args=['-V', 'geometry:margin=.75in'])
    except Exception as e:
        raise e
