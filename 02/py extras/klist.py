# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:25:20 2018

@author: Enrique
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

OSMFILE = "bogota_sample.osm"

#%%
'''
This modified version of the audit function prints the values of the k attributes of the tags
This lets me see if the tags used here are similar to the example and if there are any new ones
'''
def list_k(osmfile):
    osm_file = open(osmfile, "r")
    k_tags = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                    k_tags['k'].add(tag.attrib['k'])
    osm_file.close()
    return k_tags

#%%
'''
This simply runs the audit and prints the results
'''
types = list_k(OSMFILE)
pprint.pprint(dict(types))

#%%
