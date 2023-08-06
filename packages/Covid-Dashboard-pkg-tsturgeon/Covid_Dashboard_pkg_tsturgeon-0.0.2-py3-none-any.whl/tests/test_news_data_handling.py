"""
A test document for Tom Sturgeon EMC1400 coursework

This module test most of the covid_news_handling functions

It does not test the following since they call other functions:
    - update_news_articles
    - news_data_return
"""

from covid_dashboard.covid_news_handling import check_list, news_API_request, remove_news, update_news

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news(update_interval = 10, update_name='test')

def test_check_list():
    test_data = [
        {
        'title': "First",
        'content': "test 1"
    },
      {
        'title': "Second",
        'content': "test 2"
    },  {
        'title': "Third",
        'content': "test 3"
    },  {
        'title': "Fourth",
        'content': "test 4"
    },
    ]
    index = check_list(test_data, "Second")
    assert index == 1

def test_remove_news():
    test_data = [
        {
        'title': "First",
        'content': "test 1"
    },
      {
        'title': "Second",
        'content': "test 2"
    },  {
        'title': "Third",
        'content': "test 3"
    },  {
        'title': "Fourth",
        'content': "test 4"
    },
    ]
    test_article = remove_news("Third", test_data)
    answer = {'title':"Third",'content':"test 3"}
    assert test_article == answer
