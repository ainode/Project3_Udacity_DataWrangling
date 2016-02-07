def shape_element(element):
    node = {}
    if element.tag == "relation" :
        node['type'] = element.tag
        for tag in element.iter():
            print tag.tag
            for key, val in tag.attrib.iteritems():
                print "key: ", key , " val: ", val
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)

def test():
    data = process_map('toronto_sample.osm', False)

if __name__ == "__main__":
    test()   