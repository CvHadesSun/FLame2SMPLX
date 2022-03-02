'''
Date: 2022-02-25 16:48:16
LastEditors: cvhadessun
LastEditTime: 2022-02-25 17:00:03
FilePath: /FLame2SMPLX/src/utils/file_op.py
'''

''' some file read and save operation function defination
'''

import numpy as np 


def read_vertex_from_obj(fname):
    res = []
    with open(fname) as f:
        for line in f:
            if line.startswith('v '):
                tmp = line.split(' ')
                v = [float(i) for i in tmp[1:4]]
                res.append(v)
                
    return np.array(res, dtype=np.float) # [N,4]

def read_uv_coordinates_from_obj(fname):
    res = []
    with open(fname) as f:
        for line in f:
            if line.startswith('vt '):
                tmp = line.split(' ')
                v = [float(i) for i in tmp[1:3]]
                res.append(v)
    return np.array(res, dtype=np.float)



def read_vertex_faces_id_from_obj(fname): # read vertices id in faces: (vv1,vv2,vv3)
    res = []
    with open(fname) as f:
        for line in f:
            if line.startswith('f '):
                tmp = line.split(' ')
                if '/' in tmp[1]:
                    v = [int(i.split('/')[0]) for i in tmp[1:4]]
                else:
                    v = [int(i) for i in tmp[1:4]]
                res.append(v)
    return np.array(res, dtype=np.int) - 1 # obj index from 1



def read_uv_faces_id_from_obj(fname): # read texture id in faces: (vt1,vt2,vt3)
    res = []
    with open(fname) as f:
        for line in f:
            if line.startswith('f '):
                tmp = line.split(' ')
                if '/' in tmp[1]:
                    v = [int(i.split('/')[1]) for i in tmp[1:4]]
                else:
                    raise(Exception("not a textured obj file"))
                res.append(v)
    return np.array(res, dtype=np.int) - 1 # obj index from 1




def fv2norm(fv, vv):
    ''' calculate face norm
    # similar to the following method using trimesh 
    # mesh = trimesh.Trimesh(vv, fv, process=False)
    # return mesh.face_normals
    '''    
    p1 = vv[fv[:,0]]
    p2 = vv[fv[:,1]]
    p3 = vv[fv[:,2]]
    p12 = p2 - p1
    p13 = p3 - p1
    n = np.cross(p12, p13)
    n = n / (np.sqrt((n*n).sum(1))).reshape(-1,1)
    fnorm = n
    return fnorm


