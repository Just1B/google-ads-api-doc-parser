import unittest

from tests import (
    CAMPAIGN_SPECIFIED_YES,
    CAMPAIGN_SPECIFIED_NO,
    KEYWORD_VIEW_SPECIFIED_YES,
    KEYWORD_VIEW_SPECIFIED_NO,
)

from config import Config

from main import is_metric_page, get_parsed_html, get_comments, get_fields


class TestRessourcesWithMetrics(unittest.TestCase):
    def test_campaign_is_metrics_page(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/campaign"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), True)

    def test_customer_is_metrics_page(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/customer"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), True)

    def test_keyword_view_is_metrics_page(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/keyword_view"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), True)

    def test_ad_group_criterion_without_metrics(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/ad_group_criterion"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), False)

    def test_feed_without_metrics(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/feed"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), False)

    def test_asset_without_metrics(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/asset"

        soup = get_parsed_html(target_url=TARGET_URL)

        comments = get_comments(soup)

        self.assertEqual(is_metric_page(comments), False)

    def test_campaign_fields_with_specified(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/campaign"

        response = get_fields(
            target_url=TARGET_URL, ressource_name="campaign", specified="yes"
        )

        self.assertEqual(set(response), set(CAMPAIGN_SPECIFIED_YES))

    def test_campaign_fields_not_specified(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/campaign"

        response = get_fields(
            target_url=TARGET_URL, ressource_name="campaign", specified="no"
        )

        self.assertEqual(set(response), set(CAMPAIGN_SPECIFIED_NO))

    def test_keyword_view_fields_with_specified(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/keyword_view"

        response = get_fields(
            target_url=TARGET_URL, ressource_name="keyword_view", specified="yes"
        )

        self.assertEqual(set(response), set(KEYWORD_VIEW_SPECIFIED_YES))

    def test_keyword_view_fields_not_specified(self):

        TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/keyword_view"

        response = get_fields(
            target_url=TARGET_URL, ressource_name="keyword_view", specified="no"
        )

        self.assertEqual(set(response), set(KEYWORD_VIEW_SPECIFIED_NO))