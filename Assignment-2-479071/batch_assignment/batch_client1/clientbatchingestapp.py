from pymongo import MongoClient
from pymongo import errors as mongoerrors
import csv

def ingest_file(filename):
    parsed_json = []
    with open(filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            obj = {
                "dateRep" : row["dateRep"],
                "year" : row["year"],
                "month" : row["month"],
                "day" : row["day"],
                "cases" : row["cases"],
                "deaths" : row["deaths"],
                "countriesAndTerritories" : row["countriesAndTerritories"],
                "geoId" : row["geoId"],
                "countryterritoryCode" : row["countryterritoryCode"],
                "popData2019" : row["popData2019"],
                "continentExp" : row["continentExp"],
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000" : row["Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"]
            }
            parsed_json.append(obj)
    try:
        client = MongoClient("router", 27017)
        db = client["covid"]
        collection = db["EUData"]
        collection.insert_many(parsed_json)
    
    except mongoerrors.PyMongoError as error:
        return error
