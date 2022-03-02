'''
Date: 2022-02-25 16:48:06
LastEditors: cvhadessun
LastEditTime: 2022-03-02 10:30:14
FilePath: /FLame2SMPLX/src/main.py
'''
import os
import sys

from utils.file_op import *
import cv2
import numpy as np 
from utils.texture_match import affine_transform



fname="../data/smplx-addon.obj"
flame_smplx = '../data/SMPL-X__FLAME_vertex_ids.npy'


size=1024

vertex = read_vertex_from_obj(fname)


uv_coordinates = read_uv_coordinates_from_obj(fname)

faces_id = read_vertex_faces_id_from_obj(fname)

faces_uv = read_uv_faces_id_from_obj(fname)

texture = np.zeros((size,size, 3), np.uint8)

uv_coordinates[:,1] = 1 - uv_coordinates[:,1] # y--v

uv = (uv_coordinates*size).astype(np.int)

# ##
flame_smplx_idx = np.load(flame_smplx)

smplx_faces={}
for j in range(faces_id.shape[0]):
    v1,v2,v3 = faces_id[j]
    name = str(v1)+'_'+str(v2)+'_'+str(v3)
    smplx_faces[name] = j
    


# hash_map={}
# for id in flame_smplx_idx:
#     hash_map[id] = id



# filter face uv

# flame_idx = []

# for id, uv_ids in enumerate(faces_id):
#     # print(uv_ids)
    
#     if((uv_ids[0] in hash_map) and (uv_ids[1] in hash_map) and (uv_ids[2] in hash_map)):
#         # print(hash_map[uv_ids[0]],hash_map[uv_ids[1]],hash_map[uv_ids[2]])
#         flame_idx.append(id)
#     print("-"*50)

# # # print(len(flame_idx))
# for id in flame_idx:
#     cv2.drawContours(texture, [uv[faces_uv[id]]], 0, (100,100,100), -1)
# cv2.imwrite('../data/output_flame_smplx.png',texture)


# size_flame=512

# flame 

flame_name = '../data/head_template.obj'

flame_verts = read_vertex_from_obj(flame_name)

# print(flame_smplx_idx.shape)   # [5023]
# print(flame_verts.shape)  # [5023,3]

hash_flame_smplx = {}
for ii in range(flame_verts.shape[0]):
    hash_flame_smplx[ii] = flame_smplx_idx[ii]



flame_uv_coordinates = read_uv_coordinates_from_obj(flame_name)

flame_faces_id = read_vertex_faces_id_from_obj(flame_name)

flame_faces_uv = read_uv_faces_id_from_obj(flame_name)

flame_texture = np.zeros((size,size, 3), np.uint8)

flame_uv_coordinates[:,1] = 1 - flame_uv_coordinates[:,1] # y--v

flame_uv = (flame_uv_coordinates*size).astype(np.int)


smplx_uv_ids=[]
flame_uv_ids=[]

for id,flame_face in enumerate(flame_faces_id):
    v1=hash_flame_smplx[flame_face[0]] 
    v2=hash_flame_smplx[flame_face[1]] 
    v3=hash_flame_smplx[flame_face[2]] 
    name = str(v1)+'_'+str(v2)+'_'+str(v3)
    if name in smplx_faces:
        smplx_uv_ids.append(smplx_faces[name])
        flame_uv_ids.append(id)


for fid in flame_uv_ids:
    print(flame_uv[flame_faces_uv[fid]].shape)
 	# cv2.drawContours(flame_texture, [flame_uv[flame_faces_uv[fid]]], 0, (100,100,100), -1)

# cv2.imwrite('../data/output_flame.png',flame_texture)