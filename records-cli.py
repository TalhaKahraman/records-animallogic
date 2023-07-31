import argparse
import requests
import json
import pandas as pd

parser = argparse.ArgumentParser(
                    prog='records-cli',
                    description='records-cli allows you to get, filter, and add user data.')

parser.add_argument('-g', '--get', help='get method to fetch records data.', action='store_true')
parser.add_argument('-f', '--filter', help='filter value to filter and fetch specific records data.', type=str)
parser.add_argument('-p', '--post', help='post method to add data to the records data set.', action='store_true')

parser.add_argument('-j', '--json', help='Output format type is saved as a json file.', action='store_true')
parser.add_argument('-x', '--xml', help='Output format type is saved as a xml file.', action='store_true')
parser.add_argument('-t', '--text', help='Output format type is printed out as a table.', action='store_true')
parser.add_argument('--name', help='name of person being added to the data set.', type=str)
parser.add_argument('--address', help='address of person being added to the data set.', type=str)
parser.add_argument('--phone_number', help='phone number of person being added to the data set.', type=int)

args = parser.parse_args()

if args.get:
    if args.xml:
        format = 'application/xml'
    else:
        format = 'application/json'
    
    filter = args.filter 
    if filter != None:
        url = f'http://127.0.0.1:5000/filter/{filter}'
    else:
        url = 'http://127.0.0.1:5000/records'

    response = requests.get(url, headers={'Accept': format})

    if args.json:
        response = response.json()
        json_object = json.dumps(response, indent=4)
        with open('data.json', 'w') as outfile:
            outfile.write(json_object)
    
    elif args.xml:
        response = response.content
        with open('data.xml', 'wb') as f:
            f.write(response)

    else:
        response = response.json()
        response_list = response['response']
        records_df = pd.DataFrame.from_records(response_list)
        records_df.set_index('id', inplace=True)
        records_df_str = records_df.to_string()
        print(records_df_str)

elif args.post:
    url = 'http://127.0.0.1:5000/records'
    name = args.name
    address = args.address
    phone_number = args.phone_number
    record_data = {}
    if name and address and phone_number:
        record_data['name'] = name
        record_data['address'] = address
        record_data['phone_number'] = phone_number
        response = requests.post(url, json=record_data, headers={'Accept': 'text/csv'})
        print(response.text)
    else:
        raise ValueError('Missing arguments. Please include all 3 of the following arguments: '
                         'name, address, phone_number')