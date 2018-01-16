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
ref = {
       'BNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_1.html',
       'BNU2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_2.html',
       'BNU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/bnu_3.html',
       'HNU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/hnu_1.html',
       'IBATRT': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ibatrt.html',
       'IPCAS1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_1.html',
       'IPCAS2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_2.html',
       'IPCAS5': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_5.html',
       'IPCAS6': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_6.html',
       'IPCAS8': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/ipcas_6.html',
       'NYU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/nyu_1.html',
       'SWU1': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_1.html',
       'SWU2': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_2.html',
       'SWU3': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_3.html',
       'SWU4': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/swu_4.html',
       'UWM': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/uwm.html',
       'XHCUMS': 'http://fcon_1000.projects.nitrc.org/indi/CoRR/html/xhcums.html'
       }

page_s = """
<div class="row">
<h3> Downloads </h3>
<h4> Functional MRI </h4>
</div>
<table>
  <tr>
    <th>Dataset</th>
    <th style="border-right: dashed 1px #ddd;">Covariates</th>
    <th colspan="6">Processed fMRI</th>
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
          <td><a href="{}">Preprocessed Images</a></td>
        </tr>
      </table>
    </td>
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
          <td><a href="{}">Cleaned Images</a></td>
        </tr>
      </table>
    </td>
    <td>
      <table>
        <tr>
          <td><a href="{}">ROI Timeseries</a></td>
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
          <td><a href="https://github.com/neurodata/ndmg/tree/{}">v{}</a></td>
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
    base = 'http://mrneurodata.s3-website-us-east-1.amazonaws.com/fmri/{}'
    return base.format('/'.join(things))
    

def main():
    bucket = 'mrneurodata'
    bpath = 'data/fmri/'
    tabl = open('table_fmri.html', 'w')
    tabl.write(page_s)

    dsets = scan_bucket(bucket, bpath)
    seqs = []#['NKI24', 'resources', 'MRN114', 'Jung2015']
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
            derpath = path + '/' + ver + '/func'
            derderivs = scan_bucket(bucket, derpath)
            if derderivs:
                derderivs = [to_url((dset, ver, 'func', d, '')) for d in derderivs]
            else:
                derderivs = ['#']*5
            qapath = path + '/' + ver
            qaderivs = scan_bucket(bucket, qapath)
            if qaderivs:
                qaderivs = [to_url((dset, ver, d, '')) for d in derderivs]
                derderivs += qaderivs
            else:
                derderivs += ['#']*3
            if not derderivs:
                derderivs = ['#'] * 8
            else:
                print(dset)
                d = derderivs
                derivs = [d[2], d[3], d[0], d[4], d[1], d[7]]
                derivs += ['m3r-release', ver.replace('-', '.', 2).strip('ndmg_')]
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
