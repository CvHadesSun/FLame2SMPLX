'''
Date: 2022-02-28 16:03:27
LastEditors: cvhadessun
LastEditTime: 2022-03-10 14:46:04
FilePath: /FLame2SMPLX/src/utils/texture_match.py
'''

import cv2
from .file_op import *
import numpy as np
import tqdm






def affine_transform(p1,p2,tex1,tex2):

    tex1 = tex1.copy()
    tex2 = tex2.copy()
    # crop tex1 by p1 --> tex2 by p2
    p1 = p1.reshape(-1,2).astype(np.float32) #[3,2]
    p2 = p2.reshape(-1,2).astype(np.float32) #[3,2]
    mat_trans = cv2.getAffineTransform(p1, p2) 
    p1 = p1.astype(np.int)
    p2 = p2.astype(np.int)
    
    dst_h,dst_w,_ = tex2.shape

    # 
    tex1_mask = np.zeros(tex1.shape,dtype=np.int8)
    tex2_mask = np.ones(tex2.shape,dtype=np.int8)

    tex1_mask = cv2.drawContours(tex1_mask,[p1],0, (1,1,1), -1)  # 1
    tex2_mask = cv2.drawContours(tex2_mask,[p2],0, (0,0,0), -1)  # 0

    # crop contours from tex with p1
    invalid_index = np.where(tex1_mask==0)
    tex1[invalid_index] = 0

    # 
    invalid_index2 = np.where(tex2_mask==0)
    tex2[invalid_index2] = 0

    dst = cv2.warpAffine(tex1, mat_trans, (dst_w,dst_h)) 

    # combine tex2 and dst image
    out_img = dst+tex2

    return out_img


def get_smplx_flame_crossrespondence_face_ids(smplx_template_obj,
                                            flame_template_obj,
                                            smplx_flame_vertex_ids,
                                            smplx_face_indexes=None):
    '''
    input:
        smplx_template_obj: smplx template obj /to/path/file.obj
        flame_template_obj: flame template obj /to/path/file.obj
        smplx_flame_vertex_ids: the smplx vertices id crossresponding to flame
        size: the tmp texture size.
    output:
        flame_2_smplx_uv_ids: {flame_uv_id:smplx_uv_id,....}
        s_f_uvs: smplx uv faces
        s_uv: smplx uv coordinates
        f_f_uvs: flame uv faces
        f_uv: flame uv coordinates.
    '''

    size=1024
    # get smplx info from smplx template obj file.
    # s_verts = read_vertex_from_obj(smplx_template_obj)
    s_f_ids = read_vertex_faces_id_from_obj(smplx_template_obj)
    s_f_uvs = read_uv_faces_id_from_obj(smplx_template_obj)
    s_uv = read_uv_coordinates_from_obj(smplx_template_obj)
    # s_tex = np.zeros((size,size, 3), np.uint8)

    s_uv[:,1] = 1 - s_uv[:,1] # y--v
    # s_uv = (s_uv*size).astype(np.int)

    # get flame info from flame template obj file.
    f_verts = read_vertex_from_obj(flame_template_obj)
    f_f_ids = read_vertex_faces_id_from_obj(flame_template_obj)
    f_f_uvs = read_uv_faces_id_from_obj(flame_template_obj)
    f_uv = read_uv_coordinates_from_obj(flame_template_obj)
    # f_tex = np.zeros((size,size, 3), np.uint8)

    f_uv[:,1] = 1 - f_uv[:,1] # y--v
    # f_uv = (f_uv*size).astype(np.int)

    # smplx to flame vertex ids
    sf_ids = np.load(smplx_flame_vertex_ids)

    
    if smplx_face_indexes is not None:
        # filtered other index but face vertices index
        face_vertex_ids = np.load(smplx_face_indexes)
        for j in range(f_verts.shape[0]):
            if sf_ids[j] in face_vertex_ids[0]:
                continue
            else:
                sf_ids[j] = -1
        
    f_2_s_verts_ids = {}
    for ii in range(f_verts.shape[0]):
        f_2_s_verts_ids[ii] = sf_ids[ii]

    # smplx vertex id to face id
    smplx_faces={}
    for j in range(s_f_ids.shape[0]):
        v1,v2,v3 = s_f_ids[j]
        name = str(v1)+'_'+str(v2)+'_'+str(v3)
        smplx_faces[name] = j

    # get the uv map crossrespondences ids
    flame_2_smplx_uv_ids={}

    for id,flame_face in enumerate(f_f_ids):
        v1=f_2_s_verts_ids[flame_face[0]] 
        v2=f_2_s_verts_ids[flame_face[1]] 
        v3=f_2_s_verts_ids[flame_face[2]] 
        name = str(v1)+'_'+str(v2)+'_'+str(v3)
        if name in smplx_faces:
            flame_2_smplx_uv_ids[id] = smplx_faces[name]

    return flame_2_smplx_uv_ids,s_f_uvs,s_uv,f_f_uvs,f_uv
    
def flame_smplx_texture_combine(flame_obj,
                                smplx_obj,
                                flame_texture,
                                smplx_texture,
                                smplx_flame_vertex_ids,
                                smplx_face_indexes=None):
    
    flame_2_smplx_uv_ids,smplx_faces,smplx_uv,flame_faces,flame_uv = get_smplx_flame_crossrespondence_face_ids(smplx_obj,flame_obj,smplx_flame_vertex_ids,smplx_face_indexes)

    # 
    flame_texture = cv2.imread(flame_texture)
    smplx_texture = cv2.imread(smplx_texture)
    flame_texture = cv2.resize(flame_texture,[2048,2048])
    smplx_texture = cv2.resize(smplx_texture,[4096,4096])
    f_h,f_w,_ = flame_texture.shape
    s_h,s_w,_ = smplx_texture.shape

    flame_uv[:,1] *=f_h
    flame_uv[:,0] *=f_w
    flame_uv = flame_uv.astype(np.int)

    smplx_uv[:,1] *=s_h
    smplx_uv[:,0] *=s_w
    smplx_uv = smplx_uv.astype(np.int)

    for id in tqdm.tqdm(flame_2_smplx_uv_ids.keys()):
        f_uv_id = id
        s_uv_id = flame_2_smplx_uv_ids[id]

        flame_idx = flame_faces[f_uv_id]
        smplx_idx = smplx_faces[s_uv_id]
        flame_p = flame_uv[flame_idx]
        smplx_p = smplx_uv[smplx_idx]
        # print(flame_p.shape)
        smplx_texture = affine_transform(flame_p,smplx_p,flame_texture,smplx_texture)
        
    smplx_texture = cv2.medianBlur(smplx_texture,17)

    # cv2.imwrite('../data/flame2smplx.png',smplx_texture)
    return smplx_texture


