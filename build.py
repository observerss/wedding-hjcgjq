#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#   Copyright 2013 Jingchao Hu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
############################################################################

import os
import random
from multiprocessing import Pool, cpu_count

BUILD_ROOT = '/tmp/'

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    return d

def create_build_path():
    dirname = hex(random.randint(2**24, 2**32))[2:]
    build_path = os.path.join(BUILD_ROOT, dirname)
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    return build_path
    
def build_one(path):
    """ build rst file on 'src/'+path, generate pdf on 'dist/'+path """
    build_path = create_build_path()

    if os.path.exists(os.path.join('src', path)) and path.endswith('.rst'):
        os.system('rm -rf {}/*'.format(build_path))
        os.system('cp conf/* {}'.format(build_path))
        os.system('cp src/{} {}/'.format(path, build_path))
        rstfname = path.rsplit('/', 1)[-1]
        name, dot, ext = rstfname.partition('.')
        xetexfname = name + dot + 'xetex'
        pdffname = name + dot + 'pdf'
        os.system('cd {build_path} && rst2xetex.py --latex-preamble="" {rstfname} {xetexfname} && xelatex {xetexfname}'.format(**locals()))
        target_path = ensure_dir('dist/{}'.format(path))
        os.system('mv {build_path}/*.pdf {target_path}'.format(**locals()))

    os.system('rm -rf {}'.format(build_path))

def clear_all():
    os.system('rm -rf dist/*')

def build_all(concurrency=None):
    clear_all()
    pool = Pool(concurrency or cpu_count()*2)
    for root, dirs, files in os.walk('src'):
        for filename in files:
            if filename.endswith('.rst'):
                #build_one(os.path.join(root[4:], filename))
                pool.apply_async(build_one, [os.path.join(root[4:], filename)])
    pool.close()
    pool.join()

if __name__ == '__main__':
    build_all()
