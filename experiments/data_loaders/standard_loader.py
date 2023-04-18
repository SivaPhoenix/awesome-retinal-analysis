"""
Copyright (c) 2023. All rights reserved.
Created by Sushmith and Siva (SREC Students)
"""
import glob,cv2,numpy as np
import matplotlib.pyplot as plt
from perception.bases.data_loader_base import DataLoaderBase
from configs.utils.utils import write_hdf5,load_hdf5

class DataLoader(DataLoaderBase):
	def __init__(self, config=None):
		super(DataLoader, self).__init__(config)
		
		self.train_img_path=config.train_img_path
		self.train_groundtruth_path = config.train_groundtruth_path
		self.train_type=config.train_datatype
		self.val_img_path=config.val_img_path
		self.val_groundtruth_path=config.val_groundtruth_path
		self.val_type = config.val_datatype

		# experiment name(exp_name)
		self.exp_name=config.exp_name
		self.hdf5_path=config.hdf5_path
		self.height=config.height
		self.width=config.width
		self.num_seg_class=config.seg_num


	def _access_dataset(self,origin_path,groundtruth_path,datatype):
		
		orgList = glob.glob(origin_path+"*."+datatype) #original image filename list
		gtList = glob.glob(groundtruth_path+"*."+datatype) # groundtruth image filename list

		
		
		for num in range(len(orgList)):
			loc=orgList[num].rfind('\\')  # if this palce goes wrong,please switch to next line to have a try
			
			gtList[num]=groundtruth_path+orgList[num][loc+1:loc+4]+'manual1.tif'

		assert (len(orgList) == len(gtList)) #  To make sure they have same length

		imgs = np.empty((len(orgList), self.height, self.width, 1))
		groundTruth = np.empty((len(gtList), self.num_seg_class, self.height, self.width))

		for index in range(len(orgList)):
			orgPath=orgList[index]
			orgImg=plt.imread(orgPath)
			imgs[index,:,:,0]=np.asarray(orgImg[:,:,1]*0.75+orgImg[:,:,0]*0.25)  #RBG color

			for no_seg in range(self.num_seg_class):
				gtPath=gtList[index]
				gtImg=plt.imread(gtPath,0)
				groundTruth[index,no_seg]=np.asarray(gtImg)
		print("[INFO] Reading...")
		assert (np.max(groundTruth) == 255)
		assert (np.min(groundTruth) == 0)
		return imgs,groundTruth



	def prepare_dataset(self):

		# preapare train_img/groundtruth.hdf5
		imgs_train, groundTruth=self._access_dataset(self.train_img_path,self.train_groundtruth_path,self.train_type)
		write_hdf5(imgs_train,self.hdf5_path+"/train_img.hdf5")
		write_hdf5(groundTruth, self.hdf5_path+"/train_groundtruth.hdf5")
		print("[INFO] Saving Training Data")
		# preapare val_img/groundtruth.hdf5
		imgs_val, groundTruth = self._access_dataset(self.val_img_path, self.val_groundtruth_path, self.val_type)
		write_hdf5(imgs_val, self.hdf5_path + "/val_img.hdf5")
		write_hdf5(groundTruth, self.hdf5_path + "/val_groundtruth.hdf5")
		print("[INFO] Saving Validation Data")

	def get_train_data(self):
		imgs_train=load_hdf5(self.hdf5_path+"/train_img.hdf5")
		groundTruth=load_hdf5(self.hdf5_path+"/train_groundtruth.hdf5")
		return imgs_train,groundTruth

	def get_val_data(self):
		imgs_val=load_hdf5(self.hdf5_path+"/val_img.hdf5")
		groundTruth=load_hdf5(self.hdf5_path+"/val_groundtruth.hdf5")
		return imgs_val,groundTruth