import os
import subprocess
try:
	import libxmp
except ModuleNotFoundError as er:
    raise ModuleNotFoundError(str(er.args) + "\n Install with e.g. $ pip install python-xmp-toolkit")
import shutil

import mariqt.core as miqtc
import mariqt.directories as miqtd
import mariqt.tests as miqtt
import mariqt.variables as miqtv
import mariqt.files as miqtf


def getVideoRuntime(path):
	""" Uses FFMPEG to determine the runtime of a video in seconds. Returns 0 in case their was any issue"""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	command = "ffprobe -v fatal -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	try:
		return float(result.stdout)
	except:
		return 0


def getVideoStartTime(path):
	""" Uses FFMPEG to determine the start time of a video from the metadata of the video file. Returns an empty string in case there was any issue"""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	command = "ffprobe -v fatal -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return result.stdout.decode("utf-8").strip()


def getVideoUUID(path):
	""" Checks a video file for a UUID in its XMP namespace Darvin Core metadata field 'identifier'. Returns an empty string if there is no UUID encoded in the file"""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")

	xmpfile = libxmp.XMPFiles( file_path=path, open_forupdate=True )
	xmp = xmpfile.get_xmp()
	identifier = ""
	try:
		identifier = xmp.get_property( libxmp.consts.XMP_NS_DC, 'identifier' )
	except (libxmp.XMPError, AttributeError):
		pass
	return identifier

	""" Uses FFMPEG to query a video file for a UUID in its metadata. Returns an empty string if there is no UUID encoded in the file"""
	command = "ffprobe -v fatal -show_entries format_tags=UUID -of default=noprint_wrappers=1:nokey=1 "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	return result.stdout.decode("utf-8").strip()


def writeUUIDtoVideo(path,copy=True,test_val=""):
	""" Tries to write a UUID to an file's XMP namespace Darvin Core metadata field 'identifier'. Returns whether it succeeded """

	#TODO testing only
	if test_val != "":
		uuid = test_val
	else:
		uuid = str(miqtc.uuid4())

	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")

	if copy:
		path_original = path
		path_split = path.split('.')
		path_split[-2] = path_split[-2] + "_tmp"
		path_new = ".".join(path_split)
		shutil.copyfile(path_original, path_new)
		path = path_new

	xmpfile = libxmp.XMPFiles( file_path=path, open_forupdate=True )
	xmp = xmpfile.get_xmp()
	success = False
	try:
		# Change the XMP property
		xmp.set_property( libxmp.consts.XMP_NS_DC, 'identifier',uuid)

		# Check if XMP document can be written to file and write it.
		if xmpfile.can_put_xmp(xmp):
				xmpfile.put_xmp(xmp)
				success = True
	except (libxmp.XMPError, AttributeError):
		pass

	# XMP document is not written to the file, before the file
	# is closed.
	xmpfile.close_file()

	if copy:
		if success:
			# rename originals
			path_split = path_original.split('.')
			path_split[-2] = path_split[-2] + "_original"
			path_original_new = ".".join(path_split)
			os.rename(path_original, path_original_new)
			# rename news
			os.rename(path, path_original)
		else:
			os.remove(path)

	return success


def getImageUUID(path):
	""" Uses exiftool to query an image file for a UUID in its metadata. Returns an empty string if there is no UUID encoded in the file."""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	command = "exiftool -imageuniqueid "+path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	all = result.stdout.decode("utf-8").strip()
	if all != "":
		# Get last line of response
		txt = all.split("\n")[-1]
		# Omit Perl warnings
		if txt[0:14] == "perl: warning:":
			txt = ""
		# Omit other warings (e.g. Warning: [minor] Unrecognized MakerNotes)
		elif txt[0:8] == "Warning:":
			txt = ""
		# Omit other errors
		elif txt[0:5] == "Error":
			txt = ""
		else:
			txt = txt.split(":")[1].strip()
	else:
		txt = ""
	return txt,all

def imageContainsValidUUID(file:str):
	""" returns whether image contains valid UUID and UUID. Throws exception if file extension not in variables.photo_types or variables.video_types"""
	if os.path.splitext(file)[1][1:].lower() in miqtv.photo_types:
		uuid,msg = getImageUUID(file)
	elif os.path.splitext(file)[1][1:].lower() in miqtv.video_types:
		uuid,msg = getVideoUUID(file)
	else:
		raise Exception("Unsupported file type to determine UUID from metadata: "+os.path.splitext(file)[1][1:])
	
	if uuid == "":
		return False, uuid

	# check for validity
	if not miqtc.is_valid_uuid(uuid):
		print("Image " + file + "contains invalid UUID " + uuid)
		return False, uuid
	return True, uuid
                    

