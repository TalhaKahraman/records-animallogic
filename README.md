API Documentation
-

Link: https://documenter.getpostman.com/view/28846403/2s9Xxtyvks

Instructions
-

1. First we need to create our records database by running create_database.py. This only needs to be run once.
2. Now we can run app.py to initiate our Flask server. We can then make API calls accordingly to get, filter and add data. See API documentation link above for more info.
3. We can also interact with the records data through a command-line interface using records-cli.py. This CLI works closely with the API as it makes requests to it in order to get, filter and add data. Data retrieved here can be saved as a JSON or XML file or can be simply displayed in the console as a text table. More info can be found through the CLI's --help argument.
4. For unit testing, we can run the tests built in unit_test.py by using pytest.
