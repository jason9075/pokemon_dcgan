from __future__ import print_function, division
from builtins import range

import os
import pandas as pd
import shutil
import glob
from scipy.misc import imread, imsave, imresize

def sort_pokemon(target):
  if not os.path.exists('../large_files'):
    print("You must create a folder called large_files adjacent to the class folder first.")
  
  DESTINATION = '../large_files/Pokemon/train/'
  
  #clear train folder
  for file in os.listdir(DESTINATION):
    if file.endswith('.jpg'):
      os.remove(DESTINATION + file) 
  if os.path.exists('../large_files/Pokemon/train-cropped'):
    shutil.rmtree('../large_files/Pokemon/train-cropped')
  
  print("Reading Pokemon status data...")
  df = pd.read_csv('../large_files/Pokemon/info/status.csv')
  if not target == 'All':
    mask = (df['Type_1'] == target) | (df['Type_2'] == target) | (df['Color'] == target)
    df = df[mask]
  data = df.as_matrix()
  target_index = data[:,0].astype('str')
  target_files = list(map(lambda x: '../large_files/Pokemon/' + x.zfill(4) + '.jpg', target_index))
  print("Moving Pokemon to train...")
  for file in target_files:
    shutil.copy(file,DESTINATION)

def get_pokemon():
  if not os.path.exists('../large_files'):
    print("You must create a folder called large_files adjacent to the class folder first.")
  
  print("Reading in and transforming data...")

  if not os.path.exists('../large_files/Pokemon/train-cropped'):
    filenames = glob.glob("../large_files/Pokemon/train/*.jpg")
    N = len(filenames)
    print("Found %d files!" % N)
  
    # crop the images to 64x64
    os.mkdir('../large_files/Pokemon/train-cropped')
    print("Cropping images, please wait...")
  
    for i in range(N):
      resize(filenames[i], '../large_files/Pokemon/train-cropped')
      if i % 1000 == 0:
        print("%d/%d" % (i, N))

  filenames = glob.glob("../large_files/Pokemon/train-cropped/*.jpg")
  return filenames

def resize(inputfile, outputdir):
  im = imread(inputfile)
  small = imresize(im, (64, 64))

  filename = inputfile.split('/')[-1]
  imsave("%s/%s" % (outputdir, filename), small)

def files2raw_images(filenames):
  return [imread(fn) for fn in filenames]