def getImageUUIDsForFolder(path):
	""" Uses exiftool to query all images in folder path for the UUID in their metadata. Returns a dict with filename -> UUID keys/values. Or an empty dict if none of the images has a UUID in the metadata. Images without a UUID do not make it into the returned dict!"""
	command = "exiftool -T -filename -imageuniqueid " + path
	result = subprocess.run(command.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	txt = result.stdout.decode("utf-8").strip()
	ret = {}
	if txt != "":
		lines = txt.split("\n")
		for line in lines:
			tmp = line.split("\t")
			if len(tmp) < 2:
				continue
			ret[tmp[0]] = tmp[1].split()
	return ret


def browseForImageFiles(path:str,extensions:list = miqtv.image_types,recursive=True,skipConfigFiles=True):
	""" Recursively scans a folder for media files (specified by the given file extension you are looking for).

	The result variable contains a dictionary with the found file paths as keys and
	a triple for each of those files with the file size, runtime and file extension:
	<name>:[<size>,<runtime>,<ext>]
	"""

	ret = {}
	files = miqtf.browseForFiles(path,extensions,recursive,skipConfigFiles)
	for file in files:
		file_ext = file.split(".")[-1].lower()
		ret[file] = [os.stat(file).st_size,-1,file_ext]
		if file_ext in miqtv.video_types:
			# This is a video file, check its runtime with ffmpeg
			ret[file][1] = getVideoRuntime(file)

	return ret


def browseFolderForImages(path:str,types:list = miqtv.image_types):
	raise Exception("DEPRECATED, use browseForImageFiles instead")
	
def createImageList(path:miqtd.Dir,overwrite=False,write_path:bool=False,img_types = miqtv.image_types):
	""" Creates a text file that contains one line per image file found in path

	Can overwrite an existing file list file if told so.
	Can add the full absolute path to the text file if told so (by providing the absolute path you want as the write_path variable)
	Can filter which images (or actually all file types) to put into the file. Default is all image types.
	"""

	if not path.exists():
		return False,"Path not found"

	# Potentially create output folder
	path.createTypeFolder(["intermediate"])

	# Check whether the full path shall be written
	if write_path == True:
		write_path = path
	else:
		write_path = ""

	# Scan the directory and write all files to the output file
	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_images.lst"
	if not os.path.exists(dst_path) or overwrite:
		try:
			lst = open(dst_path,"w")
			files = os.listdir(path.tosensor()+"raw/")
			for file in files:
				if file[0] == ".":
					continue
				fn, fe = os.path.splitext(file)
				if fe[1:].lower() in img_types:
					lst.write(write_path+file+"\n")
			lst.close()
			return True,"Created output file."
		except:
			return False,"Could not create output file."
	else:
		return True,"Output file exists."


def allImageNamesValidIn(path:miqtd.Dir,sub:str = "raw"):
	""" Validates that all image file names are valid in the given folder."""

	img_paths = browseForImageFiles(path.tosensor()+"/"+sub+"/")
	invalidImageNames = []
	for file in img_paths:
		file_name = os.path.basename(file)
		if not miqtt.isValidImageName(file_name):
			invalidImageNames.append(file)
	if len(invalidImageNames) != 0:
		return False,"Not all files have valid image names! Rename following files before continuing:\n-" + "\n- ".join(invalidImageNames)
	return True,"All filenames valid"


def computeImageScaling(area_file:str, data_path:str, dst_file:str, img_col:str = "Image number/name", area_col:str = "Image area", area_factor_to_one_square_meter:float = 1.0):
	""" Turns an ASCII file with image->area information into an ASCII file with image->scaling information

	Path to the source file is given, path to the result file can be given or is constructed from the convention
	"""

	import math
	from PIL import Image
	import mariqt.files as miqtf


	miqtc.assertExists(area_file)

	area_data = miqtf.tabFileData(area_file,[img_col,area_col],key_col = img_col,graceful=True)

	o = open(dst_file,"w")
	o.write("image-filename\timage-pixel-per-millimeter\n")

	for img in area_data:

		with Image.open(data_path + img) as im:
			w,h = im.size

			scaling = math.sqrt(w*h / (float(area_data[img][area_col]) * area_factor_to_one_square_meter * 1000000))
			o.write(img + "\t" + str(scaling) + "\n")

def createImageItemsDictFromImageItemsList(items:list):
	""" Creates from a list of item dicts a dict of dicts with the 'image-filename' value becoming the respective dicts name """
	itemsDict = {}
	for item in items:
		if 'image-filename' not in item:
			raise Exception("item",item,"does not contain a field 'image-filename'")
		itemsDict[item['image-filename']] = item
	return itemsDict

def createImageItemsListFromImageItemsDict(items:dict):
	""" Creates from a dict of item dicts a list of dicts with the 'image-filename' value becoming an item field again """
	itemsList = []
	for item in items:
		itemDict = items[item]
		itemDict['image-filename'] = item
		itemsList.append(itemDict)
	return itemsList

