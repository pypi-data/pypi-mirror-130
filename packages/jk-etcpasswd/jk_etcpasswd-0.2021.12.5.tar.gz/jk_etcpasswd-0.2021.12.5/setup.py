################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "This python module provides classes to parse and model data from /etc/passwd, /etc/shadow, /etc/group and /etc/gshadow.",
	include_package_data = False,
	install_requires = [
		"jk_typing",
	],
	keywords = [
		"passwd",
		"sysadmin",
	],
	license = "Apache2",
	name = "jk_etcpasswd",
	packages = [
		"jk_etcpasswd",
	],
	version = "0.2021.12.5",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
