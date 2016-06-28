import os, json

__ENV_VAR__ = "CONFIGBOX_LOCAL_PATH"

CONFIGBOX_LOCAL_PATH = None

for k,v in os.environ.iteritems():
	if k == __ENV_VAR__:
		CONFIGBOX_LOCAL_PATH = v

if not CONFIGBOX_LOCAL_PATH:
	print "error: {} not set in environment.".format(__ENV_VAR__)

def _from_json(file):
	result = {}

	if os.path.exists(file):
		with open(file, 'r+') as jsonfile:
			result = json.load(jsonfile)

	return result	

class ConfigBox(object):
	def __init__(self):
		self._configs = {}

		# load configs
		cfg_files = [f for f in os.listdir(CONFIGBOX_LOCAL_PATH) if f[-5:] == ".json"]

		for file in cfg_files:
			name = file[:-5]
			path = os.path.join(CONFIGBOX_LOCAL_PATH, file)
			self._configs[name] = ConfigPath(_from_json(path))

	def __getitem__(self, key):
		if key in self._configs:
			return self._configs[key]
		else:
			return None

	def find(self, path, value):
		for name, config in self._configs.iteritems():
			try:
				data = reduce(lambda d,k: d[k], path, config())
			except:
				continue
			else:
				if data == value:
					return config

		return None


class ConfigPath(object):
	def __init__(self, data):
		self._data = data
		self._cache = {}

	def __getattr__(self, key):
		if key in self._cache:
			return self._cache[key]
		elif key in self._data:
			if isinstance(self._data[key], dict):
				path = ConfigPath(self._data[key])
				self._cache[key] = path
				return path
			elif key in self._data:
				return self._data[key]
			else:
				return None

	def __call__(self):
		return self._data
