'''
Date: 2022-03-02 11:14:11
LastEditors: cvhadessun
LastEditTime: 2022-03-02 11:21:19
FilePath: /FLame2SMPLX/src/test.py
'''
from utils.texture_match import flame_smplx_texture_combine


fname="../data/smplx-addon.obj"
flame_smplx = '../data/SMPL-X__FLAME_vertex_ids.npy'
flame_name = '../data/head_template.obj'
flame_texture = '../data/mean_texture.jpg'
smplx_texture = '../data/output.png'


flame_smplx_texture_combine(flame_name,fname,flame_texture,smplx_texture,flame_smplx)