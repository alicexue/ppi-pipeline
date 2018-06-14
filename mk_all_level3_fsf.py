"""
Get information to run mk_level3_fsf on multiple subjects, tasks, runs, etc
Called by run_level3_feat.py
"""
# Created by Alice Xue, 06/2018

from directory_struct_utils import *
import mk_level3_fsf
import os
import sys
import subprocess
import argparse
import json

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='setup_jobs')
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
    # set up boolean flags

    parser.add_argument('--studyid', dest='studyid',
        required=True,help='Study ID')
    parser.add_argument('--basedir', dest='basedir',
        required=True,help='Base directory (above studyid directory)')
    parser.add_argument('--modelnum', dest='modelnum',type=int,
        default=1,help='Model number')
    parser.add_argument('--subs', dest='subids', nargs='+',
        default=[],help='subject identifiers (not including prefix "sub-")')
    parser.add_argument('--sessions', dest='sessions', nargs='+',
        default=[],help='Name of session (not including prefix "sub-"')

    args = parser.parse_args(argv)
    return args

def main(argv=None):
	args=parse_command_line(argv)
	print args

	studyid=args.studyid
	basedir=args.basedir
	modelnum=args.modelnum
	subids=args.subids

	hasSessions=False
	studydir=os.path.join(basedir,studyid)
	study_info=get_study_info(studydir,hasSessions)
	if len(study_info.keys()) > 0:
		if not study_info[study_info.keys()[0]]: # if empty
			hasSessions=True
			study_info=get_study_info(studydir,hasSessions)

	print study_info

	jobs = []
	if len(subids)==0:
		subs=study_info.keys()
	else:
		subs=[]
		for sub in subids:
			subs.append('sub-'+sub)
	list.sort(subs)
	# iterate through runs based on the runs the first subject did
	subid=subs[0]
	sub=subid[len('sub-'):]
	if hasSessions:
		sessions=study_info[subid].keys()
		list.sort(sessions)
		for ses in sessions:
			sesname=ses[len('ses-'):]
			tasks=study_info[subid][ses].keys()
			list.sort(tasks)
			for task in tasks:
				args=[studyid,subids,task,basedir,modelnum,sesname]
				jobs.append(args)
	else:
		sesname=''
		tasks=study_info[subid].keys()
		list.sort(tasks)
		for task in tasks:
			args=[studyid,subids,task,basedir,modelnum,sesname]
			jobs.append(args)

	all_copes=[]
	for job_args in jobs:
		args=job_args
		copes=mk_level3_fsf.mk_level3_fsf(studyid=args[0],subids=args[1],taskname=args[2],basedir=args[3],modelnum=args[4],sesname=args[5])
		all_copes+=copes

	print len(all_copes), "jobs"
	return all_copes

if __name__ == '__main__':
    main()