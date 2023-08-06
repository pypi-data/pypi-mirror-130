"""
    Contains the general methods for manipulating files.
"""

# import json
# import shutil
import os
import re
import shutil
# from pathlib import Path

import objectUtils as obj
import file_read as read
import file_write as write
import file_search as search
import string_utils as strUtils
from secure_delete import secure_delete
from threading import Thread

# pylint: disable=line-too-long
DEST_PATH_SYNONYMS = ["dest", "dst", "dest path", "destination", "destination path", "dst path", "target", "target path"]
SRC_PATH_SYNONYMS = ["source", "src", "src path", "source path", "file path"]

# todo - DOCUMENTATION FOR METHODS


def get_data(file_path, **kwargs):
    '''
        Get data associated to the file_path provided.

        ----------
        Arguments
        -----------------
        `file_path`=cwd {str}
            The path to the file.

        Keyword Arguments
        -----------------

            `exclude`=[] {list}
                A list of keys to exclude from the returning dictionary.
                This is primarily useful for limiting the time/size of the operation.

        Return
        ----------
        `return` {str}
            A dictionary containing the file's data.
    '''
    exclude = obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    file_data = {}
    file_data['file_name'] = os.path.basename(file_path)
    ext = os.path.splitext(file_data['file_name'])
    file_data['extension'] = ext[1]
    file_data['name_no_ext'] = os.path.basename(file_path).replace(file_data['extension'], '')
    file_data['file_path'] = file_path

    if 'dir_path' not in exclude:
        file_data['dir_path'] = os.path.dirname(file_path)
    if 'access_time' not in exclude:
        file_data['access_time'] = os.path.getatime(file_path)
    if 'modified_time' not in exclude:
        file_data['modified_time'] = os.path.getmtime(file_path)
    if 'created_time' not in exclude:
        file_data['created_time'] = os.path.getctime(file_path)
    if 'size' not in exclude:
        file_data['size'] = os.path.getsize(file_path)

    return file_data


def exists(file_path):
    '''
        Confirms that the file exists.

        ----------
        `file_path` {str}
            The file path to test.

        ----------
        `return` {bool}
            True if the file exists, False otherwise.
    '''
    if os.path.isfile(file_path) is True:
        return True
    else:
        return False


def delete(file_path, **kwargs):
    '''
        Deletes a file

        ----------

        Arguments
        -------------------------
        `file_path` {string}
            The path to the file that will be deleted.

        Keyword Arguments
        -------------------------
        [`shred`=False] {bool}
            if True, the file is shredded and securely deleted.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 12:12:08
        `memberOf`: file
        `version`: 1.0
        `method_name`: delete
    '''
    shred = obj.get_kwarg(["shred", "secure"], False, (bool), **kwargs)
    success = False
    if exists(file_path) is True:
        try:
            if shred is True:
                secure_delete.secure_random_seed_init()
                secure_delete.secure_delete(file_path)
            else:
                os.remove(file_path)
        except PermissionError as error:
            print(f"Failed to delete {file_path}, {error}")
            success = True
    else:
        success = True

    if exists(file_path) is False:
        success = False
    return success


def import_project_settings(file_name):
    settings_path = file_name
    if exists(settings_path) is False:
        settings_path = search.by_name(file_name, os.getcwd(), exact_match=False)
        if settings_path is False:
            return False
    return read.as_json(settings_path)


def _parse_copy_data_from_obj(obj):
    data = {
        "src_path": None,
        "dst_path": None,
    }
    if isinstance(obj, (tuple, list)):
        if len(obj) == 2:
            data['src_path'] = obj[0]
            data['dst_path'] = obj[1]
        else:
            print(f"Invalid list/tuple provided for copy file. Must be [source_file_path, destination_file_path]")
    if isinstance(obj, (dict)):
        for syn in SRC_PATH_SYNONYMS:
            synvar = obj._gen_variations(syn)
            for sv in synvar:
                if sv in obj:
                    data['src_path'] = obj[sv]
        for syn in DEST_PATH_SYNONYMS:
            synvar = obj._gen_variations(syn)
            for sv in synvar:
                if sv in obj:
                    data['dst_path'] = obj[sv]

    if exists(data['src_path']) is False:
        print(f"Invalid source path provided, {data['src_path']} could not be found.")
    return data


