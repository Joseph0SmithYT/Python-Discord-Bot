import json
import os
class JSONDatabase:
    def __init__(self, file_path):
        self.file_path = file_path 

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                file.close()
        except FileNotFoundError:
            data = {}
        return data

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

    def get_quotes(self, person):
        data = self.load_data()
        try:
            return data.get(str(person), []).get("quotes", [])
        except AttributeError:
            return None

    def add_quote(self, person, quote, date, time):
        data = self.load_data()
        person = str(person)
        if str(person) not in data:
            data[person] = {"quotes": []}
        data[person]["quotes"].append({"quote": quote, "date": date, "time": time})
        self.save_data(data)

    def remove_quote(self, person, quote):
        data = self.load_data()
        person = str(person)
        if str(person) in data:
            quotes = data[person].get("quotes", [])
            data[person]["quotes"] = [q for q in quotes if q["quote"] != quote]
            self.save_data(data)

    def clear(self):
        with open(self.file_path, 'w') as file:
            file.write('{}')
            file.close()