from PIL import Image
import sys
import os
from pathlib import Path

images_file = sys.argv[1]
labels_file = sys.argv[2]
to_dir = sys.argv[3]

images_info = os.stat(images_file)
labels_info = os.stat(labels_file)
print("images file size {:d} bytes".format(images_info.st_size))
print("labels file size {:d} bytes".format(labels_info.st_size))

images_f = open(images_file, "rb")
labels_f = open(labels_file, "rb")
images_d = bytes(images_f.read())
labels_d = bytes(labels_f.read())

if (0 != images_d[0]) or (0 != images_d[1]) or (8 != images_d[2]) or (3 != images_d[3]):
	print("images file magic number error " + "".join("{:02x}".format(x) for x in images_d[0:4]))
	sys.exit(1)
images_n = ((images_d[4] * 256 + images_d[5]) * 256 + images_d[6]) * 256 + images_d[7]


if (0 != labels_d[0]) or (0 != labels_d[1]) or (8 != labels_d[2]) or (1 != labels_d[3]):
	print("labels file magic number error " + "".join("{:02x}".format(x) for x in labels_d[0:4]))
	sys.exit(1)
labels_n = ((labels_d[4] * 256 + labels_d[5]) * 256 + labels_d[6]) * 256 + labels_d[7]

if images_n != labels_n:
	print("images number not equal label number")
	sys.exit(2)
print("images number {:d}".format(images_n))

#os.chdir(os.path.dirname(__file__) + to_dir)
os.chdir(to_dir)
for i in range(images_n):
	image = Image.frombytes("L", (28, 28), images_d[16 + i * 28 * 28:16 + (i + 1) * 28 * 28])
	image.save("{:d}".format(i) + ".png")
