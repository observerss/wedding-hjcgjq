#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image

for root, dirs, paths in os.walk(os.path.join(os.path.dirname(__file__), 'gallery')):
    for path in paths:
        if 'web' not in path and 'thumb' not in path and path.endswith('.jpg'):
            print 'processing', os.path.join(root, path)
            im = Image.open(os.path.join(root, path)) 
            size = (im.size[0]//6, im.size[1]//6)
            webim = im.resize(size, Image.ANTIALIAS)
            webim.save(os.path.join(root, path.replace('.', '.web.')))
            size = (100, 100*webim.size[1]//webim.size[0])
            thumbim = webim.resize(size, Image.ANTIALIAS)
            thumbim.save(os.path.join(root, path.replace('.', '.thumb.')))

