import unittest
import warnings

from tests import (
    CAMPAIGN_SPECIFIED_YES,
    CAMPAIGN_SPECIFIED_NO,
    KEYWORD_VIEW_SPECIFIED_YES,
    KEYWORD_VIEW_SPECIFIED_NO,
)

from config import Config

from main import get_parsed_html, get_fields


class TestRessourcesWithMetrics(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore")

    def test_is_metrics_page(self):

        targets = ["video", "campaign", "customer", "keyword_view"]

        for target in targets:

            with self.subTest(msg=f"Checking {target} is a page with metrics."):

                TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/{target}"

                soup, is_metric_page = get_parsed_html(
                    target_url=TARGET_URL, ressource_name=target
                )

                self.assertEqual(is_metric_page, True)

    def test_without_metrics_page(self):

        targets = ["ad_group_criterion", "feed", "asset", "keyword_plan"]

        for target in targets:

            with self.subTest(msg=f"Checking {target} is a page without_metrics."):

                TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/{target}"

                soup, is_metric_page = get_parsed_html(
                    target_url=TARGET_URL, ressource_name=target
                )

                self.assertEqual(is_metric_page, False)

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