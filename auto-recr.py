#!/usr/bin/python

###
# Author: Mitch Shelton (Link270)
# Useage: python auto-recr.py {PATH-TO-SOURCE} {PATH-TO-DESTINATION}
###

import re
import sys
import os
import fnmatch
import math
from PIL import Image, ImageFilter
from random import shuffle

def generate_file_names(fnpat, rootdir):
  for  dirpath, dirnames, filenames in os.walk(rootdir):
	for filename in (filenames):
	  if filename.lower().endswith(fnpat):
		yield os.path.join(dirpath, filename)

def crop(img):
	newSize = findNewSize(min(img.size))
	h_padding = (newSize - img.size[0]) / 2
	v_padding = (newSize - img.size[1]) / 2
	return img.crop((-h_padding, -v_padding, img.size[0]+h_padding, img.size[1]+v_padding))

def findNewSize(size):
	while size%100 != 0:
		size = size-1
	return size

def resize(img, size):
	return img.resize((size,size), resample=Image.LANCZOS)

def stitch(imlist, numImgWide, numImgTall):
	imgWidth = imlist[0].size[0]
	imgHeight = imlist[0].size[1]
	new_im = Image.new('RGB', (numImgWide * imgWidth,  numImgTall * imgHeight))
	currentImg = 0
	for i in xrange(numImgTall):
		y = imgHeight * i
		for j in xrange(numImgWide):
			x = imgWidth * j
			try:
				new_im.paste(imlist[currentImg], (x,y))
			except:
				print "Image at " + str(currentImg) + " does not exist."
			currentImg = currentImg + 1
	return new_im

#This section will resize and recrop all of the images then stitch them back together into one latger image containing all of the photos.
if __name__ == '__main__':
	imlist = []
	progress = 0
	total = 0
	mod = 1 #Editing this number will increse or decrese the size of your images.
	size = (225 * mod)
	for fn in generate_file_names((".png", ".jpg", ".jpeg", ".tif"), sys.argv[1]):
		total += 1
	for fn in generate_file_names((".png", ".jpg", ".jpeg", ".tif"), sys.argv[1]):
		img = Image.open(fn)
		img = resize(crop(img), size)
		imlist.append(img)
		if progress%10 == 0:
			percentage = (progress / float(total)) * 100
			print "Progress: " + str(int(percentage)) + "%"
		progress = progress+1
	print "Progress: 100% -stitching photos together now."
	rows = 28 * ((300 * mod)/float(size)) #int(math.sqrt(len(imlist)))
	cols = 28 * ((300 * mod)/float(size)) #int(math.sqrt(len(imlist)))
	fname = 'Patchwork.jpeg'
	print int(cols)
	i = 0
	shuffle(imlist)
	while os.path.isfile(fname):
		i = i+1
		fname = 'Patchwork_' + str(i) + '.jpeg'
	stitch(imlist, int(rows), int(cols)).save(sys.argv[2] + fname, 'JPEG', quality = 95, dpi = (300,300))
		
#This section will resize and crop the images and save them to the provided folder with the provided filetype
#if __name__ == '__main__':
#	i=0
# 	for fn in generate_file_names("*.jpg" or "*.png", sys.argv[1]):
# 		size = 500
# 		img = Image.open(fn)
# 		img = resize(crop(img), size)
# 		img.save(sys.argv[2] + str(i) + '.' + 'jpeg', 'JPEG', quality = 95, dpi = (300,300))
# 		i = i+1
		#img2.save(sys.argv[2] + str(i) + '.' + sys.argv[3])