version = '0.1'

import datetime
def report(*args):
	print(datetime.datetime.now().strftime('%Y-%m-%d/%H-%M-%S.%f')+' '+' '.join(map(str,args)))

# ------------------------------------------------------
import os
import time			# for start delay
import random		# for random order
import datetime		# for archive
import itertools	# for combination of options
import subprocess
from collections	import deque
from threading		import Thread
class Query:
	def __init__(self, workroom='workroom', start_decay=5, is_report=True, random_order=False, is_debug=False, archive='ARCHIVEs'):
		self._workroom		= workroom
		self._start_decay	= start_decay
		self._is_report		= is_report
		self._random_order	= random_order
		self._is_debug		= is_debug
		self._archive 		= archive
		self._options		= {}

	# ---------------------------------------------------------
	def _add_option(self, key, value):
		if key in self._options:
			print(f'warning - this key:{key} is already added. update the older value.')
		self._options[key] = value

	def add(self, key, value):
		self._add_option(key, value)

	def __setitem__(self, key, value):
		self._add_option(key, value)

	def __getitem__(self, key):
		return self._options[key]

	# ---------------------------------------------------------
	def ready(self, available_GPU_indexes=[-1,]):
		if not self._is_valid_options():
			print('something wrong, check experimental setup.')
			return
		self._available_GPU_index	= tuple(available_GPU_indexes)
		self._number_of_gpu 		= len(available_GPU_indexes)
		self._parallel_options_to_serial_quque()
		if self._is_report:
			report('ready to run experiments.')
			report(f'  total query size:{len(self._queue)}')

	def _is_valid_options(self):
		if 'scripts' not in self._options:
			print('warning - target scripts is not assigned.')
			return False
		for key,value in self._options.items():
			if not isinstance(value,list):
				print(f'warning - value must be list, but key:{key}\'s one is {type(value)}.')
				return False
		for script in self._options['scripts']:
			if not isinstance(script,str):
				print(f'warning - script value must be string, but {type(script)}.')
				return False
			if not os.path.exists(script):
				print(f'warning - there is no such script:{script}.')
				return False
		return True

	def _parallel_options_to_serial_quque(self):
		self._queue = []
		keys = list(self._options.keys())
		for values in itertools.product(*[self._options[k] for k in keys]):
			option = {key:value for key,value in zip(keys,values)}
			self._queue.append(option)
		if self._random_order:
			random.shuffle(self._queue)

	# ---------------------------------------------------------
	def run(self):
		if not hasattr(self, '_number_of_gpu'):
			print('experimental setup is not ready')
			print('  please finish it.')
			return
		deq	 = deque(self._queue)
		pool = []
		for i,idx in enumerate(self._available_GPU_index):
			pool.append(Thread(target=self._parallel_worker,args=(deq,idx,i)))
		for p in pool:
			p.start()
		for p in pool:
			p.join()
		if self._is_report:
			report('finish all experiments')

		# remove workspace if the directory exists and is empty
		if os.path.exists(self._workroom) and len(os.listdir(self._workroom))==0:
			os.rmdir(self._workroom)

	def _parallel_worker(self, deq, gpu, _worker_index):
		time.sleep(_worker_index * self._start_decay)
		workroom = f'{self._workroom}/{_worker_index:02d}/'
		while len(deq)!=0:
			option = deq.popleft()
			
			command = ['nohup','python']
			if self._is_debug:	command += ['-u']
			else:				command += ['-uO']
			command += [option['scripts']]

			for key, value in option.items():
				if key=='scripts':	continue
				if isinstance(value, list):	
					command += [f'--{key}']+values	# equal sign cannot deal with nargs well
				else:
					command += [f'--{key}={value}']
			command += [f'--gpu={gpu}']
			command += [f'--workroom={workroom}']

			if self._is_report:
				report(f'remains:{len(deq)} worker-index:{_worker_index} command:{" ".join(command)}')
			os.makedirs(workroom,exist_ok=True)
			with open(os.path.join(workroom, 'log.txt'),'w') as logfile:
				subprocess.call(command, stdout=logfile)

			archive = os.path.join(self._archive, str(datetime.datetime.now().strftime('%Y-%m-%d=%H-%M-%S-%f')))
			os.makedirs(archive,	exist_ok=True)
			os.rename(workroom,	archive)
			
	# ---------------------------------------------------------

