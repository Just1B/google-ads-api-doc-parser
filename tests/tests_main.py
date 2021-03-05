import unittest

from config import Config

from main import is_metric_page, get_parsed_html, get_comments


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