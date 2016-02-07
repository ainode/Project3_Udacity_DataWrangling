#get number of unique users using Python code
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if(element.tag == 'node' or element.tag == 'way' or element.tag == 'relation'):
            users.add(element.attrib['uid'])
        pass
    return users


def test():

    users = process_map('toronto_sample.osm')
    pprint.pprint(users)
    print "Number of unique users:: ", len(users)

if __name__ == "__main__":
    test()