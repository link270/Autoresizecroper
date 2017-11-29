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

def generate_file_names(fnpat, rootdir):
  for  dirpath, dirnames, filenames in os.walk(rootdir):
    for filename in fnmatch.filter(filenames, fnpat):
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
			new_im.paste(imlist[currentImg], (x,y))
			currentImg = currentImg + 1
	return new_im


if __name__ == '__main__':
	imlist = []
 	for fn in generate_file_names("*.jpg" or "*.png", sys.argv[1]):
 		size = 800
 		img = Image.open(fn)
 		img = resize(crop(img), size)
 		imlist.append(img)
 	rows = int(math.sqrt(len(imlist)))
 	cols = int(math.sqrt(len(imlist)))
 	fname = 'Patchwork.jpeg'
 	i = 0
 	while os.path.isfile(fname):
 		i = i+1
 		fname = 'Patchwork_' + str(i) + '.jpeg'
 	stitch(imlist, rows, cols).save(sys.argv[2] + fname, 'JPEG', quality = 95, dpi = (300,300))
 		

#if __name__ == '__main__':
#	i=0
# 	for fn in generate_file_names("*.jpg" or "*.png", sys.argv[1]):
# 		size = 500
# 		img = Image.open(fn)
# 		img = resize(crop(img), size)
# 		img.save(sys.argv[2] + str(i) + '.' + 'jpeg', 'JPEG', quality = 95, dpi = (300,300))
# 		i = i+1
 		#img2.save(sys.argv[2] + str(i) + '.' + sys.argv[3])