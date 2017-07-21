#!/usr/bin/env python
'''
This module can be used to import python packages and install them if not already installed.
'''
import os
import sys
import subprocess
import tempfile
import urllib

_pipSetupUrl = 'https://bootstrap.pypa.io/get-pip.py'

PIP_OPTIONS=[]
GET_PIP_OPTIONS=[]
PYTHON_EXE_PATH=sys.executable
HTTPS_PROXY=None

def _updateModVarsFromEnv():
	if os.environ.get('PYTHON_EXE_PATH') is not None:
		global PYTHON_EXE_PATH
		PYTHON_EXE_PATH=os.environ['PYTHON_EXE_PATH']

	if os.environ.get('GET_PIP_OPTIONS') is not None:
		global GET_PIP_OPTIONS
		GET_PIP_OPTIONS=os.environ['GET_PIP_OPTIONS']

	if os.environ.get('PIP_OPTIONS') is not None:
		global PIP_OPTIONS
		PIP_OPTIONS=os.environ['PIP_OPTIONS']

	global HTTPS_PROXY
	if os.environ.get('https_proxy') is not None and os.environ['https_proxy']!='':
		HTTPS_PROXY=os.environ['https_proxy']
	elif os.environ.get('HTTPS_PROXY') is not None and os.environ['HTTPS_PROXY']!='':
		HTTPS_PROXY=os.environ['HTTPS_PROXY']
	elif os.environ.get('http_proxy') is not None and os.environ['http_proxy']!='':
		HTTPS_PROXY=os.environ['http_proxy']
	elif os.environ.get('HTTP_PROXY') is not None and os.environ['HTTP_PROXY']!='':
		HTTPS_PROXY=os.environ['HTTP_PROXY']

def _installWithPip(pipName, pythonExePath=eval('PYTHON_EXE_PATH'), getPipOpts=eval('GET_PIP_OPTIONS'), pipOpts=eval('PIP_OPTIONS')):
	'''
	:param pipName:
	:return:
	'''
	pipAvail = False
	try:
		import pip as pip
		pipAvail = True
	except ImportError:
		pass

	proxyArgs = []
	if HTTPS_PROXY is not None:
		proxyArgs.append(HTTPS_PROXY)

	if not pipAvail:
		print 'Downloading pip installer:', _pipSetupUrl
		tmpDir = tempfile.gettempdir()
		pipSetupFilePath = os.path.join(tmpDir, os.path.basename(_pipSetupUrl))
		urllib.urlretrieve(_pipSetupUrl, pipSetupFilePath)

		pipSetupArgs = [pythonExePath, pipSetupFilePath]
		pipSetupArgs.extend(proxyArgs)
		pipSetupArgs.extend(getPipOpts)
		print 'Executing pip installer:', ' '.join(pipSetupArgs)
		subprocess.Popen(pipSetupArgs)

		pipAvail = False
		try:
			import pip as pip
			pipAvail = True
		except ImportError:
			pass

	if pipAvail:
		pipArgs = ['install', pipName]
		pipArgs.extend(proxyArgs)
		pipArgs.extend(pipOpts)
		print 'Installing', pipName + ':', 'pip', ' '.join(pipArgs)
		pip.main(pipArgs)
	else:
		print 'Pip not available...'
		#Look at pypi repo for installers
		#Download and use installer if available


def impstall(module, items={}, pipPackage=None):
	'''
	This is the main function of the module.  It will import `importName` if it can.  If not, it will try to install it.

	First, it tries to import the module.  If pip is not installed, it tries to install pip.  If that fails, it tries to install from pip.
	If the pip install fails or the module fails to install from pip, we try to find a module installer on the internet.
	If that fails, an exception is raised.

	:param module: str
	This is the name of the module that we want to import or import from.  It should be the name that would be used in a standard import statement.
	:param pipPackage: str, optional
	This is the name of the module as it would be requested through pip.  If not provided, it is set to `module`
	:return: N/A
	'''

	baseModule=module.split('.')[0]

	if pipPackage is None:
		pipPackage = baseModule

	if len(items) == 0:
		builtImportString = 'import ' + module
	else:
		builtImportString = 'from ' + module + ' import '
		tempIdx = 0
		for key in items:
			if tempIdx > 0:
				builtImportString += ', '
			builtImportString += key
			if items[key] is not None and items[key] != '':
				builtImportString += ' as ' + items[key]
			tempIdx += 1

	packageAlreadyInstalled = False
	try:
		exec('import '+baseModule)
		packageAlreadyInstalled = True
	except ImportError:
		pass

	if not packageAlreadyInstalled:
		_updateModVarsFromEnv()
		_installWithPip(pipPackage)

	exec (builtImportString, sys._getframe(1).f_globals)


now = impstall
