#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)
    
    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside."""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

        def do_create(self, arg):
            """
            Creates a new instance of a class, saves it to the JSON file, and prints the id
            Usage: create <class name> <param 1> <param 2> <param 3>...
            """
            args = arg.split()
            if len(args) == 0:
                print("** class name missing **")
                return
            class_name = args[0]
            if class_name not in models.classes:
                print("** class doesn't exist **")
                return
            kwargs = {}
            for arg in args[1:]:
                if "=" not in arg:
                    continue
                key, val = arg.split("=", 1)
                if not val:
                    continue
                if val[0] == '"' and val[-1] == '"' and len(val) > 1:
                    val = val[1:-1].replace("_", " ").replace('\\"', '"')
                    kwargs[key] = val
                elif '.' in val:
                    try:
                        kwargs[key] = float(val)
                    except ValueError:
                        continue
                else:
                    try:
                        kwargs[key] = int(val)
                    except ValueError:
                        continue
            new_obj = models.classes[class_name](**kwargs)
            new_obj.save()
            print(new_obj.id)
