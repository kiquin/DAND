# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:21:40 2018

@author: Enrique

This file simply counts the tags in the specified file and is indented in blocks 
for use with Spyder
"""

import xml.etree.cElementTree as ET
import pprint

#%%
'''
This function iterates through the tree and builds a dictionary where keys
are the tag names and the values are its ocurrences.
'''
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        tag_name = elem.tag
        if tag_name in tags:
            tags[tag_name] += 1
        else:
            tags[tag_name] = 1
    return tags

#%%
'''
Creates a set of the users marked as such in the ET
'''
def get_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        users.add(element.get('user'))
    
    users.remove(None)
    return users

#%%
sample = 'bogota_sample.osm'

tags = count_tags(sample)
pprint.pprint(tags)

#%%
users = get_users(sample)
print(len(users))
