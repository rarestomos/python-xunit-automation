import unittest
import uuid

import assertpy
from assertpy import assert_that

from actions.book_endpoint_actions import do_delete_request_for_book, do_post_request_to_create_book
from helpers.books_helper import append_to_books_list
from models.books_model import get_valid_minim_required_create_book_payload
from tests import logger


class DeleteBookTest(unittest.TestCase):

    def setUp(self):
        self.book_ids = []

    def tearDown(self):
        self.all_book_ids_deleted = True
        for book_id in self.book_ids:
            response = do_delete_request_for_book(book_id)
            if not response.ok:
                self.all_book_ids_deleted = False
                logger.debug('Not all books were deleted')
        assertpy.assert_that(self.all_book_ids_deleted).described_as("Not all books were deleted").is_true()

    def test_delete_a_book_using_a_valid_book_id(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        self.book_ids = append_to_books_list(response=response_post, book_ids=self.book_ids)
        book_id = response_post.json()['id']
        response_delete = do_delete_request_for_book(book_id)
        assert_that(response_delete.status_code).is_equal_to(200)
        assert_that(response_delete.json()).is_equal_to(f'Book with id {book_id} has been deleted')
        self.book_ids.remove(book_id)

    def test_try_to_delete_a_book_using_an_invalid_book_id(self):
        not_existing_book_id = str(uuid.uuid4())
        response = do_delete_request_for_book(not_existing_book_id)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to(f'Book with id = {not_existing_book_id} was not found')
