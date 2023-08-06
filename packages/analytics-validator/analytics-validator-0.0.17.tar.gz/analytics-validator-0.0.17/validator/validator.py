#!/usr/bin/python
import os
import sys
import glob
import pykwalify
import yaml
from pykwalify.core import Core
from pykwalify.errors import SchemaError, CoreError
import pkg_resources


def check(proj_dir):
    # Loads configurations.yaml from the project directory
    with open(proj_dir + "/configurations.yml") as file:
        project_configs = yaml.load(file, Loader=yaml.FullLoader)

    proj_schema_version = project_configs['schema']
    proj_name = project_configs['name']

    # Verify if schema directory exists
    schema_directory = pkg_resources.resource_filename(
        __name__, "schemas/" + proj_schema_version)

    if(not os.path.isdir(schema_directory)):
        raise Exception("Invalid schema version: %s" % proj_schema_version)

    # prints project information
    print("Detected project %s using schema version: %s" %
          (proj_name, proj_schema_version))

    # Load schema version
    exec("sys.path.append('%s')" % schema_directory)
    from schema_validator import validate

    # Calls the validate inside the schema version
    validate(proj_schema_version, os.path.abspath(proj_dir))
