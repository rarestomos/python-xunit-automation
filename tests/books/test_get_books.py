import uuid
import unittest

from assertpy import assert_that

from actions.book_endpoint_actions import (do_delete_request_for_book,
                                           do_post_request_to_create_book,
                                           do_get_request_for_all_books, do_get_request_for_book)
from models.books_model import (get_valid_minim_required_create_book_payload,
                                get_valid_with_all_params_create_book_payload)
from tests import logger


class GetBookTest(unittest.TestCase):

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

    def test_get_all_books(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        all_books_response = do_get_request_for_all_books()
        assert_that(all_books_response.status_code).is_equal_to(200)
        assert_that(all_books_response.json()[0]).contains('id', 'name', 'author')

    def test_list_of_books_incremented_after_each_new_book_added(self):
        all_books_response = do_get_request_for_all_books()
        number_of_books_before = len(all_books_response.json())
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        all_books_response = do_get_request_for_all_books()
        number_of_books_after = len(all_books_response.json())
        assert_that(number_of_books_after) \
            .described_as('Books list not incremented as expected!') \
            .is_equal_to(number_of_books_before + 1)

    def test_get_details_of_book_added_only_with_the_required_parameters(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        valid_book_id = response_post.json()['id']
        get_book_response = do_get_request_for_book(book_id=valid_book_id)
        book = get_book_response.json()
        assert_that(get_book_response.status_code).is_equal_to(200)
        assert_that(book['id']).is_equal_to(valid_book_id)
        assert_that(book).is_equal_to(request_body, ignore=['id', 'description', 'cover'])

    def test_get_details_of_book_added_with_all_parameters(self):
        request_body = get_valid_with_all_params_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        valid_book_id = response_post.json()['id']
        get_book_response = do_get_request_for_book(book_id=valid_book_id)
        book = get_book_response.json()
        assert_that(get_book_response.status_code).is_equal_to(200)
        assert_that(book['id']).is_equal_to(valid_book_id)
        assert_that(book).is_equal_to(request_body, ignore=['id', 'description', 'cover'])

    def test_try_to_get_book_details_using_not_existing_book_id(self):
        not_existing_book_id = str(uuid.uuid4())
        get_book_response = do_get_request_for_book(book_id=not_existing_book_id)
        assert_that(get_book_response.status_code).is_equal_to(400)
        assert_that(get_book_response.json()).is_equal_to(f'Book with id = {not_existing_book_id} was not found')
