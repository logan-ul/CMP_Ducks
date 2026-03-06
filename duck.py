import requests
import json
import os

class DuckManager:
    def __init__(self):
        # This initializes the data object containing all the duck information
        # if internet is not available or for some reason the api is down it defaults to a local copy
        try:
            data = requests.get("https://duckland-production.up.railway.app/ducks").json()
            with open("cache.json", "w") as file:
                json.dump(data, file, indent=4)
        except:
            if not os.path.isfile("cache.json"):
                # here we're checking to see if the file exists and creating an empty one if it doesnt
                with open("cache.json", "w") as file:
                    pass
            with open("cache.json", "r") as file:
                data = json.load(file)
        self.data = data
        self.duck_list = []

    def create_duck_list(self):
        """Creates and returns a list of duck objects in the duck manager."""
        for duck in self.data:
            self.duck_list.append(Duck(duck))
        return self.duck_list

    def get_duck_by_id(self, id:list[str]|str = []):
        """Accepts either a string or list of strings containing id's and returns the duck with the matching id"""
        if id:
            return next(filter(lambda duck: duck.id in id, self.duck_list))

    def get_ducks_by_name(self, name: str):
        """Accepts a string and returns the duck with the matching name"""
        return list(filter(lambda duck: duck.name.lower() == name.lower(), self.duck_list))
    
    def get_ducks_by_assembler(self, assembler: str):
        """Accepts a string and returns the duck with the matching assembler, note this currently deos not work"""
        return list(filter(lambda duck: assembler.lower() in duck.assembler.lower(), self.duck_list))

    

        



class Duck:
    def __init__(self, data:dict):
        # Main fields
        self.raw_data = data
        self.id = data["_id"]
        self.name = data["name"]
        self.assembler = data["assembler"]
        self.adjectives = data["adjectives"]
        self.derpy = data["derpy"]
        self.bio = data["bio"]
        self.date = data["date"]
        self.approved = data["approved"]
        self.version = data["__v"]

        # Body fields
        self.head_color = data["body"]["head"]
        self.front1_color = data["body"]["front1"]
        self.front2_color = data["body"]["front2"]
        self.back1_color = data["body"]["back1"]
        self.back2_color = data["body"]["back2"]

        # Stats fields
        self.strength = data["stats"]["strength"]
        self.health = data["stats"]["health"]
        self.focus = data["stats"]["focus"]
        self.intelligence = data["stats"]["intelligence"]
        self.kindness = data["stats"]["kindness"]

    def __str__(self):
        return f"{self.name.title()}, owned by {self.assembler.title()}"





if __name__ == "__main__":
    manager = DuckManager()
    for duck in manager.create_duck_list():
        print(duck)
    print(manager.get_duck_by_id("69a881b504f2a69eea6979cf"))
    print(manager.get_ducks_by_name("TEST")[0])
    print(manager.get_ducks_by_name("Logan"))
