import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="cryptosharp",
	packages=setuptools.find_packages(),
	include_package_data = True,
	version="0.0.1",
	author="K0lb3",
	description="wrapper around C# cryptography libraries using pythonnet",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/K0lb3/cryptosharp",
	download_url="https://github.com/K0lb3/cryptosharp/tarball/master",
	keywords=['python', 'csharp', 'cryptography', 'pythonnet', 'wrapper'],
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	install_requires=[
		"pythonnet"
	]
)
