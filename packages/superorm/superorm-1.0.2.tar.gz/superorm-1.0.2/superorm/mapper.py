from typing import Dict, Any
from xml.dom.minidom import parse, parseString


Mapper = Dict


def parse4string(xml_string: str) -> Mapper:
    """
    Parsing XML configuration string
    :param xml_string: XML configuration string
    :return: Profile information dictionary
    """
    return _parse4doc(parseString(xml_string))


def parse4file(file_path: str) -> Mapper:
    """
    Parsing XML configuration file
    :param file_path: Profile path
    :return: Profile information dictionary
    """
    return _parse4doc(parse(file_path))


# noinspection SpellCheckingInspection
def _parse4doc(doc: Any) -> Mapper:
    """
    Parsing DOC documents
    :param doc: Doc document
    :return: Profile information dictionary
    """
    # Pre create return dictionary
    return_dict = {}
    root = doc.documentElement
    # Analytic mapping
    return_dict["mappers"] = {}
    for mapper in root.getElementsByTagName('mapper'):
        column = mapper.getAttribute("column")
        parameter = mapper.getAttribute("parameter")
        return_dict["mappers"][column] = parameter
    # Parsing SQL statements
    return_dict["sqls"] = {}
    for sql in root.getElementsByTagName('sql'):
        key = sql.getElementsByTagName('key')[0].childNodes[0].data
        value = sql.getElementsByTagName('value')[0].childNodes[0].data
        return_dict["sqls"][key] = value
    return return_dict
