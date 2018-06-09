#!/usr/bin/env python

from PIL import Image
import glob
import bisect
from datetime import datetime, timedelta

# parameters & settings ------------------------------
Area = [ 'Taiwan', 'Taipei', 'Taichung', 'Tainan', 'Taoyuan' ]
# indicate how many hours ago for producing the gif
HOURS = 12
# Rounded
BASE = 10
# use 20 min per image to form the .gif file
IMG_RANGE = 60
# the time for each frame
DURATION = 750
# indicate the times for looping the animation
LOOP = 10000

# DIR = "/Users/iisnrl/Documents/code/"
DIR = "/home/ubuntu/LASS/operations/idw_gif/img/"
# DIR_GIF = DIR + "/gif/"
DIR_GIF = '/var/www/html/LASS/assets/IDW_gif/'
# ------------------------------ parameters & settings

current = datetime.now()
# change timezone to Asia/Taipei
current = current + timedelta( hours = 8 )
current = current.replace( minute = 0, second = 0, microsecond = 0 )
time_lowerbound = current - timedelta( hours = HOURS )
# add 5 min to make sure the range could include the final file in ??:00 hours
current = current + timedelta( minutes = 5 )

image=[]
for loc in Area:
	image=[]
	file_prefix = DIR + loc + '/' + loc + ' '
	file_list = sorted( glob.glob( DIR + loc + "/*.png" ) )
	date_list = [datetime.strptime( i, file_prefix + "%Y-%m-%d %H:%M.png" ) for i in file_list]

	lower = bisect.bisect_right( date_list, time_lowerbound )
	upper = bisect.bisect_left( date_list, current )
	# print( "lower: " + str( lower ) )
	# print( "upper: " + str( upper ) )

	i = 0
	# handling file amount less than 24 hr
	if lower == 0:
		lower = 1
	file_list = file_list[ (lower - 1):upper ]
	date_list = date_list[ (lower - 1):upper ]
	for filename in file_list:
		check = int( date_list[ i ].minute )
		check = BASE * round( float( check ) / BASE )
		if( check == 0 ):
			# print( "[INSERT] " + str( filename ) )
			im = Image.open( filename )
			image.append( im )
		i = i + 1

	im = Image.open( file_list[ 0 ] )
	im.save( DIR_GIF + loc + '_latest_thumbnail.gif', save_all=True, append_images=image, duration=DURATION, loop=LOOP )
