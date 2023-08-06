import os
import text_unidecode

from configparser import ConfigParser
from robot.api import logger


DIR_RESOURCES = 'resources'
FILE_PROJECT_PROPERTIES = 'project.properties'


def extract_type_from(locator):
    return locator.split(":")[0]


def extract_name_from(locator):
    return locator.split(":", 1)[1]


def sanitize_camel_case(name: str):
    if name is not None:
        name = ''.join(c for c in name.title() if not c.isspace())
        name = name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\'"})
        name = text_unidecode.unidecode(name)
    return name


def execute(cmd: str):
    res = os.system(cmd)
    cmdlog = f'EXECUTED: "{cmd}" WITH RESULT {res}'
    logger.info(cmdlog)
    print(cmdlog)


def get_project_properties():
    project = ConfigParser()
    project.read(os.path.join(os.getcwd(), DIR_RESOURCES, FILE_PROJECT_PROPERTIES))
    return project

