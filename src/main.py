'''
Date: 2022-02-25 16:48:06
LastEditors: cvhadessun
LastEditTime: 2022-03-10 13:53:54
FilePath: /FLame2SMPLX/src/main.py
'''
import cv2
from utils.texture_match import flame_smplx_texture_combine



smplx_obj = "../data/smplx-addon.obj"
flame_obj = "../data/head_template.obj"
smplx_2_flame = "../data/SMPL-X__FLAME_vertex_ids.npy"
smplx_texture = "../data/smplx_texture_m_alb.png"
flame_texture = "../data/swh_dongmi_white.png"

# only face (not head)
face_vertex_ids = "../data/face_vertex_ids.npy"



tex_output = flame_smplx_texture_combine(flame_obj,smplx_obj,flame_texture,smplx_texture,smplx_2_flame,face_vertex_ids)

cv2.imwrite('../data/output_texture.png',tex_output)