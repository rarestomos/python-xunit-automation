import unittest
import assertpy

from assertpy import assert_that

from actions.book_endpoint_actions import do_post_request_to_create_book, do_delete_request_for_book
from helpers.books_helper import update_book_payload
from models.books_model import (get_valid_minim_required_create_book_payload,
                                get_valid_with_all_params_create_book_payload,
                                get_add_book_payload_without_parameter)
from tests import logger


class CreateBookTest(unittest.TestCase):

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

    def test_create_book_only_with_the_required_parameters(self):
        request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        assert_that(response_post.json()) \
            .has_name(request_body['name']) \
            .has_author(request_body['author']) \
            .has_description(None) \
            .has_cover(None)

    def test_create_book_with_all_parameters(self):
        request_body = get_valid_with_all_params_create_book_payload()
        response_after_post = do_post_request_to_create_book(request_body)
        assert_that(response_after_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_after_post.json()['id'])
        assert_that(response_after_post.json()).is_equal_to(request_body, ignore="id")

    def test_create_book_using_existing_author_but_different_title(self):
        first_request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(first_request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        second_request_body = update_book_payload(payload=get_valid_minim_required_create_book_payload(),
                                                  author=first_request_body["author"])
        response_second_post = do_post_request_to_create_book(second_request_body)
        assert_that(response_second_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_second_post.json()['id'])
        assert_that(response_second_post.json()) \
            .has_name(second_request_body['name']) \
            .has_author(second_request_body['author']) \
            .has_description(None) \
            .has_cover(None)

    def test_create_book_using_existing_title_different_author(self):
        first_request_body = get_valid_minim_required_create_book_payload()
        response_post = do_post_request_to_create_book(first_request_body)
        assert_that(response_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_post.json()['id'])
        second_request_body = update_book_payload(payload=get_valid_minim_required_create_book_payload(),
                                                  name=first_request_body["name"])
        response_second_post = do_post_request_to_create_book(second_request_body)
        assert_that(response_second_post.status_code).described_as('"Create Book" request failed!').is_equal_to(200)
        self.book_ids.append(response_second_post.json()['id'])
        assert_that(response_second_post.json()) \
            .has_name(second_request_body['name']) \
            .has_author(second_request_body['author']) \
            .has_description(None) \
            .has_cover(None)

    def test_try_to_add_several_books_with_the_same_name_and_author(self):
        request_body = get_valid_minim_required_create_book_payload()
        do_post_request_to_create_book(request_body)
        response_post_again = do_post_request_to_create_book(request_body)
        assert_that(response_post_again.status_code).is_equal_to(400)
        assert_that(response_post_again.json()).is_equal_to(f"Book with name: {request_body['name']} writen by "
                                                            f"author: {request_body['author']} already exists")

    def test_try_to_add_a_new_book_without_its_title(self):
        request_body = get_add_book_payload_without_parameter(param='name')
        response = do_post_request_to_create_book(request_body)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to(f"'name' is required")

    def test_try_to_add_a_new_book_without_its_author(self):
        request_body = get_add_book_payload_without_parameter(param='author')
        response = do_post_request_to_create_book(request_body)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to(f"'author' is required")
