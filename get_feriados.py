import requests
from bs4 import BeautifulSoup
import re
import json


def create_json_object(array_of_objects):
    json_object = {}

    for obj in array_of_objects:
        # Assuming each object has a unique identifier key
        identifier = obj['date']
        json_object[identifier] = obj

    return json_object

# Function to save dictionary to a JSON file


def save_to_json(dictionary, filename):
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(dictionary, json_file, indent=4)


def get_variable_value(url, variable_name):
    # Fetch the HTML content of the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(
            response.content, 'html.parser')

        # Find all script tags
        scripts = soup.find_all('script')

        # Iterate through each script tag
        for script in scripts:
            # Extract the text content of the script tag
            # script_text = script.get_text().encode().decode("unicode-escape")
            script_text = script.get_text()
            # print(script_text)

            # Use regular expressions to find the variable and its value
            match = re.search(
                r'const\s+' + re.escape(variable_name) + r'\s*=\s*([^;]+);', script_text)

            # If the variable is found, return its value
            if match:
                return match.group(1).strip()

    # If the request was not successful or the variable was not found, return None
    return None


def get_holidays_of_year(year):
    # Example usage
    url = f'https://www.argentina.gob.ar/interior/feriados-nacionales-{year}'
    variable_name = f'holidays{year}'
    value = get_variable_value(url, variable_name)

    jsonData = eval(value)

    if value is not None:
        # json_dictionary = create_json_object(jsonData)
        # print(json_dictionary)
        # # save_to_json(json_dictionary, "2024.json")
        # with open("2024.json", "w", encoding="utf-8") as file:
        #     json.dump(json_dictionary, file, indent=4, ensure_ascii=False)
        return jsonData
    else:
        print(f"Variable {variable_name} not found on the webpage.")
