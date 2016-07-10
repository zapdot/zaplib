import os, json
from functools import total_ordering

@total_ordering
class GameVersion(object):
	def __init__(self, major=0, minor=0, patch=0):
		self.major = int(major)
		self.minor = int(minor)
		self.patch = int(patch)

	@classmethod
	def from_string(cls, ver_str):
		ver = ver_str.split('.')
		ver = ver + [0] * (3 - len(ver))
		return cls(ver[0], ver[1], ver[2])

	@classmethod 
	def from_path(cls, path):
		if os.path.exists(path):
			with open(path) as version_json:
				result = json.load(version_json)

				return cls(result['majorVersion'], result['minorVersion'], result['patchVersion'])

		return cls()


	def __str__(self):
		return "{}.{}.{}".format(self.major, self.minor, self.patch)

	def __eq__(self, other):
		return self.major == other.major and self.minor == other.minor and self.patch == other.patch

	def __gt__(self, other):
		if self.major != other.major:
			return self.major > other.major

		if self.minor != other.minor:
			return self.minor > other.minor

		if self.patch != other.patch:
			return self.patch > other.patch

		return False

	def bumpMajor(self):
		self.major += 1
		self.minor = 0
		self.patch = 0

	def bumpMinor(self):
		self.minor += 1
		self.patch = 0

	def bumpPatch(self):
		self.patch += 1

	def saveToFile(self, path):
		data = {
			'majorVersion': self.major,
			'minorVersion': self.minor,
			'patchVersion': self.patch
		}

		with open(path, 'w+') as version_json:
			json.dump(data, version_json, indent=4*' ')