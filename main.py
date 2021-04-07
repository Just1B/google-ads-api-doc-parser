"""
    Author: Justin Baroux
    Github: https://github.com/Just1B
    Description: Export Google ADS API fields and Big Query Schemas
    Version: 1.1
"""

import os
import json
import argparse

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

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
        choices=["yes", "no"],
        default="no",
    )

    args = parser.parse_args()

    logger.info(
        f"RESSOURCE : {args.ressource_name} - SPECIFIED IN FROM CLAUSE : {args.specified} \n"
    )

    TARGET_URL = f"{Config.MAIN_URL}/{Config.API_VERSION}/{args.ressource_name}"

    get_fields(
        target_url=TARGET_URL,
        ressource_name=args.ressource_name,
        specified=args.specified,
    )


def get_parsed_html(target_url: str, ressource_name: str):

    try:
        logger.info(f"TARGET_URL : {target_url}\n")

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(target_url)
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, "html.parser")

        selects = soup.find_all(class_=Config.SELECTORS_CLASS)

        is_metrics_page = (
            True
            if (
                ressource_name not in Config.WITHOUT_METRICS_EXECPTIONS
                and len(selects) >= 3
            )
            else False
        )

        return (soup, is_metrics_page)

    except Exception as error:
        logger.exception(error)

        raise error


def parse_page_without_metrics(soup: BeautifulSoup):

    logger.info(" ** PARSING PAGE WITHOUT METRICS **\n")

    # blue responsive -> Resource fields

    fields = soup.find_all(True, {"class": ["blue responsive"]})

    raw = []
    text_output = "fields,\n"
    json_output = []

    for field in fields:

        text = field.find("h2").text
        doc_type = field.find_all("code")[1].text

        if "ENUM" in doc_type:
            doc_type = "ENUM"

        raw.append(text)
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

    return raw


def parse_page_with_metrics(soup: BeautifulSoup, ressource_name: str, specified: str):

    logger.info(" ** PARSING PAGE WITH METRICS **\n")

    # blue responsive -> Resource fields
    # orange responsive -> Segments ( NOT USE HERE BUT SAME LOGIC )
    # green responsive -> Metrics

    target_ids = []
    text_output = "fields,\n"
    json_output = []

    # the second columns blue responsive
    resource_fields = soup.select("table.columns.blue.responsive")[1].find_all("a")

    for r in resource_fields:
        target_ids.append(f"{ressource_name}.{r.text}")

    metrics = soup.select("table.columns.green.responsive")[0].find_all("a")

    for r in metrics:

        comment = r.findAll(text=lambda text: isinstance(text, Comment))

        if specified == "no":
            target_ids.append(f"metrics.{r.text}")

        elif specified == "yes" and comment[0] == Config.SELECTORS["yes"]:
            target_ids.append(f"metrics.{r.text}")

    for target_id in target_ids:

        doc_type = (
            soup.find(id=target_id)
            .find_parent()
            .find_parent()
            .find_parent()
            .find_all("code")[1]
            .text
        )

        text_output += f"{target_id},\n"
        json_output.append(
            {
                "name": target_id.replace(".", "_"),
                "type": type_to_bq_type(doc_type),
                "mode": "NULLABLE",
            }
        )

    create_files(filename="fields.csv", content=text_output)
    create_files(filename="schema.json", content=json.dumps(json_output))

    return target_ids


def get_fields(target_url: str, ressource_name: str, specified: str):

    (soup, is_metric_page) = get_parsed_html(
        target_url=target_url, ressource_name=ressource_name
    )

    return (
        parse_page_without_metrics(soup=soup)
        if not is_metric_page
        else parse_page_with_metrics(
            soup=soup, ressource_name=ressource_name, specified=specified
        )
    )


def create_files(filename, content):

    logger.info(f"CREATING NEW FILE OUTPUT : {filename}\n")

    f = open(filename, "w+")

    f.write(content)

    f.close()


if __name__ == "__main__":
    main()