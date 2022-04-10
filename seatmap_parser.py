import xml.etree.ElementTree as ET
import sys
import json

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
        ns = './/{' + my_namespaces['ns'] + '}'
        # Flight basic info: (Flight Number, Departure Time, etc)
        flight_info = root.find(ns + 'FlightSegmentInfo')
        flight = {}
        for attrib in flight_info.attrib:
            flight[attrib] = flight_info.attrib[attrib]
        
        # Flight child info:
        
        # Auxiliar ns endpoint string len to extract child tags without
        # Incurring into quadratic time complexity
        ns_len = len('{' + my_namespaces['ns'] + '}')

        # We just get the 1st element on child attribs.
        
        for child in flight_info:
            flight[child.tag[ns_len:]] = child.attrib[next(iter(child.attrib))]
            
        
        # Warnings:
        
        warnings = root.find(ns + 'Warnings')
        # Auxiliary warning list to make it faster.
        warning_list = []
        for child in warnings:
            warning = {}
            warning['Code'] = child.attrib['Code']
            warning['Message'] = child.text
            warning_list.append(warning)
            
        flight[warnings.tag.split('}')[1]] = warning_list
        

            
        # Row Info:
        flight["Rows"] = []
        rows = root.findall(ns + 'RowInfo')
        
        # Extracting row by row.
        for row in rows: 
            row_attribs = row.attrib
            row_attribs["Seats"] = []
            # Seat by seat for each row extracted
            for seat in row:
                seat_attribs = seat.attrib
                # If seat is finded we will extract its attributes.
                if seat:
                    for summary in [seat.find(ns + "Summary")]:
                        seat_attribs["Summary"] = summary.attrib
                    for features in [seat.find(ns + "Features")]:
                        seat_attribs["Features"] = features.text 
                    # At the end we save all the seat attributes into the dict.
                    row_attribs["Seats"].append(seat_attribs)
                
            # At the end we append all the rows
            flight["Rows"].append(row_attribs) 
        
        # Finally we save the file with the json format
        with open(f"{filename.split('.')[0]}_parsed.json",  "w+", encoding="utf-8") as f: 
            f.write(json.dumps(flight, indent=4))
        
        
            
            
    
    # If it is seatmap2.xml we can extract without using ns
    else:
        # TODO extract seatmap2.xml attributes and parse it into JSON file.
        print("Is filename 2")
        

        
        
parseXML(tree)