import requests
import unittest
  
# define the api-endpoint
API_ENDPOINT = "http://127.0.0.1:5000/food_trucks"

# a function to extract results from get requests
def get_results(url, query):
    r = requests.get(url = url, params = query)
    data = r.json()['results']
    return data

# test cases for get requests
get_queries = [
    {'locationid': '1010174'}, # an existing locationid
    {'locationid': '1'}, # a non-existing locationid
    {'block': '0263'}, # a existing block
    {'block': '11'}, # a non-existing block
    # {'aa': 'aa'}, # an invalid query -> should return the whole list
    # {} # a empty query -> should return the whole list
]

# a list of all results from get request test cases
output = []

for query in get_queries:
    out = get_results(API_ENDPOINT, query)
    output.append(out)

# ans to compare with the output
ans_by_id_exist = {'Address': '2386 MISSION ST', 'Applicant': "Julie's Hot Dogs", 'Approved': '', 'ExpirationDate': '', 'FacilityType': 'Truck', 'Fire Prevention Districts': '2', 'FoodItems': 'Hot dogs: bacon-wrapped hot dogs: chicken burgers: energy drinks: water and various other drinks.', 'Latitude': '37.75887999201479', 'Location': '(37.75887999201479, -122.41937920298372)', 'LocationDescription': 'MISSION ST: 19TH ST to 20TH ST (2300 - 2399)', 'Longitude': '-122.41937920298372', 'NOISent': '', 'Neighborhoods (old)': '19', 'Police Districts': '4', 'PriorPermit': '0', 'Received': '20150223', 'Schedule': 'http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=15MFF-0007&ExportPDF=1&Filename=15MFF-0007_schedule.pdf', 'Status': 'REQUESTED', 'Supervisor Districts': '7', 'X': '6006843.48', 'Y': '2104477.073', 'Zip Codes': '28859', 'block': '3596', 'blocklot': '3596119', 'cnn': '9121000', 'dayshours': 'Tu/We/Th:12AM-3AM;Mo-We:12PM-12AM', 'locationid': '1010174', 'lot': '119', 'permit': '15MFF-0007'}
ans_by_id_nexist = {}
ans_by_block_exist = [{'Address': '101 CALIFORNIA ST', 'Applicant': 'MOMO INNOVATION LLC', 'Approved': '10/22/2021 12:00:00 AM', 'ExpirationDate': '11/15/2022 12:00:00 AM', 'FacilityType': 'Truck', 'Fire Prevention Districts': '4', 'FoodItems': "MOMO Spicy Noodle: POPO's Noodle: Spicy Chicken Noodle: Rice Noodles", 'Latitude': '37.792948952834664', 'Location': '(37.792948952834664, -122.39809861316652)', 'LocationDescription': 'CALIFORNIA ST: DAVIS ST to FRONT ST (100 - 199)', 'Longitude': '-122.39809861316652', 'NOISent': '', 'Neighborhoods (old)': '6', 'Police Districts': '1', 'PriorPermit': '0', 'Received': '20211022', 'Schedule': 'http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=21MFF-00089&ExportPDF=1&Filename=21MFF-00089_schedule.pdf', 'Status': 'APPROVED', 'Supervisor Districts': '10', 'X': '6013245.668', 'Y': '2116754.292', 'Zip Codes': '28860', 'block': '0263', 'blocklot': '0263011', 'cnn': '3525000', 'dayshours': '', 'locationid': '1565571', 'lot': '011', 'permit': '21MFF-00089'}, {'Address': '101 CALIFORNIA ST', 'Applicant': 'Senor Sisig', 'Approved': '11/04/2021 12:00:00 AM', 'ExpirationDate': '11/15/2022 12:00:00 AM', 'FacilityType': 'Truck', 'Fire Prevention Districts': '4', 'FoodItems': 'Senor Sisig: Filipino fusion food: tacos: burritos: nachos: rice plates. Various beverages.', 'Latitude': '37.792948952834664', 'Location': '(37.792948952834664, -122.39809861316652)', 'LocationDescription': 'CALIFORNIA ST: DAVIS ST to FRONT ST (100 - 199)', 'Longitude': '-122.39809861316652', 'NOISent': '', 'Neighborhoods (old)': '6', 'Police Districts': '1', 'PriorPermit': '0', 'Received': '20211104', 'Schedule': 'http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=21MFF-00095&ExportPDF=1&Filename=21MFF-00095_schedule.pdf', 'Status': 'APPROVED', 'Supervisor Districts': '10', 'X': '6013245.668', 'Y': '2116754.292', 'Zip Codes': '28860', 'block': '0263', 'blocklot': '0263011', 'cnn': '3525000', 'dayshours': '', 'locationid': '1568883', 'lot': '011', 'permit': '21MFF-00095'}]
ans_by_block_nexist = {}

ans = [ans_by_id_exist, ans_by_id_nexist, ans_by_block_exist, ans_by_block_nexist]


# post request: one valid and one invalid
new_data = [
    {
        'locationid': "00000",
        'block': '23456789'
    },
    {
        'aa': 0
    }
]

# results from the post requests
output_post = []
for truck in new_data:
    r = requests.post(url = API_ENDPOINT, json = truck)
    output_post.append(r.text)
    
# ans for the output to assert
ans_post = [
    '{\n  "block": "23456789", \n  "locationid": "00000"\n}\n',
    "INVALID INPUT"]

class TestStringMethods(unittest.TestCase):
    
    def test_get(self):
        for i in range(len(output)):
            self.assertEqual(output[i], ans[i])
        # for i in range(5, 7):
        #     self.assertTrue(len(output[i]) == 0)

    def test_post(self):
        for i in range(len(output_post)):
            self.assertEqual(output_post[i], ans_post[i])


if __name__ == '__main__':
    unittest.main()