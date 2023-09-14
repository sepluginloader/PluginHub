import os
import json
import sys
import xml.etree.ElementTree as ET
import subprocess;

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
				try:
					getData(fullpath, mods, plugins)
				except BaseException as error:
					print("Error occurred while reading file ", fullpath, ": ", error)
					sys.exit(1)

	plugins.sort(key=lambda x: x["name"])
	mods.sort(key=lambda x: x["name"])

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

	lastModified = getLastModified(xmlFile, root.find("Commit"))
	if(lastModified > 0):
		plugin["modified"] = lastModified

	if(root.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ModPlugin"):
		modList.append(plugin)
	else:
		pluginList.append(plugin)

def getLastModified(file: str, commitElement):
	fullPath = os.path.abspath(file)
	gitPath = os.path.dirname(fullPath)
	try:
		args = None
		if(commitElement != None and commitElement.text != None):
			args = ['git', 'log', '--date=unix', '--pretty=format:%ct', '--reverse', '-S', commitElement.text, '--', fullPath]
		else:
			args = ['git', 'log', '-1', '--date=unix', '--pretty=format:%ct', '--follow', '--diff-filter=A', '--', fullPath]
		process = subprocess.run(args, cwd=gitPath, capture_output=True, text=True)

		processError = str(process.stderr).strip()
		if(len(processError) > 0):
			print("ERROR: ", processError)
		result = str(process.stdout).partition('\n')[0].strip()
		return int(result)
	except BaseException as error:
		print("Error getting last modified date: ", error)
		return 0

if __name__ == "__main__":
    main()
