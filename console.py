#!/usr/bin/python3
"""Module for console"""

import cmd
from shlex import split
import re
import models
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def ArgumentParser(arg):
    curly_braces_match = re.search(r"\{(.*?)\}", arg)
    brackets_match = re.search(r"\[(.*?)\]", arg)

    if curly_braces_match is None:
        if brackets_match is None:
            return [i.strip(",") for i in split(arg)]
        else:
            string_parser = split(arg[:brackets_match.span()[0]])
            parsed_tokens = [i.strip(",") for i in string_parser]
            parsed_tokens.append(brackets_match.group())
            return parsed_tokens
    else:
        string_parser = split(arg[:curly_braces_match.span()[0]])
        parsed_tokens = [i.strip(",") for i in string_parser]
        parsed_tokens.append(curly_braces_match.group())
        return parsed_tokens


class HBNBCommand(cmd.Cmd):
    """Class for console"""
    prompt = '(hbnb) '
    __classes = {"BaseModel", "User", "State",
                 "City", "Amenity", "Place", "Review"}

    def default(self, arg):
        """Default behaviour of the console."""
        argument_dict = {
                "all": self.do_all,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "count": self.do_count,
                "update": self.do_update
                }

        match = re.search(r"\.", arg)

        if match is not None:
            arguments_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arguments_list[1])

            if match is not None:
                command = [arguments_list[1][:match.span()[0]],
                           match.group()[1:-1]]

                if command[0] in argument_dict.keys():
                    call = "{} {}".format(arguments_list[0], command[1])
                    return argument_dict[command[0]](call)
            print("*** Unknown syntax: {}".format(arg))
            return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        arguments_list = ArgumentParser(arg)

        if len(arguments_list) == 0:
            print("** class name missing **")
        elif arguments_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arguments_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id"""
        arguments_list = ArgumentParser(arg)
        object_dict = storage.all()

        if len(arguments_list) == 0:
            print("** class name missing **")
        elif arguments_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arguments_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arguments_list[0],
                            arguments_list[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(
                  arguments_list[0], arguments_list[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        arguments_list = ArgumentParser(arg)
        object_dict = storage.all()

        if len(arguments_list) == 0:
            print("** class name missing **")
        elif arguments_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arguments_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arguments_list[0],
                            arguments_list[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(arguments_list[0],
                                           arguments_list[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        arguments_list = ArgumentParser(arg)

        if len(arguments_list) > 0 and arguments_list[0] is not None:
            if arguments_list[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
            else:
                object_list = []

                for obj in storage.all().values():
                    if arguments_list[0] == obj.__class__.__name__:
                        object_list.append(obj.__str__())
                    elif len(arguments_list) == 0:
                        object_list.append(obj.__str__())
                print(object_list)
        else:
            object_list = []

            for obj in storage.all().values():
                object_list.append(obj.__str__())
            print(object_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and
        id by adding or updating attribute"""

        arguments_list = ArgumentParser(arg)
        object_dict = storage.all()

        if len(arguments_list) == 0:
            print("** class name missing **")
            return False
        if arguments_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arguments_list) == 1:
            print("** instance id missing **")
            return False
        if f"{arguments_list[0]}.{arguments_list[1]}" not in \
                object_dict.keys():
            print("** no instance found **")
            return False
        if len(arguments_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arguments_list) == 3:
            try:
                type(eval(arguments_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arguments_list) == 4:
            obj = object_dict[f"{arguments_list[0]}.{arguments_list[1]}"]

            if arguments_list[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[arguments_list[2]])
                obj.__dict__[arguments_list[2]] = value_type(arguments_list[3])
            else:
                obj.__dict__[arguments_list[2]] = arguments_list[3]
        elif type(eval(arguments_list[2])) == dict:
            obj = object_dict[f"{arguments_list[0]}.{arguments_list[1]}"]

            for k, v in eval(arguments_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        arguments_list = ArgumentParser(arg)
        count = 0

        for obj in storage.all().values():
            if arguments_list[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
