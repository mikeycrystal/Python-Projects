import math
from PIL import Image

def make_collage(collage_dim, images):
	""" 
	Given a series of images, paste them into a collage that covers 
	a whole canvas (collage_im)

	How do we calculate placement? Assume square-ish images

	"""




	collage_im = Image.new(mode="RGB", size=collage_dim)
	if len(images) == 0:
		print("----- No images in collage -----")
		return collage_im

	count = math.ceil(math.sqrt(len(images)))
	w = collage_im.size[0]//count
	h = collage_im.size[1]//count


	def get_aspect_ratio(im):
		return im.size[0] / im.size[1]


	collage_aspect = w/h
	
	for (index, im) in enumerate(images):
		x = (index%count)*w
		y = (index//count)*h

		# Handle images or Cat Pics
		if type(im) != Image:
			im = im.im

		# We have to fill an w by h region
		# How much of this image should we crop?
		aspect = get_aspect_ratio(im)

		if aspect < collage_aspect:
			# Taller? Crop the height
			box = (0,0,im.size[0],math.floor(im.size[1]*aspect//collage_aspect))
		else:
			# Wider? Crop the width
			box = (0,0,math.floor(im.size[0]*collage_aspect//aspect),im.size[1])


		region = im.crop(box)
		region = region.resize((w,h))
		collage_im.paste(region, (x, y, x+w, y+h))

		
	return collage_im
		
