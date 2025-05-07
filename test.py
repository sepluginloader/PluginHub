import os
import sys
import xml.etree.ElementTree as ET
import re

def main():
	plugins = []
	mods = []

	if len(sys.argv) < 2:
		print(f"Usage: {os.path.basename(__file__)} input_directory")
		return
	
	pluginDir = sys.argv[1]

	for root, dirs, files in os.walk(pluginDir):
		for filename in files:
			fullpath = os.path.join(root, filename)
			if(os.path.isfile(fullpath) and filename.lower().endswith(".xml")):
				try:
					validate(fullpath)
				except BaseException as error:
					print("Error occurred while reading file ", fullpath, ": ", error)
					sys.exit(1)

	print(f"All files validated")

def validate(xmlFile: str):
	cleanPath = xmlFile.replace(os.getcwd(), "").replace("\\", "/").lstrip("/")
	if (not cleanPath.startswith("Plugins/")):
		raise Exception(f"{xmlFile} is not in the Plugins folder")
	
	tree = ET.parse(xmlFile)
	if(tree == None):
		raise Exception(f"{xmlFile} is not valid xml")
	
	root = tree.getroot()
	pluginType = root.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type")
	if(pluginType == "ModPlugin"):
		if(not cleanPath.startswith("Plugins/Mods/")):
			raise Exception(f"{xmlFile} must be in the Plugins/Mods/ folder")
	elif (pluginType != "GitHubPlugin"):
		raise Exception(f"{xmlFile} has invalid type: {pluginType}")
	
	element = root.find("Id")
	if(element == None or element.text == None):
		raise Exception(f"{xmlFile} is missing an Id")

	element = root.find("FriendlyName")
	if(element == None or element.text == None):
		raise Exception(f"{xmlFile} is missing a FriendlyName")

	element = root.find("Author")
	if(element == None or element.text == None):
		raise Exception(f"{xmlFile} is missing an Author")

	if(pluginType == "GitHubPlugin"):
		element = root.find("Commit")
		if(element == None or element.text == None):
			raise Exception(f"{xmlFile} is missing a Commit")
		if(not re.search(r"^[0-9a-f]+$", element.text)):
			raise Exception(f"'{element.text}' in {xmlFile} is not a valid commit id")

if __name__ == "__main__":
    main()
