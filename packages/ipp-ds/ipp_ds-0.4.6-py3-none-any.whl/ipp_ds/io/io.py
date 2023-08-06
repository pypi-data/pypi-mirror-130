import tempfile
from pyarrow.parquet import read_schema
from pyarrow.parquet import read_table as pa_read_table
from io import BytesIO, StringIO
from urllib.request import urlretrieve
from pptx import Presentation
from thinkcell import Thinkcell
import json
import pandas as pd
import numpy as np
import re
import gc
import os

from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

import logging
import fnmatch

from .io_utils import *

# Set the logging level for all azure-* libraries
logger = logging.getLogger('azure')
logger.setLevel(logging.ERROR)

import warnings
warnings.filterwarnings('ignore')

DEFAULT_SERVICE_KWARGS = json.loads(os.getenv('DEFAULT_SERVICE_KWARGS','{}'))
DEFAULT_CONN_KWARGS = json.loads(os.getenv('DEFAULT_CONN_KWARGS','{}'))
DEFAULT_BLOB_SERVICE = os.getenv('DEFAULT_BLOB_SERVICE','gen2')

def create_blob_service(uri, conn_type=DEFAULT_BLOB_SERVICE,
                        service_kwargs=DEFAULT_SERVICE_KWARGS):

    credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

    account_name = uri.replace('abfs://','').split('.')[0]

    if conn_type == 'gen2':
        dlService = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net",
                                          credential = credential,
                                          **service_kwargs)

    if conn_type == 'blob':
        dlService = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                      credential = credential,
                                      **service_kwargs)

    return dlService

def to_any(byte_stream, uri,
           encoding='utf-8', conn_type=DEFAULT_BLOB_SERVICE,
           **upload_kwargs):

    byte_stream.seek(0)

    service_client = create_blob_service(uri=uri, conn_type=conn_type)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    if conn_type == 'gen2':
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        file_client = file_system_client.get_file_client(file_path=blob_name)

    if conn_type == 'blob':
        file_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        if conn_type == 'gen2':
            if isinstance(byte_stream, BytesIO):
                file_client.upload_data(byte_stream, overwrite=True, **upload_kwargs)
            else:
                file_client.upload_data("".join(byte_stream.readlines()), overwrite=True, encoding=encoding, **upload_kwargs)

        if conn_type == 'blob':
            if isinstance(byte_stream, BytesIO):
                file_client.upload_blob(byte_stream, overwrite=True, **upload_kwargs)
            else:
                file_client.upload_blob("".join(byte_stream.readlines()), overwrite=True, encoding=encoding, **upload_kwargs)

    finally:

        file_client.close()
        del file_client

        if conn_type == 'gen2':
            file_system_client.close()
            del file_system_client

        service_client.close()
        del service_client

        gc.collect()

def read_any(uri, func, conn_type = DEFAULT_BLOB_SERVICE, **kwargs):

    """ Get a dataframe from Parquet file on blob storage """
    service_client = create_blob_service(uri, conn_type = conn_type)
    container_name = uri.split('/')[3]
    blob_name = '/'.join(uri.split('/')[4:])

    if conn_type == 'gen2':
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        file_client = file_system_client.get_file_client(blob_name)

    if conn_type == 'blob':
        file_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    try:
        byte_stream = BytesIO()

        if conn_type == 'gen2':
            byte_stream.write(file_client.download_file().readall())
        if conn_type == 'blob':
            byte_stream.write(file_client.download_blob().readall())

    except:
        byte_stream.close()

        file_client.close()
        del file_client

        if conn_type == 'gen2':
            file_system_client.close()
            del file_system_client

        service_client.close()
        del service_client

        gc.collect()

        raise Exception(f'Could not find blob in {blob_name}')

    try:

        byte_stream.seek(0)
        df = func(byte_stream, **kwargs)

    finally:

        byte_stream.close()

        file_client.close()
        del file_client

        if conn_type == 'gen2':
            file_system_client.close()
            del file_system_client

        service_client.close()
        del service_client

        gc.collect()

    return df

