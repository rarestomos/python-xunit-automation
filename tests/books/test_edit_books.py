import unittest

from assertpy import assert_that

from actions.book_endpoint_actions import (do_delete_request_for_book,
                                           do_post_request_to_create_book,
                                           do_put_request_to_update_book)
from helpers.books_helper import update_book_payload
from models.books_model import get_valid_minim_required_create_book_payload
from tests import logger, fake


class EditBookTest(unittest.TestCase):

    def setUp(self):
        self.book_ids = []

    def tearDown(self):
        self.all_book_ids_deleted = True
        for book_id in self.book_ids:
            response = do_delete_request_for_book(book_id)
            if not response.ok:
                self.all_book_ids_deleted = False
                logger.debug('Not all books were deleted')
        assert_that(self.all_book_ids_deleted).described_as("Not all books were deleted").is_true()

    def test_edit_book_details(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        request_body = update_book_payload(payload=request_body, name=fake.text(20), author=fake.name())
        book_id = response_post.json()['id']
        response = do_put_request_to_update_book(book_id=book_id, book=request_body)
        book = response.json()
        request = request_body
        assert_that(response.status_code).is_equal_to(200)
        assert_that(book) \
            .has_name(request['name']) \
            .has_author(request['author']) \
            .has_description(None) \
            .has_cover(None)

    def test_try_to_update_book_with_the_same_details(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        book_id = response_post.json()['id']
        response_put = do_put_request_to_update_book(book_id=book_id, book=request_body)
        book = response_put.json()
        request = request_body
        assert_that(response_put.status_code).is_equal_to(200)
        assert_that(book) \
            .has_name(request['name']) \
            .has_author(request['author']) \
            .has_description(None) \
            .has_cover(None)
