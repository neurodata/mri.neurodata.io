#!/usr/bin/env python

# Copyright 2014 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# update_site.py
# Created by Greg Kiar on 2017-03-04.
# Email: gkiar@jhu.edu

from subprocess import Popen, PIPE
import os
import sys
import re

opj = os.path.join

def scan_bucket(bucket, path):
    path = path.strip('/')
    cmd = 'aws s3 ls s3://{}/{}/'.format(bucket, path)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    out = re.findall('PRE (.+)', out)
    return out


def main():
    bucket = 'mrneurodata'
    bpath = 'data/'
    outf = open('table2.html', 'w')

    dsets = scan_bucket(bucket, bpath)
    for dset in dsets:
        path = bpath + dset
        dirt = scan_bucket(bucket, path)
        vers = [d for d in dirt if 'ndmg' in d]
        if not vers:
            print("{} has not yet been processed".format(dset))
        else:
            print("{} has been processed by the following pipelines: ".format(dset) +\
                  ", ".join(vers))

    pass


if __name__ == "__main__":
    main()

"""
Key
---
*_s: start
*_e: end
"""
ref = {'SWU4': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_4.html',
       'HNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/hnu_1.html',
       'BNU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_3.html',
       'BNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_1.html',
       'KKI2009': 'http://mri.kennedykrieger.org/databases.html#Kirby21',
       'NKIENH': 'http://fcon_1000.projects.nitrc.org/indi/enhanced/',
       'NKI1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/nki_1.html'}

page_s = """
<div class="row">
<h3> Downloads </h3>
</div>
<table>
  <tr>
    <th>Dataset</th>
    <th style="border-right: dashed 1px #ddd;">Covariates</th>
    <th colspan="5">Processed DWI</th>
    <th style="border-right: dashed 1px #ddd;">Code</th>
    <th colspan="5">Processed fMRI</th>
    <th>Code</th>
  </tr>
"""

page_e = """
</table>
"""

row_s = """
  <tr>
    <td>{}<a href="{}">[ref]</a></td>
    <td style="border-right: dashed 1px #ddd;"><a href="{}">[@csv]</a></td>
"""

row_e = """
  </tr>
"""
