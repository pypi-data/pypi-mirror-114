#!/usr/bin/python

import os
import glob
import pykwalify
import yaml
import re
from dateformat import DateFormat
from pykwalify.core import Core
from pykwalify.errors import SchemaError, CoreError

CONFIG_SCHEMA = "configurations_schema.yml"
ATTR_SCHEMA = "attributes_schema.yml"
ENUM_SCHEMA = "enum_schema.yml"
EVENT_SCHEMA = "event_schema.yml"


def validateEnums(schema_dir, proj_dir):
    enums_path = os.path.join(proj_dir, "enums/*.yml")
    enums_schema_path = os.path.join(schema_dir, ENUM_SCHEMA)

    files = glob.glob(enums_path)
    count = 0
    for enum in files:
        c = Core(source_file=enum, schema_files=[enums_schema_path])
        c.validate(raise_exception=True)
        count += 1
    print("Found %s Enums!" % count)


def validateEvents(schema_dir, proj_dir, proj_enums):
    event_schema_path = os.path.join(schema_dir, EVENT_SCHEMA)

    default_event_attributes = loadConfigurations(proj_dir).get("default_event_attributes", None)

    event_domains = glob.glob("%s/events/*/" % proj_dir)
    count = 0
    for event_domain in event_domains:
        files = glob.glob("%s/*.yml" % event_domain)
        for event in files:
            c = Core(source_file=event, schema_files=[event_schema_path])
            c.validate(raise_exception=True)

            with open(event) as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

                for scope in data["scopes"]:
                    for attribute in scope["attributes"]:
                        validateType(attribute["type"], attribute.get(
                            "value", None), proj_enums)
                        if(default_event_attributes and hasDuplicatedAttributes(default_event_attributes["scopes"], scope["name"], attribute["name"])):
                            raise Exception("Duplicate attribute %s inside scope %s. Already declared in the default_event_attributes" %
                                            (attribute["name"], scope["name"]))

            count += 1
    print("Found %s Events!" % count)

def hasDuplicatedAttributes(scopes, scope, attribute):
    if(any(s["name"] == scope for s in scopes)):
        attributes = next(s for s in scopes if s["name"] == scope)["attributes"]
        if(any(a["name"] == attribute for a in attributes)):
            return True
    return False

def validateType(attr_type, attr_value, proj_enums):
    match = re.search(
        r'(string|integer|boolean|datetime|date|time|float|map|enum\/([a-zA-Z]+)$)', attr_type)
    if(match.group(1) == "string" and attr_value != None and type(attr_value) is not str):
        raise Exception("Invalid type %s for value %s!" %
                        (attr_type, attr_type))
    elif(match.group(1) == "integer" and attr_value != None and not attr_value.isdigit()):
        raise Exception("Invalid type %s for value %s!" %
                        (attr_type, attr_value))
    elif(match.group(1) == "boolean" and attr_value != None and type(attr_value) is not bool):
        raise Exception("Invalid type %s for value %s!" %
                        (attr_type, attr_value))
    elif(match.group(1) in ["date", "map"] and attr_value != None):
        raise Exception("Type %s cannot have default value!" % (attr_type))
    elif(match.group(1) == "float" and attr_value != None and type(attr_value) is not float):
        raise Exception("Invalid type %s for value %s!" %
                        (attr_type, attr_value))
    elif(match.group(1) in ("date", "time", "datetime") and attr_value != None and attr_value != "now"):
        raise Exception("Invalid value %s for type %s!" %
                        (attr_value, attr_type))
    elif(match.group(1).startswith("enum")):
        if(match.group(2) not in proj_enums):
            raise Exception("Custom enum %s not declared!" % match.group(2))
        elif(attr_value != None and attr_value not in [data["name"] for data in proj_enums[match.group(2)]]):
            raise Exception("Invalid value %s for enum %s!" %
                            (attr_value, match.group(2)))


def validateAttributes(schema_dir, proj_dir, proj_enums):
    attrs_schema_path = os.path.join(schema_dir, ATTR_SCHEMA)

    count = 0

    files = glob.glob("%s/attributes/*.yml" % proj_dir)
    for attribute_file in files:
        c = Core(source_file=attribute_file, schema_files=[attrs_schema_path])
        c.validate(raise_exception=True)

        with open(attribute_file) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

            for attribute in data["attributes"]:
                validateType(attribute["type"], attribute.get(
                    "value", None), proj_enums)

        count += 1
    print("Found %s Attribute files!" % count)


def validateConfigurations(schema_directory, projectDirectory, proj_enums):
    configurations_path = os.path.join(projectDirectory, "configurations.yml")
    configurations_schema_path = os.path.join(schema_directory, CONFIG_SCHEMA)

    c = Core(source_file=configurations_path,
             schema_files=[configurations_schema_path])
    c.validate(raise_exception=True)

    configurations = loadConfigurations(projectDirectory)
    if(configurations.get("default_event_attributes", None)):
        data = configurations["default_event_attributes"]
        for scope in data["scopes"]:
            for attribute in scope["attributes"]:
                validateType(attribute["type"], attribute.get("value", None), proj_enums)


def loadConfigurations(projectDirectory):
    configurations_path = os.path.join(projectDirectory, "configurations.yml")
    with open(configurations_path) as file:
        configurations = yaml.load(file, Loader=yaml.FullLoader)
        return configurations


def loadEnums(projectDirectory):
    files = glob.glob("%s/enums/*.yml" % projectDirectory)

    enums = {}

    for enum_file in files:
        # Loads configurations.yaml from the project directory
        with open(enum_file) as file:
            enum_data = yaml.load(file, Loader=yaml.FullLoader)

            name = enum_data["name"]
            values = enum_data["values"]

            if name not in enums:
                enums[name] = enum_data["values"]
            else:
                raise Exception(
                    "Enum %s declared mutiple times in different files!" % name)

    return enums


def validate(schema_version, proj_dir):
    schema_dir = os.path.dirname(__file__)

    validateEnums(schema_dir, proj_dir)

    proj_enums = loadEnums(proj_dir)

    validateConfigurations(schema_dir, proj_dir, proj_enums)

    validateEvents(schema_dir, proj_dir, proj_enums)

    validateAttributes(schema_dir, proj_dir, proj_enums)
