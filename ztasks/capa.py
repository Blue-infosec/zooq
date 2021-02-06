#!/usr/bin/env python3
#
# Author: Coleman Kane <ckane@colemankane.org>
# This module will run "exiftool" against an artifact and will
# write results into a file named exiftool_output.csv
#
import sqlite3
import os
from subprocess import Popen, DEVNULL, PIPE

from ztasks.base_zooqdb_task import base_zooqdb_task

class capa(base_zooqdb_task):
    def __init__(self, objid, dir):
        super(capa, self).__init__(objid, dir)

    def dowork(self):
        dbconn = sqlite3.connect('{dir}/samples.sqlite'.format(dir=self.dirname()))
        cur = dbconn.cursor()
        cur.execute('SELECT `mwpath` from `samples` WHERE `mwid`=?', (self.objid(),))
        res = cur.fetchall()
        dbconn.close()
        if res:
            mwpath = res[0][0]
            mwdir = os.path.dirname(mwpath)
            with open(mwdir+'/capa.json', 'wb') as outfile:
                proc = Popen(['capa', '-j', '-q', '-r', 'capa-rules', mwpath],
                             stderr=DEVNULL, stdout=outfile, stdin=DEVNULL)
                proc.wait()
