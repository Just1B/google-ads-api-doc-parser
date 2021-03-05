"""
    Author: Justin Baroux
    Github: https://github.com/Just1B
    Description: Export Google ADS API fields and Big Query Schemas
    Version: 1.0
"""

import os
import json
import argparse

import requests

from bs4 import BeautifulSoup, Comment, ResultSet
from bs4 import Comment

from helpers.logger import get_app_logger
from helpers.types import type_to_bq_type

from config import Config

logger = get_app_logger("Google Ads Doc Exporter")


def main():

    logger.info(
        f"""
        _________________________________ 
        |  _____________________________  |
                 
                 GOOGLE ADS API 

                   DOC PARSER            
        | |_____________________________| |
        |_________________________________|
    """
    )

    # Parse arguments.
    parser = argparse.ArgumentParser(
        description="Fetches Google Ads Api documentation fields and types."
    )

    parser.add_argument(
        "-r",
        "--ressource_name",
        help="Google Ads Api Ressource name ( ad_group_criterion , ... ) ",
        required=True,
    )

    parser.add_argument(
        "-s",
        "--specified",
        help="Is ressource_name specified in the FROM clause of your query ?",
        default="no",
    )

    args = parser.parse_args()

    TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/{args.ressource_name}"

    get_fields(target_url=TARGET_URL)


def get_parsed_html(target_url: str):

    try:
        logger.info(f"TARGET_URL : {target_url}\n")

        page = requests.get(target_url)
        soup = BeautifulSoup(page.text, "html.parser")

        return soup

    except requests.exceptions.RequestException as requests_error:
        logger.exception(requests_error)

        raise requests_error

    except Exception as error:
        logger.exception(error)

        raise error


def is_metric_page(comments: ResultSet):

    return Config.SELECTORS_SET.issubset(set(comments))


def get_comments(soup: BeautifulSoup):

    try:

        return soup.find_all(string=lambda text: isinstance(text, Comment))

    except Exception as error:

        raise error


def parse_page_without_metrics(soup: BeautifulSoup):

    logger.info(" ** PARSING PAGE WITHOUT METRICS **\n")

    # blue responsive -> Resource fields

    fields = soup.find_all(True, {"class": ["blue responsive"]})

    text_output = "fields,\n"
    json_output = []

    for field in fields:

        text = field.find("h2").text
        doc_type = field.find_all("code")[1].text

        if "ENUM" in doc_type:
            doc_type = "ENUM"

        text_output += f"{text},\n"
        json_output.append(
            {
                "name": text.replace(".", "_"),
                "type": type_to_bq_type(doc_type),
                "mode": "NULLABLE",
            }
        )

    create_files(filename="fields.csv", content=text_output)
    create_files(filename="schema.json", content=json.dumps(json_output))


def parse_page_with_metrics(soup: BeautifulSoup):

    logger.info(" ** PARSING PAGE WITH METRICS **\n")

    # blue responsive -> Resource fields
    # orange responsive -> Segments
    # green responsive -> Metrics

    # TODO

    # values = soup.find_all(
    #     True, {"class": ["columns blue responsive", "columns green responsive"]}
    # )

    # the second columns blue responsive
    # resource_fields = soup.find_all(True, {"class": ["columns blue responsive"]})[1]
    # resource_fields = soup.select("table.columns.blue.responsive")[1].find_all("a")
    # metrics = soup.select("table.columns.green.responsive")
    # metrics = soup.find_all(True, {"class": ["columns green responsive"]})

    # logger.info(resource_fields)

    # logger.info(metrics)

    # for value in resource_fields:
    #     #     logger.info(value)
    #     text = value.find_all("a")

    #     logger.info(text)

    # logger.info(list_values)

    return True


def get_fields(target_url: str):

    soup = get_parsed_html(target_url=target_url)

    # Find page type by parsing comments
    # Ressources with metrics have a selector ( ressources specified in FROM )
    comments = get_comments(soup)

    metrics_page = is_metric_page(comments)

    parse_page_without_metrics(soup) if not metrics_page else parse_page_with_metrics(
        soup
    )


def create_files(filename, content):

    logger.info(f"CREATING NEW FILE OUTPUT : {filename}\n")

    f = open(filename, "w+")

    f.write(content)

    f.close()


if __name__ == "__main__":
    main()