# -*- coding: utf-8 -*-
"""
This file containts functions that help audit the street names
and also update them to conform to the standards.
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

'''
This regular expresion was created with help from https://regexr.com/
it gets the first word of a string.
'''
OSMFILE = "bogota.osm"
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

'''
These are the street names in Bogotá. If you read spanish you can learn
about it in https://www.idu.gov.co/page/bogota-y-los-nombres-de-sus-calles
All are in titlecase and the mapping reflects that. Names in lowercase are replaced.
'''
expected = ["Calle", "Carrera", "Diagonal", "Transversal", "Autopista", "Avenida", "Via"]

mapping = { "Ak": "Avenida Carrera",
            "AK": "Avenida Carrera",
            "Ak.": "Avenida Carrera",
            "Avcl": "Avenida Calle",
            "Ave": "Avenida",
            "Av": "Avenida",
            "Av.": "Avenida",
            "calle": "Calle",
            "Cl": "Calle",
            "Cll": "Calle",
            "Clle": "Calle",
            "Cl.": "Calle",
            "Cll.": "Calle",
            "Cale": "Calle",
            "Call": "Calle",
            "carrera": "Carrera",
            "Carerra": "Carrera",
            "Carrea": "Carrera",
            "Carrera.": "Carrera",
            "KR" : "Carrera",
            "kr" : "Carrera",
            "Cr": "Carrera",
            "Cr.": "Carrera",
            "Cra": "Carrera",
            "Cra.": "Carrera",
            "Crr.": "Carrera",
            "Kr": "Carrera",
            "Diagona": "Diagonal",
            "Tv": "Transversal",
            "transvesal": "Transversal"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r", encoding='utf8')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    for key, value in mapping.items():
        if key in name:
            name = re.sub(r'\b'+key+r'\b', value, name)
            break
        
    return name

#%%
#this prints the street names that do not comform to expectations
def run_audit(OSMFILE):
    names = audit_street(OSMFILE)
    pprint.pprint(dict(names))

run_audit(OSMFILE)