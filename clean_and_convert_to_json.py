"""
json file creation and cleaning
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
ok_post = re.compile(r'\w\d\w \d\w\d')

mapping = { "St": "Street",
            "St.": "Street",
            "Rd." : "Road",
            "Ave" : "Avenue",
            "Ave." : "Avenue",
             "Dr" : "Drive",
            "Cresent" : "Crescent"
            }

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def update_name(name, mapping):
    name = name.rsplit(' ', 1)[0] + " " + mapping[name.rsplit(' ', 1)[1]]
    return name

#cleaning the data and putting it in json
def change_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            return update_name(street_name, mapping)
        else:
            return street_name
        
#example: change "city of Burlington" to "Burlington"        
def edit_city_name(city_name):
    if (city_name.startswith("City of") or city_name.startswith("city of")\
        or city_name.startswith("Town of") or city_name.startswith("town of")):
        return city_name.split()[2]
    else:
        return city_name
    
def edit_postal_code(postalcode):
    if ok_post.search(postalcode):
        return postalcode
    else:
        return postalcode[0:3] + " " + postalcode[3:6]
    
#example 1 (416)222-4444 to 4162224444
def edit_phone_number(phone):
    #eliminate all non-number charactors
    num = re.sub(r'\D', "", phone)
    num_len = len(num)
    if num_len == 10:
        return num
    elif (num_len) > 10:
        if(int(num[0]) == 1):
            return num[1:11]
        else:
            return num[0:10]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node['type'] = element.tag
        node['created'] = {}
        node['pos'] = []
        for attribute, val in element.attrib.iteritems():
            if(attribute in CREATED):
                node['created'][attribute] = val
            elif(attribute in ['lat', 'lon']):
                node['pos'].append(float(val))    
            else:
                node[attribute] = val
        for tag in element.iter("tag"):
            attrib_val = tag.attrib['k']
            if( not (problemchars.search(attrib_val)) and attrib_val.count(":") < 2):
                if(attrib_val.startswith("addr:")):
                    if('address' not in node):
                        node['address'] = {}
                    if attrib_val == "addr:street":
                        node['address'][attrib_val[5:]] = change_street_type(tag.attrib['v'])
                    if attrib_val == "addr:city":
                        node['address'][attrib_val[5:]] = edit_city_name(tag.attrib['v'])  
                    if attrib_val == "addr:postcode":
                        node['address'][attrib_val[5:]] = edit_postal_code(tag.attrib['v'])  
                elif(attrib_val.find(":") != -1):
                    node[attrib_val] = tag.attrib['v']
                else:
                    if('other_tags' not in node):
                        node['other_tags'] = {}
                    if attrib_val == "phone":
                        node['other_tags'][attrib_val] = edit_phone_number(tag.attrib['v'])
                    else:
                        node['other_tags'][attrib_val] = tag.attrib['v']    
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('toronto_sample.osm', False)

if __name__ == "__main__":
    test()   