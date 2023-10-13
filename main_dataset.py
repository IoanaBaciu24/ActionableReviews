"""Module that runs the scraper tool"""
import argparse
from google_play_scraper import Sort
from config import get_json_from_config
from app_scrape_reviews.gather_data import create_info,create_reviews_dataframe


def create_reviwews_on_stars(path_out_template, config):
    """Function that scrapes reviews for each star"""
    for star in range(1, 6):
        p_out = path_out_template.format(star)
        info = create_info(config, Sort.NEWEST, filter_score_with=star)
        df = create_reviews_dataframe(info)
        df.to_csv(p_out, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the config file')
    config_path = parser.parse_args().config
    config_json = get_json_from_config(config_path)
    path_out = config_json["path_out"]
    create_reviwews_on_stars(path_out, config_json)
