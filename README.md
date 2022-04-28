This application provides REST APIs to add new food trucks, get the details of a food truck by locationid, and get the details of food trucks in a given block.

## Prerequisit
### Language and framework

Python3.10 and Flask are used for the API implementation. For setting up an environment to run the server, please refer to the article https://www.linkedin.com/pulse/building-data-science-website-flask-venvanaconda-part1-sushant-rao/

### File list
* `food_truck.py`: the server code that can be run directly in an IDE or via command
* `food_truck_client.py`: the unit test code. The server needs to be running before running the test code
* `import_data.py`: the file containing the function called in the server code to convert data from csv to a dictionary
* `Mobile_Food_Facility_Permit.csv`: data downloaded from https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/data

### Packages and dependencies
The following Python packages are needed to run the server code locally:
* flask
* collections
* csv

The following files need to be included in the same directory as the server code:
* import_data.py
* Mobile_Food_Facility_Permit.csv

To run the test code from the client side, the following packages are needed:
* requests
* unittest

## API
API endpoint: http://127.0.0.1/food_trucks

For `GET` method, the user can choose to pass one of the following data as parameters:
```
{'locationid': [LOCATION_ID]}
```
or
```
{'block': [BLOCK_ID]}
```
If both of the above fields are provided, only the data specified by the `locationid` will be returned. If neither of the above parameters are provided, the complete list of all data will be returned.

If the locationid or the block does not exist, the server will return an empty dictionary.

For `POST` method, the user is required to provide both the fields mentioned above. If either is missing, the server will return `"INVALID INPUT"`. If the locationid already exists in the data, the server will return `"ALREADY EXIST"`.

## Site map
* /: the homepage. Provides basic instructions on the API and navigation in the website
* /food_trucks: API endpoint. Displys all data on the page
* /food_trucks/locationid=\<locationid\>: Displays the food truck specified by the locaitonid (at most one qualified food truck)
* /food_trucks/block=\<blockid\>: Displays the food trucks specified by the block (can be more than one qualified food truck, or none)

The last two pages are not crucial for the APIs, but help testing and debugging.

## Impelmentaion
The main part of the design is the data structure for holding the food truck data. Two dictionaries are used in my implementation. The original data, when imported from csv, was converted to a dictionary, with the key the locationid, and the value the details of the foodtruck. Another dictionary is used to index the original data to quickly find all food trucks in a given block. This dictionary holds keys of blocks, and values of arrays containing the locationids of qualified food trucks.

When adding a new food truck, both dictionaries are updated.

When getting a food truck by locationid, the server searches directly in the original data dictionary.

When getting a list of food trucks by block, the server searches in the block dictionary first. For each locationid in the corresponding value, ther server can populate the response by looking into the original dictionary by that id.

## Testing
Some simple test cases are included in the test file. It checkes when the parameters of a get/post request are valid/invalid, whether the response matches what's expected. The expected responses are obtained by manually searching in the original csv file, and are hard-coded. 

## Future work
### Multithreading
The current server is single-threaded. When there are multiple clients, with each possibly multi-threaded when issuing requests, the server should be able to handle requests concurrently. Synchronization mechanisms will be needed. In particular, since the data is not in a thread-safe database (e.g. SQL), any access (GET or POST) to the data should be treated as a critical section and be protected by a mutex.

### Multiple ids in one request
The current code allows the client to specify one locationid or block per get request. Should it be a common case that clients need to get data for multiple locationids or blocks, the code needs to be adapted to allow for adding multiple ids in one request. Otherwise, a client has to issue multiple requests using the current server, which will reduce the bandwidth for other users and increase latency. Similarly, the current server allows adding one food truck at a time. If clients tend to add more than one at a time, the code needs to be adapted accordingly.

### Auto generated locationid
When adding new food trucks, the client is supposed to provide the locationid. The code can be adapted to meet the needs of auto-generating locationids.

### Error handling
Currently when there are errors in either the request or the server, the error messages are hard-coded. It would be better to raise corresponding HTTP response directly.

### Failure tolerance
The current server saves all data within the program. If the program crashes, all added food trucks from the client side will be gone. One way to avoid it is to write the data to a file periodically, even to make replications on other machines. This way at least part of the newly added data will be recovered when the server is back up. 

Another related feature is to add a signal handler, to deal with the case when the server is terminated manually, the data should be written to one or multiple designated file(s).

### More test cases and auto-generated benchmark
With more features, more test cases are needed. It would help a lot to be able to automatically generate test cases as well as "correct answers" for each test case. 

## References
1. environment setup: https://www.linkedin.com/pulse/building-data-science-website-flask-venvanaconda-part1-sushant-rao/
2. code template: https://www.linode.com/docs/guides/create-restful-api-using-python-and-flask/prog_lang_app.txt
3. client test: https://www.geeksforgeeks.org/get-post-requests-using-python/
4. csv to json: https://www.geeksforgeeks.org/convert-csv-to-json-using-python/

