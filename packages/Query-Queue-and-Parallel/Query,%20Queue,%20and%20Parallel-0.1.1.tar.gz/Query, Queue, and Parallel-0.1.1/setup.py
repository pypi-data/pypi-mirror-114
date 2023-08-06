from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as fp:
	long_description = fp.read()

setup(
	name='Query, Queue, and Parallel',
	packages=['query_queue_and_parallel'],
	version='0.1.1',
	license='MIT',

	install_requires=[''],

	author='Takuo Hamaguchi',
	author_email='nyahha@gmail.com',

	url='https://gitlab.com/takuo-h/query-queue-and-parallel',

	description='Run experiments using specified GPU indexes',
	long_description=long_description,
	long_description_content_type='text/markdown',
	keywords='',

	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.6',
	],
)