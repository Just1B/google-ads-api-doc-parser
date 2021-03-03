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
from bs4 import BeautifulSoup

from helpers.logger import get_app_logger
from helpers.types import type_to_bq_type

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

    MAIN_URL = "https://developers.google.com/google-ads/api/fields"

    VERSION = "v6"

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

    args = parser.parse_args()

    TARGET_URL = f"{MAIN_URL}/{VERSION}/{args.ressource_name}"

    fetch_fields(target_url=TARGET_URL)


def fetch_fields(target_url: str):

    try:

        logger.info(f"TARGET_URL : {target_url}")

        page = requests.get(target_url)
        soup = BeautifulSoup(page.text, "lxml")

        fields = soup.find_all(class_="blue responsive")

        parsed = []
        for field in fields:

            text = field.find("h2").text
            doc_type = field.find_all("code")[1].text

            if "ENUM" in doc_type:
                doc_type = "ENUM"

            parsed.append(
                {
                    "field": text,
                    "bq_name": text.replace(".", "_"),
                    "type": type_to_bq_type(doc_type),
                }
            )

        create_outputs(parsed=parsed)

    except requests.exceptions.RequestException as requests_error:
        logger.exception(requests_error)

    except Exception as error:
        logger.exception(error)


def create_outputs(parsed: list):

    try:

        text_output = "fields,\n"
        json_output = []

        for p in parsed:

            text_output += f"{p['field']},\n"
            json_output.append(
                {"name": p["bq_name"], "type": p["type"], "mode": "NULLABLE"}
            )

        create_files(filename="fields.csv", content=text_output)
        create_files(filename="schema.json", content=json.dumps(json_output))

    except Exception as error:
        logger.exception(error)


def create_files(filename, content):

    logger.info(f"CREATING NEW FILE OUTPUT : {filename}")

    f = open(filename, "w+")

    f.write(content)

    f.close()


if __name__ == "__main__":
    main()