from helpers import logger


def append_to_books_list(response, book_ids):
    if response.status_code == 200:
        book_ids.append(response.json()['id'])
    else:
        logger.debug(f'Create book failed. Status Code: {response.status_code} and the error was:'
                     f' {response.text}')
    return book_ids
