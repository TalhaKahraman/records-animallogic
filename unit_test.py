import requests
import sqlite3
import pytest
import os
import string
import random

class TestAPIRequests:
    def get_row_count(self):
        records_db_file = os.path.dirname(os.path.abspath(__file__)) + '/records.db'
        conn = sqlite3.connect(records_db_file)
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM records"
        cursor.execute(query)
        result = cursor.fetchone()
        row_count = result[0]
        return row_count

    def parse_data(self, response):
        try:
            response_dict = response.json()
            records = response_dict['response']
            test_user = records[0]
            test_name = test_user['name']
            test_address = test_user['address']
            test_phone_number = test_user['phone_number']
            return records, test_name, test_address, test_phone_number
        except:
            return [],'','', ''

    def test_get_request(self):
        url = 'http://127.0.0.1:5000/records'
        response = requests.get(url)
        records, test_name, test_address, test_phone_number = self.parse_data(response)
        row_count = self.get_row_count()

        assert response.status_code == 200, 'Request failed'
        assert len(records) > 0, 'Something went wrong due to missing data'
        assert test_name == "Test Name", 'missing or incorrect test user name'
        assert test_address == "Test Address", 'missing or incorrect test user address'
        assert test_phone_number == 123456789, 'missing or incorrect test user phone_number'
        assert row_count == len(records), 'number of database and requested data rows not matching'
    
    def test_filter_request(self):
        filter = 'name=Test Name'
        url = f'http://127.0.0.1:5000/filter/{filter}'
        response = requests.get(url)

        records, test_name, test_address, test_phone_number = self.parse_data(response)

        assert response.status_code == 200, 'Request failed'
        assert len(records) > 0, 'Something went wrong due to missing data'
        assert test_name == "Test Name", 'Missing or incorrect test user name'
        assert test_address == "Test Address", 'Missing or incorrect test user address'
        assert test_phone_number == 123456789, 'Missing or incorrect test user phone_number'
    
    def test_post_request(self):
        letters = string.ascii_lowercase
        random_str = ''.join(random.choice(letters) for i in range(10))
        record_data = {}
        record_data['name'] = f'Test {random_str}'
        new_test_name = record_data['name']
        record_data['address'] = 'Test Address'
        record_data['phone_number'] = 123456789

        url = 'http://127.0.0.1:5000/records'
        post_response = requests.post(url, json=record_data)
        print(post_response)

        filter = f'name={new_test_name}'
        url = f'http://127.0.0.1:5000/filter/{filter}'
        get_response = requests.get(url)

        records, test_name, test_address, test_phone_number = self.parse_data(get_response)

        assert post_response.status_code == 201, 'Request failed'
        assert len(records) > 0, 'Something went wrong adding/querying data'
        assert test_name == new_test_name, 'Issue adding test user name'
        assert test_address == 'Test Address', 'Issue adding test user address'
        assert test_phone_number == 123456789, 'Issue adding test user phone_number'