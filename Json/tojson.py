import os
import json
import sys
import xml.etree.ElementTree as ET

def main():
	plugins = []
	mods = []

	if len(sys.argv) < 3:
		print(f"Usage: {os.path.basename(__file__)} input_directory output_file")
		return
	
	pluginDir = sys.argv[1]
	outputFile =  sys.argv[2]

	for root, dirs, files in os.walk(pluginDir):
		for filename in files:
			fullpath = os.path.join(root, filename)
			if(os.path.isfile(fullpath) and filename.lower().endswith(".xml")):
				getData(fullpath, mods, plugins)

	with open(outputFile, "w") as outfile:
		json.dump({ "plugins": plugins, "mods": mods }, outfile, indent=2)
	print(f"Wrote {len(plugins)} plugins and {len(mods)} mods")

def getData(xmlFile: str, modList: list, pluginList: list):
	tree = ET.parse(xmlFile)
	if(tree == None):
		return
	root = tree.getroot()
	plugin = {}

	element = root.find("Id")
	if(element == None or element.text == None):
		return
	plugin["id"] = element.text

	element = root.find("FriendlyName")
	if(element == None or element.text == None):
		return
	plugin["name"] = element.text

	element = root.find("Author")
	if(element == None or element.text == None):
		return
	plugin["author"] = element.text

	element = root.find("Tooltip")
	if(element != None and element.text != None):
		plugin["tooltip"] = element.text

	element = root.find("Description")
	if(element != None and element.text != None):
		plugin["description"] = element.text

	element = root.find("Hidden")
	if(element != None and element.text != None):
		plugin["hidden"] = element.text

	if(root.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ModPlugin"):
		modList.append(plugin)
	else:
		pluginList.append(plugin)

if __name__ == "__main__":
    main()
