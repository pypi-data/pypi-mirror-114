version = '0.1'

import datetime
def report(*args):
	print(datetime.datetime.now().strftime('%Y-%m-%d/%H-%M-%S.%f')+' '+' '.join(map(str,args)))

# ------------------------------------------------------
import os
class Query:
	def __init__(self, workroom='workroom', start_decay=5, is_report=True, random_order=False, is_debug=False, archive='ARCHIVEs'):
		assert not os.path.exists(workroom), f'there exists workroom already'
		self._workroom		= workroom
		self._start_decay	= start_decay
		self._is_report		= is_report
		self._random_order	= random_order
		self._is_debug		= is_debug
		self._archive 		= archive
		self._options		= {}
		self._queue 		= []

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
	def ready(self):
		self._check_options()
		self._parallel_options_to_serial_quque()
		self._options = {}
		if self._is_report:
			report('ready to run experiments.')
			report(f'  total query size:{len(self._queue)}')

	import itertools
	def _parallel_options_to_serial_quque(self):
		keys = list(self._options.keys())
		for values in itertools.product(*[self._options[k] for k in keys]):
			option = {key:value for key,value in zip(keys,values)}
			self._queue.append(option)

	def _check_options(self):
		assert 'scripts' in self._options, 'scripts are not specified'
		for key,value in self._options.items():
			assert isinstance(value,list), f'value must be list type'
		for script in self._options['scripts']:
			assert isinstance(script,str), 'each script must be str'
			assert os.path.exists(script), f'there is no such script'
	
	# ---------------------------------------------------------
	import random
	from collections	import deque
	from threading		import Thread
	def run(self, GPU_index=[]):
		assert len(self._options)==0,			'options must be empty'

		if self._random_order:
			random.shuffle(self._queue)

		deq	 = deque(self._queue)
		pool = []
		for i,idx in enumerate(self.GPU_index):
			pool.append(Thread(target=self._parallel_worker,args=(deq,idx,i)))

		for p in pool:
			p.start()
		for p in pool:
			p.join()

		# remove workspace if the directory exists and is empty
		if os.path.exists(self._workroom) and len(os.listdir(self._workroom))==0:
			os.rmdir(self._workroom)

		if self._is_report:
			report('finish all experiments')

	import time
	import datetime
	import subprocess
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

