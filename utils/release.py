#!/usr/bin/env python
'''
'''

import argparse
import sys
import core

def checkPyPiReleaseVersions(test=True):
	#check if version released to pypitest already
	#check if version released to pypi already

def main(args=[]):
	argParser = argparse.ArgumentParser(prog='release', description='This utility is used to push a release to github and publish on pypi (test, then normal).')
	argNamespace = argParser.parse_args(args)

	#get local package version
	#check github released versions
	#check pypi released versions

	#if released on github already, check if released on pypitest/pypi.
	#if released on pypi, increment version in file, commit all changes to github, release on pypi test
	#if not released on pypi, switch to the tag in github and release on pypi

if __name__ == '__main__':
	tempArgs=sys.argv
	#trim off the module name
	if len(tempArgs)<2:
		tempArgs=[]
	else:
		tempArgs=tempArgs[1:]
	main(tempArgs)
