from scipy import io

class MPII():
    def __init__(self):
        mat_file = io.loadmat('./mpii/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat')

        self.annolist = mat_file['RELEASE']['annolist'][0, 0][0]
        self.img_train = mat_file['RELEASE']['img_train'][0, 0][0]
        self.single_person = mat_file['RELEASE']['single_person'][0, 0]
        self.act = mat_file['RELEASE']['act'][0, 0]
        # self.video_list = mat_file['RELEASE']['video_list'][0, 0][0]

        self.num = len(self.annolist)
    
    def _head(self, head):
        return head['x1'][0,0], head['y1'][0,0], head['x2'][0,0], head['y2'][0,0]
    
    def _objpos(self, objpos):
        return objpos['x'][0,0][0,0], objpos['y'][0,0][0,0]
    
    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            anno = self.annolist[idx]
            image_name = self.get_image_name(anno)
            heads = self.get_heads(anno)
            scales = self.get_scales(anno)
            objposes = self.get_objposes(anno)
            annopoints = self.get_annopoints(anno)
            if(annopoints is not None and annopoints[0] is not None and len(annopoints[0]) != 16):
                print(idx)
                print(idx)
                print(idx)
                print(idx)
                print(idx)
            yield image_name, heads, scales, objposes, annopoints
        return None
    
    def _annopoint(self, annopoint):
        if(annopoint.dtype.names is not None and 'point' in annopoint.dtype.names):
            annopoint = annopoint['point'][0,0]
            if(annopoint.dtype.names is not None and 'is_visible' in annopoint.dtype.names):
                return list(zip(
                    [x[0,0] for x in annopoint['id'][0]], 
                    zip([x[0,0] for x in annopoint['x'][0]], [x[0,0] for x in annopoint['y'][0]]), 
                    [bool(vis.flatten()[0]) if vis.size > 0 else None for vis in annopoint['is_visible'][0]]))
            else:
                return list(zip(
                    [x[0,0] for x in annopoint['id'][0]], 
                    zip([x[0,0] for x in annopoint['x'][0]], [x[0,0] for x in annopoint['y'][0]]), 
                    [None] * 16))
        return None
    
    def get_image_name(self, anno):
        return anno['image']['name'][0, 0][0]

    def get_annorect(self, anno):
        annorect = anno['annorect']
        return annorect

    def get_heads(self, anno):
        if anno['annorect'].dtype.names is not None and 'x1' in anno['annorect'].dtype.names:
            head_rect = [self._head(head) for head in anno['annorect'][['x1','y1','x2','y2']][0]]
            return head_rect
        return None
    
    def get_scales(self, anno):
        if anno['annorect'].dtype.names is not None and 'scale' in anno['annorect'].dtype.names:
            scales = [scale[0,0] if scale.size > 0 else None for scale in anno['annorect']['scale'][0]]
            return scales
        return None
    
    def get_objposes(self, anno):
        if anno['annorect'].dtype.names is not None and 'objpos' in anno['annorect'].dtype.names:
            obj_poses = [self._objpos(objpos) if objpos.size > 0 else None for objpos in anno['annorect']['objpos'][0]]
            return obj_poses
        return None
    
    def get_annopoints(self, anno):
        if anno['annorect'].dtype.names is not None and 'annopoints' in anno['annorect'].dtype.names:
            annopoints = [self._annopoint(annopoint) for annopoint in anno['annorect']['annopoints'][0]]
            return annopoints
        return None