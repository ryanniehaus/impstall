#!/usr/bin/env python

import argparse
import sys
import core

def main(args=[]):
	argParser = argparse.ArgumentParser(prog='impstall', description='This utility is used to install a python package via pip if it is not installed already.')
	argParser.add_argument('-p', '--pipname')
	argParser.add_argument('importname')
	argNamespace = argParser.parse_args(args)

	core.impstall(argNamespace.importname, pipPackage=argNamespace.pipname)

if __name__ == '__main__':
	tempArgs=sys.argv
	#trim off the module name
	if len(tempArgs)<2:
		tempArgs=[]
	else:
		tempArgs=tempArgs[1:]
	main(tempArgs)
