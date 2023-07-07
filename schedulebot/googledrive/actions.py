"""
The module actions:
Defines functions for the interaction of the Telegram bot
with the data of the working Google folder using the Google APIs.
"""

import logging
import asyncio
from typing import Callable, Optional, Union, List, Dict

from aiogoogle import Aiogoogle

from schedulebot.googledrive.credentials import CREDS


def only_id_and_name(func_doc_files) -> Callable:
    """
    Separates `id` and `name` from among file data.

    :return: If success, a list of dicts containing the Document file data
             with parameters `id` and `name`.
    """
    async def wrapper() -> Optional[List[Dict]]:
        doc_files = await func_doc_files()
        return [{'id': item['id'], 'name': item['name']} for item in doc_files]
    return wrapper


def only_document(func_list_files) -> Callable:
    """
    Decorator for func get_list_files().

    Looks for Document files.
    (from the results of get_list_files() separates files with the extension `.document`).

    :return: If success, a list of dicts containing the Document file data.
    """
    async def wrapper() -> Union[List[Dict], List[None]]:
        list_files = await func_list_files()
        file_document = list(filter(lambda x: x['mimeType'].split('.')[-1] == 'document',
                                    list_files))
        return file_document if file_document else []
    return wrapper


@only_id_and_name
@only_document
async def get_list_files() -> Union[List[Dict], List[None]]:
    """
    Getting a list of Google folder's files with their data.

    :return: If the folder is not empty, a list of dicts containing the file data.
    """
    async with Aiogoogle(service_account_creds=CREDS) as aiogoogle:
        drive = await aiogoogle.discover('drive', 'v3')
        response: dict = await aiogoogle.as_service_account(
            drive.files.list(),
        )
        lst_files = response.get('files')
        return lst_files if lst_files else []


if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=3)
    files = asyncio.run(get_list_files())
    pp.pprint(files)
