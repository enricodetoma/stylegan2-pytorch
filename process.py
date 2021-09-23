import glob
import os

file_path = "modern_paintings"
file_path_resized = "modern_paintings_resized"
os.makedirs(file_path, exist_ok=True)
os.makedirs(file_path_resized, exist_ok=True)
image_files = [os.path.join(root, name)
             for root, dirs, files in os.walk(file_path)
             for name in files
             if name.endswith((".jpg", ".jpeg"))]
num_files = len(image_files)
print(num_files)

from PIL import Image
import matplotlib.pyplot as plt

def save_image(file, img, side):
  path = os.path.dirname(file).replace(file_path, file_path_resized)
  fname = os.path.basename(file).replace(".jpg", side + ".jpg")
  os.makedirs(path, exist_ok=True)
  path = os.path.join(path, fname)
  print(path)
  img.save(path)

for i, file in enumerate(sorted(image_files)):
  try:
    img = Image.open(file)
    img = img.convert('RGB')
  except:
    continue
  width, height = img.size

  if (width > height): # wide
    # print("wide")
    img1 = img.crop((0, 0, height, height))
    img1 = img1.resize((1024, 1024))
    save_image(file, img1, "_lft")

    offset = (width-height) // 2
    img2 = img.crop((offset, 0, height+offset, height))
    img2 = img2.resize((1024, 1024))
    save_image(file, img2, "_ctr")

    img3 = img.crop((width-height, 0, width, height))
    img3 = img3.resize((1024, 1024))
    save_image(file, img3, "_rgt")

  elif (height > width): # tall
    # print("tall")
    img1 = img.crop((0, 0, width, width))
    img1 = img1.resize((1024, 1024))
    save_image(file, img1, "_top")

    offset = (height-width) // 2
    img2 = img.crop((0, offset, width, width+offset))
    img2 = img2.resize((1024, 1024))
    save_image(file, img2, "_ctr")

    img3 = img.crop((0, height-width, width, height))
    img3 = img3.resize((1024, 1024))
    save_image(file, img3, "_bot")

  else: # square
    # print("square")
    img1 = img
    save_image(file, img1, "")

  # imgplot = plt.imshow(img1)
  # plt.axis("off")
  # plt.show()
  # imgplot = plt.imshow(img2)
  # plt.axis("off")
  # plt.show()
  # imgplot = plt.imshow(img3)
  # plt.axis("off")
  # plt.show()

  # if i > 5:
  #   break
 