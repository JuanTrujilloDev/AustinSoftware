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
        
        
            
            
    
    # If it is seatmap2.xml we can extract it
    else:
        # TODO extract seatmap2.xml attributes and parse it into JSON file.
        root = tree.getroot()
        ns = "{http://www.iata.org/IATA/EDIST/2017.2}"
        
        # Flight dict will ve transformed into json.
        flight = {}
        flight_data =  {}
        data_lists = root.find(ns + "DataLists")
        flight_segment_list = data_lists.find(ns + "FlightSegmentList")
        flight_segment = flight_segment_list.find(ns + "FlightSegment")
        
        # Extracting flight data
        for child in flight_segment:
            flight_data[child.tag[len(ns):]] = {}
            for element in child:
                flight_data[child.tag[len(ns):]][element.tag[len(ns):]] = element.text
        
        flight["flight_data"] = flight_data
        
        
        # Seat definition data.
        seat_definition = {}
        
        seat_definition_list = data_lists.find(ns + "SeatDefinitionList").findall(ns + "SeatDefinition")
        
        # Extracting each definition and storing it into the flight data
        for seat_info in seat_definition_list:
            for text in seat_info.find(ns + "Description"):
                seat_definition[seat_info.attrib["SeatDefinitionID"]] = text.text 
            
        flight["seat_definition"] = seat_definition
        
        
        # Price data:
        
        alacarteoffer = root.find(ns + "ALaCarteOffer")
        alacarteitems = alacarteoffer.findall(ns + "ALaCarteOfferItem")
        
        price_list = {}
        for item in alacarteitems:
            for price_detail in item.findall(ns + "UnitPriceDetail"):
                # Extracting each price and its code.
                price_code = price_detail.find(ns + "TotalAmount").find(ns + "SimpleCurrencyPrice")
                price_list[item.attrib["OfferItemID"]] = price_code.text + " GBP"
        
        # Adding price list to flight data        
        flight["price_list"] = price_list
        
        
        # Seat map:
        
        flight["cabins"] = []
        
        seat_map_list = root.findall(ns + "SeatMap")
        cabin_list = [seat_map.find(ns + "Cabin") for seat_map in seat_map_list]
        
        for cabin in cabin_list:
            # Extrating Cabin Values
            cabin_layout = cabin.find(ns + "CabinLayout")
            cabin_values = {}
            cabin_values["start_row"] = cabin_layout.find(ns + "Rows").find(ns + "First").text
            cabin_values["end_row"] = cabin_layout.find(ns + "Rows").find(ns + "Last").text
            
            
            cabin_values["rows"] = []
            
            # PD: I know it might not be the most optimal solution but it was the best workaround.
            # Time complexity is O(n*m*k)
            
            # Then extrating row number and seats
            for row in cabin.findall(ns + "Row"):
                row_values = {}
                row_values["number"] = row.find(ns + "Number").text
                row_values["seat"] = []
                
                # For each seat we will get its values
                for seat in row.findall(ns + "Seat"):
                    seat_values = {}
                    seat_values["seat_number"] = row_values["number"] + seat.find(ns + "Column").text
                    price_ref = seat.findall(ns + "OfferItemRefs")
                    
                    # Getting the price reference
                    if price_ref:
                        seat_values["price"] = flight["price_list"][price_ref[0].text]
                    # If there is not price reference the price will be None
                    else:
                        seat_values["price"] = None
                        
                    seat_values["seat_definition"] = {}
                    
                    # Finally we get each flight definition
                    for seat_definition in seat.findall(ns + "SeatDefinitionRef"):
                        seat_values["seat_definition"][seat_definition.text] = flight["seat_definition"][seat_definition.text]
                        
                    # Then we append each seat to the row
                    row_values["seat"].append(seat_values)
                    
                    
                # Finally we append each row to the cabin
                cabin_values["rows"].append(row_values)
                    
            # And finally we add each cabin to the flight     
            flight["cabins"].append(cabin_values)
            
        with open(filename.split(".")[0] + "_parsed.json", "w+", encoding="utf-8") as f:
            f.write(json.dumps(flight, indent=4))
                
            
                
                
            
            
        
        
        
        
        
        
        
        
        

        
        
parseXML(tree)