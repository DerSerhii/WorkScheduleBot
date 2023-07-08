"""
The module represents functions for the interaction of the bot
with the data of the working Google folder using the Google APIs.
"""

import asyncio
from typing import Callable, List, Dict

from aiogoogle import Aiogoogle, GoogleAPI

from schedulebot.googledrive.credentials import CREDS


def separate_id_and_name_in_doc_files(func) -> Callable:
    """
    Decorator for :func:`separate_document_files.<locals>.get_list_doc_files`.

    :return: Decorated function.
    """
    async def get_list_id_name_doc_files() -> List[Dict]:
        """
        Retrieves a list of Document files with `id` and `name` metadata from Google folder.

        :return: A list of dicts containing `id` and `name` Document file metadata,
            or an empty list if there are none.
        :rtype: :obj:`typing.List[typing.Dict]`.
        """
        doc_files = await func()
        return [{'id': item['id'], 'name': item['name']} for item in doc_files]
    return get_list_id_name_doc_files


def separate_document_files(func) -> Callable:
    """
    Decorator for :func:`get_list_files`.

    :return: Decorated function.
    """
    async def get_list_doc_files() -> List[Dict]:
        """
        Retrieves a list of Document files with their metadata from Google folder.

        :return: A list of dicts containing Document file metadata, or an empty list if there are none.
        :rtype: :obj:`typing.List[typing.Dict]`
        """
        lst_files: List[Dict] = await func()
        return list(filter(lambda x: x['mimeType'].split('.')[-1] == 'document', lst_files))
    return get_list_doc_files


@separate_id_and_name_in_doc_files
@separate_document_files
async def get_list_files() -> List[Dict]:
    """
    Retrieves a list of files with their metadata from Google folder.

    :return: A list of dicts containing file metadata, or an empty list if there are none.
    :rtype: :obj:`typing.List[typing.Dict]`
    """
    async with Aiogoogle(service_account_creds=CREDS) as aiogoogle:
        drive: GoogleAPI = await aiogoogle.discover('drive', 'v3')
        response: dict = await aiogoogle.as_service_account(drive.files.list())
        return response.get('files', [])


if __name__ == "__main__":
    import pprint
    # Use it to check if the Google API is working.
    # If you need to see a list of all files or all metadata, comment out decorators.
    files = asyncio.run(get_list_files())
    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(files)
