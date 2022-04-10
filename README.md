# Austin Software - Test Solution

### Intro:


Seatmap Availability Exercise:

Our goal is to parse seatmap information from XML files and create a JSON format that our customers can parse so that they can display any airline seatmap by integrating our format.

Desired behavior:

Input: python seatmap_parser.py [FILENAME]

Output: FILENAME_parsed.json

Description:
Write a python script that parses the XML seatmap files included in this folder (seatmap1.xml, seatmap2.xml) into a standardized JSON format that outputs the seatmap (by row) with the following properties at minimum:
	- Seat/Element type (Seat, Kitchen, Bathroom, etc)
	- Seat id (17A, 18A)
	- Seat price
	- Cabin class
	- Availability

Feel free to include any other properties in your JSON format that you think are relevant.

Please avoid the use of xml to json libraries/tools such as xmltodict, objectify and the like.


## Solution:

First at all I want to thank **Austin Software, Camila Carrique and Pia Borras** for the opportunity.

This exercise one of my first times working with XML, I had only worked with csv, excel and JSON files. However I think I found a good workoround for the solution.

Here is a step by step of how I decided to solve the problem.


1. First I took a read on both XMLs in that way I could understand how the data was stored and organized.
2. Then I gave the posibility to pass the filename as execution arguments or reading them by user input.
3. I parsed the seatmap1 first which was the longest one but the most easier out of the 2, I had to learn about namespaces on XML files and used xml.etree Python native module to solve it. Due to the lack of knowledge on XML etree module the algorithm has O(n) and O(n*m) time complexity.
4. Next I parsed seatmap2 the first step was extracting all the seat information and price codes, then I extracted the cabin data, rows and lastly the seat info. It was harder because I had to traverse through child nodes and it was harder for me.
5. Finally depending on the file I save it on a json file using open Python module.

Note: I'm thinking also on parsing the json file into csv or creating a Django Project where I can store all the json data into a database or visualize it on a graphic interface. However due to the lack of time I'm note sure if I will be able to do this extra task.


## Execution Tutorial - Step by step

TODO: Here I will write down a step by step tutorial on how to use the program.
