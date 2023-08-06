"""
A test document for Tom Sturgeon EMC1400 coursework

This module test most of the covid_data_handler functions

It does not test the following since they call other functions:
    - update_covid_data
    - covid_data_return
    - test_process_covid_json_data
"""


import json
from covid_dashboard.covid_data_handler import calc_previous_7_days, extract_total_deaths, find_hospital_cases, parse_csv_data, process_covid_json_data, process_covid_csv_data, covid_API_request, schedule_covid_updates

with open('test_data.json', 'r', encoding="utf8") as test_data:
    test_data = json.load(test_data)

local_data = test_data["local"]
national_data = test_data['national']

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    local_data, national_data = covid_API_request()
    assert isinstance(local_data, dict)
    assert isinstance(national_data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_calc_previous_7_days():
    local_answer = calc_previous_7_days(local_data)
    national_answer = calc_previous_7_days(national_data)
    assert local_answer == 868
    assert national_answer == 275399

def test_extract_total_deaths():
    total_deaths = extract_total_deaths(national_data)
    assert total_deaths == 145824

def test_find_hospital_cases():
    hospital_cases = find_hospital_cases(national_data)
    assert hospital_cases == 5784

