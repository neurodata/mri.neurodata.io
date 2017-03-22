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
       'NKI1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/nki_1.html',
       'Templeton255': '#',
       'Templeton114': '#',
       'MRN1313': '#'}

page_s = """
<div class="row">
<h3> Downloads </h3>
<h4> Diffusion MRI </h4>
</div>
<table>
  <tr>
    <th>Dataset</th>
    <th style="border-right: dashed 1px #ddd;">Covariates</th>
    <th colspan="5">Processed DWI</th>
    <th>Code</th>
  </tr>
"""
page_e = """
</table>
"""

row_s = """
  <tr>
    <td><a href="{}">{}</a></td>
    <td style="border-right: dashed 1px #ddd;"><a href="{}">[@csv]</a></td>
"""
row_bulk = """
    <td>
      <table>
        <tr>
          <td><a href="{}">Aligned Images</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="{}">Tensors</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="{}">Fibers</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="{}">Graphs</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="{}">QA</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="https://github.com/neurodata/ndmg/tree/v{}">v{}</a></td>
        </tr>
      </table>
    </td>
"""
row_e = """
  </tr>
"""

def scan_bucket(bucket, path):
    path = path.strip('/')
    cmd = 'aws s3 ls s3://{}/{}/'.format(bucket, path)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    out = [d.split(' ')[-1].strip('/') for d in re.findall('(.+)\n', out)]
    return out


def to_url(things):
    base = 'http://mrneurodata.s3-website-us-east-1.amazonaws.com/{}'
    return base.format('/'.join(things))
    

def main():
    bucket = 'mrneurodata'
    bpath = 'data/'
    tabl = open('table_dwi.html', 'w')
    tabl.write(page_s)

    dsets = scan_bucket(bucket, bpath)
    seqs = ['NKI24', 'resources', 'MRN114', 'Jung2015']
    for seq in seqs:
        dsets.remove(seq) if seq in dsets else dsets

    for dset in dsets:
        path = bpath + dset
        dirt = scan_bucket(bucket, path)
        csv = [d for d in dirt if '.csv' in d]
        if not csv:
            csv = "#"
        else:
            csv = to_url((path, csv[0])) 
        tabl.write(row_s.format(ref[dset], dset, csv))

        vers = [d for d in dirt if 'ndmg' in d]
        if vers:
            ver = sorted(vers, reverse=True)[0]
            path += '/' + ver
            derivs = scan_bucket(bucket, path)
            if not derivs:
                derivs = ['#'] * 7
            else:
                derivs = [to_url((dset, ver, d, '')) for d in derivs]
                d = derivs
                derivs = [d[3], d[4], d[0], d[1], d[2]]
                derivs += [ver.replace('-', '.', 2).strip('ndmg_')] * 2
                tabl.write(row_bulk.format(*derivs))

        tabl.write(row_e)
    tabl.write(page_e)
    tabl.close()
    pass


if __name__ == "__main__":
    main()


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
