from flask import Flask, request
from collections import defaultdict
import import_data

app = Flask(__name__)


# on the homepage, show basic navigation and API call instructions in HTML code

@app.route('/')

def instruction():

    return "<h1>Food Truck Website</h1>" \
           "<p>Go to /food_trucks/locationid=(locationid) to see the details of a food truck specified by the location id</p>" \
           "<p>Go to /food_trucks/block=(block) to see a list of food truck details in a given block</p>"\
            "<h1>Food Truck API</h1>" \
            "<p>API Endpoint: /food_trucks</p>"\
            "<p>GET request: parameters: 'locationid' or 'block'</p>"\
            "<p>POST request: parameters: 'locationid' and 'block'; both required; optional to add other parameters</p>"\
            "<p>All parameters are strings</p>"


# an in-memory hash map to store the existing food truck data
# key: id; value: a dictionary that contains the details of the food truck corresponding to the id
# initialize to a dictionary containing the data from a csv file
food_truck_by_id = import_data.prepare_data("Mobile_Food_Facility_Permit.csv", "locationid")

# an in-memory index of the food truck data implemented by a dictionary
# key: the block id
# value: a list of food truck ids which belong to the block
# each time adding a new truck, update both dictionaries
food_truck_by_block = defaultdict(list)
for id, truck in food_truck_by_id.items():
    block_id = truck['block']
    food_truck_by_block[block_id].append(id)

# list all food trucks
def list_food_trucks():
    return {"results": food_truck_by_id}

# create a new food truck
def create_food_truck(new_truck):
    if 'locationid'not in new_truck or 'block' not in new_truck:
        return "INVALID INPUT" # if the locationid or block is not specified, return an error message
    new_truck_id = new_truck['locationid']
    if new_truck_id in food_truck_by_id:
        return "ALREADY EXIST" # if the id is already exists, return an error message
    new_truck_block = new_truck['block']
    food_truck_by_id[new_truck_id] = new_truck
    food_truck_by_block[new_truck_block].append(new_truck_id) # update the block indexing
    return new_truck

# get a food truck by id
def get_food_truck(id):
    if id not in food_truck_by_id:
        return {"results" : {}}
    return {"results": food_truck_by_id[id]}

# get a list of food trucks by block
def get_food_truck_block(id):
    selected_data = [] # there can be more than one food trucks in a given block
    if id not in food_truck_by_block:
        return {"results": {}} # if the given block is invalid, return an empty result
    location_ids = food_truck_by_block[id]
    for id in location_ids:
        if id not in food_truck_by_id:
            return "INTERNAL ERROR" # if an id is in the block dict but not in the orig data, return an error message (this should never happen)
        selected_data.append(food_truck_by_id[id])
    return {"results": selected_data}

# define methods in url /food_trucks: list qualified food trucks in a GET method; add a new food truck in a POST method
@app.route('/food_trucks', methods=['GET', 'POST'])
def food_truck_route():
    if request.method == 'GET':
        locationid = request.args.get('locationid')
        block = request.args.get('block')
        if locationid: # if locationid is set, return corresponding food truck
            return get_food_truck(locationid)
        if block: # if block is set, return correpsonding food truck
            return get_food_truck_block(block)
        return list_food_trucks() # in other cases (no args or irrelevant args) return the whole list
        
    elif request.method == "POST":
        return create_food_truck(request.get_json(force=True))

# define methods in url /food_trucks/locationid=<locationid>: list the food truck of the specified id
@app.route('/food_trucks/locationid=<locationid>', methods=['GET'])
def food_truck_loc_route(locationid):
    if request.method == 'GET':
        return get_food_truck(locationid)

# define methods in url /food_trucks/block=<block>: list food trucks in the specified block
@app.route('/food_trucks/block=<block>', methods=['GET'])
def food_truck_block_route(block):
    if request.method == 'GET':
        return get_food_truck_block(block)
   

if __name__ == '__main__':
    # run on local server with debugger activated
    app.run(host = '127.0.0.1', port = 5000, debug = True)