def to_parquet(df: pd.DataFrame, uri, conn_type = DEFAULT_BLOB_SERVICE,
               upload_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    if 'use_deprecated_int96_timestamps' in kwargs:
        kwargs.pop('use_deprecated_int96_timestamps')

    byte_stream = BytesIO()
    df.to_parquet(byte_stream, use_deprecated_int96_timestamps=True, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type, **upload_kwargs)

def to_excel(df: pd.DataFrame, uri, conn_type = DEFAULT_BLOB_SERVICE, mode='pandas',
             upload_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    #Csv writing currently not supported in blob conn_type
    if mode == 'pyexcelerate':
        logger.warn(f'to_excel method is currently not supported with pyexcelerate mode')
        mode = 'pandas'

    byte_stream = BytesIO()
    func_dict = {'pandas': pd.DataFrame.to_excel, 'pyexcelerate': pyx_to_excel}
    func_dict[mode](df, byte_stream, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type, **upload_kwargs)

def to_ppttc(df, uri, conn_type = DEFAULT_BLOB_SERVICE,
             upload_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_pptc method is currently not supported with blob conn_type')
        conn_type = 'gen2'

    byte_stream = StringIO()
    func = json.dump
    func(obj=df.charts, fp=byte_stream, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type, **upload_kwargs)

def to_csv(df: pd.DataFrame, uri, conn_type = DEFAULT_BLOB_SERVICE, encoding='utf-8',
           upload_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    #Csv writing currently not supported in blob conn_type
    if conn_type == 'blob':
        logger.warn(f'to_csv method is currently not supported with blob conn_type')
        conn_type = 'gen2'

    byte_stream = StringIO()
    df.to_csv(byte_stream, encoding=encoding, **kwargs)
    return to_any(byte_stream, uri, encoding=encoding, conn_type=conn_type, **upload_kwargs)

def to_pptx(df, uri, conn_type = DEFAULT_BLOB_SERVICE, upload_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    byte_stream = BytesIO()
    df.save(byte_stream, **kwargs)

    return to_any(byte_stream, uri, conn_type=conn_type, **upload_kwargs)

def glob(uri, conn_kwargs=DEFAULT_CONN_KWARGS, **kwargs):

    blob_service = create_blob_service(uri, conn_type='gen2')
    container_name = uri.split('/')[3]
    container_url = '/'.join(uri.split('/')[:4])
    blob_name = '/'.join(uri.split('/')[4:])
    container_client = blob_service.get_file_system_client(file_system=container_name)

    if '*' in blob_name:
        path = blob_name.split("*")[0]
        path_suffix = '*'.join(blob_name.split("*")[1:])
    else:
        path = blob_name.rstrip('/')
        path_suffix = ''

    try:
        list_blobs = [container_url+'/'+unit.name for unit in container_client.get_paths(path=path, **kwargs, **conn_kwargs)]
    except:
        new_path = '/'.join(path.split('/')[:-1])
        path_suffix = path.split('/')[-1]+'*'+path_suffix
        list_blobs = [container_url+'/'+unit.name for unit in container_client.get_paths(path=new_path, **kwargs, **conn_kwargs)]

    result_list = []

    if len(list_blobs) == 0:
        print('Does not have any file that match the specified criteria')
        return result_list

    if len(path_suffix) == 0:
        return list_blobs

    else:
        path_suffix = fnmatch.translate(path_suffix)
        for i in np.array(list_blobs):
            match = re.search(path_suffix, i)
            if match is not None:
                result_list.append(i)

    return result_list

def read_cols(uri, conn_type = DEFAULT_BLOB_SERVICE, **kwargs):
    # Lê estritamente os metadados do parquet

    if ('.parquet' not in uri):
        raise TypeError("O formato do arquivo precisa ser parquet.")

    func = read_schema
    func.memory_map = True

    schema = read_any(uri, func, conn_type=conn_type)
    schema = pd.DataFrame(({"Column": name, "dtype": str(pa_dtype)} for name, pa_dtype in zip(schema.names, schema.types)))
    schema.dropna(inplace = True)

    return schema

def pa_read_parquet(stream, **kwargs):

    to_pandas_kwargs = {}
    params = ['timestamp_as_object']

    for param in params:
        if param in kwargs:
            to_pandas_kwargs[param] = kwargs.pop(param)

    return pa_read_table(stream, **kwargs).to_pandas(**to_pandas_kwargs)

def read_parquet(uri, mode='pandas', conn_type = DEFAULT_BLOB_SERVICE, **kwargs):
    func = {'pandas': pd.read_parquet, 'pyarrow':pa_read_parquet}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)


def read_csv(uri, mode='pandas', conn_type = DEFAULT_BLOB_SERVICE, **kwargs):
    func = {'pandas': pd.read_csv}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)


def read_excel(uri, mode='pandas', conn_type = DEFAULT_BLOB_SERVICE, **kwargs):

    # A partir de uma determinada versao, o xlrd parou de dar suporte a xlsx.
    # Usa-se por padrão a engine openpyxl. Se ela não for passada, agnt força a engine
    if ('.xlsx' in uri) & ('engine' not in kwargs):
        kwargs['engine'] = 'openpyxl'

    func = {'pandas': pd.read_excel}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)

def read_pptx(uri, mode='pptx', conn_type = DEFAULT_BLOB_SERVICE, **kwargs):
    func = {'pptx': Presentation}
    func = func[mode]
    return read_any(uri, func, conn_type=conn_type, **kwargs)

def read_tc_template(uri, _format='pptx', mode='thinkcell', conn_type = DEFAULT_BLOB_SERVICE, **kwargs):
    df = Thinkcell()
    df.add_template(uri)
    return df

def read_url(uri, sas_token, _format, **kwargs):
    """Read from a container with SAS token """
    with tempfile.NamedTemporaryFile() as tf:
        url_tok = uri + sas_token
        urlretrieve(url_tok, tf.name)
        df = read_any(uri=tf.name, _format=_format, **kwargs)
        return df


def file_exists(path):
    """ Checa se o arquivo informado existe """
    last_dir = path.replace(path.split('/')[-1], "*")

    if path in glob(last_dir):
        return True
    else:
        return False
