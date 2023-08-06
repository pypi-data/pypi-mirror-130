import os
from os.path import expanduser
import shutil
import logging
import urllib.request as request
from contextlib import closing
from Configs import getConfig


config = getConfig()

log = logging.getLogger("PubmedSuckerETLProcessToFile")


def _extract_gz_file(source_file, target_file):
    import gzip
    import shutil

    # Check sanity
    if not os.path.isfile(source_file):
        log.error(f"Error extracting {source_file}. File does not exists.")
        raise ValueError(f"Error extracting {source_file}. File does not exists.")
    if not os.access(os.path.dirname(target_file), os.W_OK):
        log.error(
            f"Error extracting {source_file}. Target dir {os.path.dirname(target_file)} is not writable."
        )
        raise ValueError(
            f"Error extracting {source_file}. Target dir {os.path.dirname(target_file)} is not writable."
        )
    # try writing file
    try:
        f = open(target_file, "w")
        f.write("test")
        f.close()
        os.remove(target_file)
    except:
        log.error(
            f"Error extracting {source_file}. Target {target_file} is not writable."
        )
        raise ValueError(
            f"Error extracting {source_file}. Target {target_file} is not writable."
        )

    try:
        with gzip.open(source_file, "rb") as f_in:
            with open(target_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        log.error(f"Error extracting {source_file} to {target_file}")
        raise
    return target_file


def download(source) -> str:
    storage_dir = os.path.abspath(config.PUBMED_XML_DOWNLOAD_DIR)
    os.makedirs(storage_dir, exist_ok=True)
    source_filename = os.path.basename(source)
    download_path = os.path.join(storage_dir, source_filename)
    file_name, file_extension = os.path.splitext(source_filename)
    if file_extension == ".gz":
        storage_path = os.path.join(storage_dir, file_name)
    else:
        storage_path = download_path
    if not os.path.isfile(storage_path) or config.REDOWNLOAD_EXTISTING_PUBMED_XMLS:
        try:
            with closing(request.urlopen(source)) as r:
                with open(download_path, "wb") as f:
                    shutil.copyfileobj(r, f)
        except:
            log.error(f"Failed downloading file from '{source}' to '{download_path}'")
            raise
        if file_extension == ".gz":
            _extract_gz_file(download_path, storage_path)
            os.remove(download_path)
    return storage_path
