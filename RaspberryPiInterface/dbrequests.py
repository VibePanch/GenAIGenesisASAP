import requests
import json
#from dotenv import load_dotenv
import os

#load_dotenv("dh2024.env")
api_key = "uN5a52qg3b50g9uIJBUZO2YFrZP9dZuo3W8mGi2Gk9DivUa1kjXAFlXF0BzbTLid"

def GET(database,collection):
    url = "https://us-east-1.aws.data.mongodb-api.com/app/data-sikvi/endpoint/data/v1/action/find"

    payload = json.dumps({
        "collection": f"{collection}",
        "database": f"{database}",
        "dataSource": "DeerHacks2024",
        "projection": None
    })
    headers = {
      'Content-Type': 'application/json',
      'Access-Control-Request-Headers': '*',
      'api-key': f'{api_key}',
    }

    return requests.request("POST", url, headers=headers, data=payload).json()

def POST(database, collection, data):
    url = "https://us-east-1.aws.data.mongodb-api.com/app/data-sikvi/endpoint/data/v1/action/insertOne"

    payload = {
        "collection": collection,
        "database": database,
        "dataSource": "DeerHacks2024",
        "document": data  # Add the data you want to write to the database
    }

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': api_key  # Assuming api_key is defined somewhere in your code
    }

    # Send a POST request to insert data into the database
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        return "Data inserted successfully!"
    else:
        return f"Error: {response.status_code}"


def PATCH(database, collection, filter_data, update_data):
    url = "https://us-east-1.aws.data.mongodb-api.com/app/data-sikvi/endpoint/data/v1/action/updateOne"

    payload = {
        "collection": collection,
        "database": database,
        "dataSource": "DeerHacks2024",
        "filter": filter_data,  # Specify the filter for the document to update
        "update": update_data   # Specify the update operation to perform
    }

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': api_key  # Assuming api_key is defined somewhere in your code
    }

    # Send a POST request to update data in the database
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 201:
        return "Data updated successfully!"
    else:
        return f"Error: {response.status_code}"


def LOGIN(email, password, role):
    allAccounts = GET("Accounts",role)
    for i in allAccounts.get("documents"):
        if i.get("Email")==email and i.get("Password:")==password:
            return True
    return False


def getUserByKey(key,value,role):
    allAccounts = GET("Accounts",role)
    for i in allAccounts.get("documents"):
        if i.get(key) ==value:
            return i
    return False


def getAllStudents(role):
    allAccounts = GET("Accounts",role)
    students=[]
    for i in allAccounts.get("documents"):
        students.append(i.get("Name") + " (" + i.get("Email") + ")")
    return students