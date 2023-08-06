import setuptools
from setuptools import setup

# with open("README.md", "r") as fh:
# 	long_description = fh.read()

setup(    
	name='bluebeam_production5', # Name of the PyPI package
	author='Clyde Slichter',
	package_dir={"": "src"},
	packages = setuptools.find_packages(where="src"),
	package_data={
		"bluebeam": ["*.txt","images/*.png", "images/*/*.png", "images/*/*/*.png", "images/*/*/*.PNG", "Sounds/*.wav", "Sounds/*.mod", "Sounds/*.xm", "tilemap_resources/*", "tilemap_resources/*/*", "tilemap_resources/*/*/*", "tilemap_resources/*/*/*/*"]
	},
	author_email='cnslichter@ufl.edu',
	version='1.0.0',
	description='A side scroller, tile map, shooter game', 
	#long_description=long_description,
	#url='https://github.com/josephmbarron/bluebeam',
	install_requires=[
				'pygame>=2.0.1', 
				'PyTMX>=3.25', 
				'wheel',
				'cx-freeze'

	], 
	keywords='pygame, game, shooter', 

	#py_modules=["GlobalVars"],
	python_requires='>=3.8',
	entry_points ={
		'console_scripts': [
			'gameplay_BB5 = bluebeam.Engine:main',
		],
	},
	include_package_data=True,
)
