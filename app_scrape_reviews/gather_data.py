"""Module that gathers the reviews for a given app"""
from dataclasses import dataclass
import pandas as pd
from google_play_scraper import Sort, reviews

COLUMNS = ['reviewId', 'content', 'score',
       'thumbsUpCount', 'reviewCreatedVersion', 'at', 'replyContent',
       'repliedAt', 'appVersion']

@dataclass
class GoogleScrapInfo:
    """Class that keeps the parameters for the scraper function"""
    app_name: str
    language: str
    country: str
    sort: Sort
    count: int = None
    filter_score_with: int = None

def create_info(config: dict, sort: Sort, filter_score_with=None):
    """Function that creates a GoogleScrapInfo object"""
    return GoogleScrapInfo(
        app_name=config["app_name"],
        language=config["language"],
        country=config["country"],
        sort=sort,
        count=config["count"],
        filter_score_with=filter_score_with
    )


def create_reviews_dataframe(information: GoogleScrapInfo) -> pd.DataFrame:
    """Gets reviews from google play and makes a dataframe out of them"""
    reviews_result, continuation_token = reviews(
        information.app_name,
        lang=information.language,
        country=information.country,
        sort=information.sort,
        count=information.count,
        filter_score_with=information.filter_score_with
    )
    reviews_result, _ = reviews(
        information.app_name,
        continuation_token=continuation_token # defaults to None(load from the beginning)
    )
    return pd.DataFrame.from_dict(reviews_result)[COLUMNS]
