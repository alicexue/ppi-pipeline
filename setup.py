#!/usr/bin/env python
"""
Create model directories based on structure of fmriprep directory
Creates empty_condition_key, task_contrasts, and model_params files
"""

# Created by Alice Xue, 06/2018

import json
import os
import sys

from setup_utils import *

def main():
	if len(sys.argv) < 4:
		print "usage: setup.py <studyid> <basedir> <modelname>"
		sys.exit(-1)
	studyid=sys.argv[1]
	basedir=sys.argv[2]
	modelname=sys.argv[3]
	create_model_level1_dir(studyid,basedir,modelname)
	create_empty_condition_key(studyid,basedir,modelname)
	create_empty_task_contrasts_file(studyid,basedir,modelname)
	create_level1_model_params_json(studyid,basedir,modelname)
	check_model_params_cli(studyid,basedir,modelname)
	modeldir=os.path.join(basedir,studyid,'model','level1','model-%s'%modelname)
	print '\nMake sure to modify:'
	print '\t', modeldir+'/condition_key.json'
	print '\t', modeldir+'/task_contrasts.json'
	print '\tand the EV files under the onset directories'


if __name__ == '__main__':
	main()
