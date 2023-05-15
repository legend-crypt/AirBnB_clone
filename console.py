#!/usr/bin/python3
"""Module for console"""

import cmd
import models
import json
import re
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """Class for console"""
    prompt = '(hbnb) '
    classes = ["BaseModel", "User", "State",
               "City", "Amenity", "Place", "Review"]

    def default(self, cmd_line):
        """Catch commands if nothing else matches then."""
        self._precmd(cmd_line)

    def _precmd(self, arg):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", arg)
        if not match:
            return arg
        class_name = match[1]
        method = match[2]
        args = match[3]

        if match_uid_and_args := re.search('^"([^"]*)"(?:, (.*))?$', args):
            uid = match_uid_and_args[1]
            attr_or_dict = match_uid_and_args[2]
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            if match_dict := re.search('^({.*})$', attr_or_dict):
                self._update_dict(class_name, uid, match_dict[1])
                return ""
            if match_attr_and_value := re.search(
                    '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict):
                attr_and_value = ((match_attr_and_value[1]
                                   or "") + " ") + (
                                   match_attr_and_value[2] or "")
        command = f"{method} {class_name} {uid} {attr_and_value}"
        self.onecmd(command)
        return command

    def _update_dict(self, class_name, uid, str_dict):
        """Helper method for update() with a dictionary."""
        str_dict = str_dict.replace("'", '"')
        dict_ = json.loads(str_dict)
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[class_name]
                for attribute, value in dict_.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

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
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            new = eval(arg)()
            new.save()
            print(new.id)

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id"""
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f"{args[0]}.{args[1]}"
                instances = models.storage.all()
                if key in instances:
                    print(instances[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f'{args[0]}.{args[1]}'
                if key in models.storage.all():
                    del models.storage.all()[key]
                    models.storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        instances = models.storage.all()
        if not arg:
            object_list = [str(value) for key, value in instances.items()]
            print(object_list)
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            object_list = [
                    str(value)
                    for key, value in instances.items()
                    if value.__class__.__name__ == arg
                    ]
            print(object_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and
        id by adding or updating attribute"""

        if arg == "" or arg is None:
            print("** class name missing **")
            return

        pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+"?([^"]*)"?$'
        match = re.search(rex, arg)
        class_name = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(class_name, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[class_name]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        count = sum(arg in key for key,
                    value in models.storage.all().items())
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
