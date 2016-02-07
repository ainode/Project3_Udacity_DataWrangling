#This code is written to compare contents of all same tags to see if there is any inconsistancies
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}   
    count = 0
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag not in tags:
            tags[elem.tag] = {}
            for tag in elem.iter():
                if tag.tag not in tags[elem.tag]:
                    tags[elem.tag][tag.tag]  = {}
                for attribute, val in tag.attrib.iteritems():
                    if attribute not in tags[elem.tag][tag.tag]:
                        tags[elem.tag][tag.tag][attribute] = []
                        tags[elem.tag][tag.tag][attribute].append(val)
                    else:
                        tags[elem.tag][tag.tag][attribute].append(val)
    return tags
def test():
    tags = count_tags('toronto_sample.osm')
    pprint.pprint(tags)

if __name__ == "__main__":
    test()