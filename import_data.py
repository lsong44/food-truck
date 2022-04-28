import csv

'''
This is a function to convert data from a csv file to a dictionary
args: sourse file path (string), primary key (string)
return: a dictionary containing all data from the file; key: passed in args; value: row data
'''
def prepare_data(file_path, prime_key):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(file_path, encoding='utf-8') as source:
        csvReader = csv.DictReader(source)
         
        # Convert each row into a dictionary value to the defined key and add to data
        for row in csvReader:
            key = row[prime_key]
            data[key] = row
 
    return data
         
# test code
if __name__ == "__main__":
    file_path = "Mobile_Food_Facility_Permit.csv"
    prime_key = "locationid"
    data = prepare_data(file_path, prime_key)
    counter = 0
    for key in data:
        print(data[key])
        counter += 1
        if counter >= 10:
            break