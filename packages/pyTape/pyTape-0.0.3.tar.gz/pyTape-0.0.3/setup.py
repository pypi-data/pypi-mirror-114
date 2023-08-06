import setuptools
with open("readme.md","r") as f:
	long_description=f.read()
setuptools.setup(
	name="pyTape",
	version="0.0.3",
	author="kawaai-hina",
	author_email="kawaai@qq.com",
	description="Tape",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kawaai-hina/pyTape",
	include_package_data=False,
	package_data={},
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)