import xml.etree.ElementTree as ET
import sys

# Extracts the filename on execution with argument lists.
if len(sys.argv) >= 2:
    filename = sys.argv[1]
# If the File wasn't pass on the arguments then we must write it back with input.
else:
    filename = input("Please input the xml filename with the file extention. (example.xml) : ")

      
try:
    tree = ET.parse(filename)
except:
    # If the file isn't on the path given then it will give an error.
    raise FileNotFoundError("The file was not found please try again!")


# If we have the file then we continue the execution.
def parseXML(tree):
    root = tree.getroot()
    # Then we will get the namespaces to differientate the xmls.
    # seatmap1 has ns on all the tags, seatmap2 doesn't
    my_namespaces = dict([
        node for (_, node) in ET.iterparse(filename, events=['start-ns'])
    ])
    
    # If it is seatmap1.xml then we must extract all it's attributes with ns
    if 'ns' in my_namespaces:
        # TODO extract seatmap1.xml attributes and parse it into JSON file.
        print("Is filename 1")
    
    # If it is seatmap2.xml we can extract without using ns
    else:
        # TODO extract seatmap2.xml attributes and parse it into JSON file.
        print("Is filename 2")
        

        
        
parseXML(tree)