def rename(src_path, dst_path):
    success = False
    if exists(src_path):
        os.rename(src_path, dst_path)
        success = True
    return success


def copy(src, dest=False, **kwargs):
    '''
        Copy a file from one location to another

        ----------

        Arguments
        -------------------------
        `src` {string|list|tuple|dict}
            The path to the file that will be copied.

            if it is a list/tuple:
                [src_path,dst_path]

                or nested lists [one level max.]

                [[src_path,dst_path],[src_path,dst_path]]

                or a list of dictionaries, lists and/or tuples

                [{src_path:"xx",dst_path:"xx"},[src_path,dst_path]]

            if it is a dictionary:
                The dictionary must have at least one of these keys or variation of it:

                ["source", "src", "src path", "source path", "file path"]

                ["dest", "dst", "dest path", "destination", "destination path", "dst path", "target", "target path"]


        [`src`=False] {string}
            Where to copy the source file to.

            if False, it is assumed that the src is a list,tuple, or dictionary.

        Keyword Arguments
        -------------------------
        [`threading`=True] {bool}
            If True, and there are more files than "min_thread_threshold", then the copy task is divided into threads.

            If False, the files are copied one at a time.

        [`max_threads`=15] {int}
            The total number of threads allowed to function simultaneously.  

        [`min_thread_threshold`=100] {int}
            There must be this many files to copy before threading is allowed.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 12:39:45
        `memberOf`: file
        `version`: 1.0
        `method_name`: copy
    '''

    threading = obj.get_kwarg(["threading"], True, (bool), **kwargs)
    max_threads = obj.get_kwarg(["max_threads"], 15, (int), **kwargs)
    min_thread_threshold = obj.get_kwarg(["min thread threshold", "min files thread"], 100, (int), **kwargs)

    copy_list = []
    if dest is False:
        if isinstance(src, (list, tuple, dict)):
            if isinstance(src, (list, tuple)):
                for item in src:
                    copy_obj = _parse_copy_data_from_obj(item)
                    if copy_obj['src_path'] is not None and copy_obj['dst_path'] is not None:
                        copy_list.append(_parse_copy_data_from_obj(item))
            if isinstance(src, (dict)):
                copy_obj = _parse_copy_data_from_obj(item)
                if copy_obj['src_path'] is not None and copy_obj['dst_path'] is not None:
                    copy_list.append(_parse_copy_data_from_obj(item))
    else:
        copy_obj = _parse_copy_data_from_obj([src, dest])
        copy_list.append(copy_obj)

    if threading is True:
        if len(copy_list) >= min_thread_threshold:
            _thread_copy_files(copy_list, max_threads=max_threads, min_thread_threshold=min_thread_threshold)
            return

    _copy_files_from_array(copy_list)


def _copy_files_from_array(files):
    for file in files:
        os.makedirs(os.path.dirname(file['dst_path']), exist_ok=True)
        shutil.copy2(file['src_path'], file['dst_path'])
    return True


def _thread_copy_files(files, **kwargs):
    max_threads = obj.get_kwarg(["max_threads"], 15, (int), **kwargs)
    min_thread_threshold = obj.get_kwarg(["min thread threshold", "min files thread"], 100, (int), **kwargs)

    if len(files) <= min_thread_threshold:
        max_threads = 1

    files_per_thread = round(len(files) / max_threads)
    threads = []
    for idx in range(max_threads):
        start_idx = files_per_thread * idx
        end_idx = start_idx + files_per_thread
        if end_idx > len(files):
            end_idx = len(files)
        files_array = files[start_idx:end_idx]
        threads.append(Thread(target=_copy_files_from_array, args=(files_array,)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return
