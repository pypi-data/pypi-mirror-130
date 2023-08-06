"""test_covid_news_handling module

This module exports functions intended to test the functionality of the
covid_news_handling module.

The following functions are not testable for various reasons:
 - news_API_request
 - update_news
 - schedule_news_updates
 - remove_article_by_title
"""

import os

from covid19dashboard import covid_news_handling
from covid19dashboard.config import get_config

def reset_test_environment():
    """
    This function resets the test environment by resetting default values.
    """
    covid_news_handling.news_articles = []
    covid_news_handling.removed_articles = []

    config = get_config()
    if "NEWS_API_KEY" in os.environ:
        config["news_api_key"] = os.environ["NEWS_API_KEY"]

def test_add_removed_article():
    """
    This test ensures that add_removed_article adds an article's url to the removed list
    """
    reset_test_environment()

    test_url = "https://www.google.com"
    test_article = {
        "url": test_url
    }

    covid_news_handling.add_removed_article(test_article)

    assert covid_news_handling.removed_articles == [ test_url ]

def test_news_API_request():
    reset_test_environment()

    assert covid_news_handling.news_API_request()
    assert (
        covid_news_handling.news_API_request('Covid COVID-19 coronavirus')
        == covid_news_handling.news_API_request()
    )

def test_update_news():
    reset_test_environment()

    covid_news_handling.update_news('test')
