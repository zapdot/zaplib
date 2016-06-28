from siesta import *
from siesta.auth import APIKeyAuth

class PivotalAPI(object):

	def __init__(self, project_id, config_dir = None):
		import ConfigParser

		config = ConfigParser.ConfigParser()

		if config_dir:
			config.read('{}/tokens.ini'.format(config_dir))
		else:
			config.read('config/tokens.ini')

		token = config.get('pivotal', 'token')
		auth = APIKeyAuth(token, "X-TrackerToken")

		self.id = project_id
		self.api = API('https://www.pivotaltracker.com/services/v5', auth)
		self.project = self.api.projects(self.id)

	def get_epics(self):
		results, resp = self.project.epics().get()
		return results

	def search(self, query):
		args = {
			'query': query
		}

		results, resp = self.project.search.get(**args)
		return results

	def create_story(self, name, labels):
		args = {
			'name' : name,
			'labels[]' : labels
		}

		self.project.stories().post(**args)

	def update_story(self, story_id, args):

		self.project.stories(story_id).put(**args)

	def set_story_estimate(self, story_id, estimate):
		args = {
			'estimate': estimate
		}

		self.update_story(story_id, args)

	def set_story_state(self, story_id, state):
		args = {
			'current_state': state
		}

		self.project.stories(story_id).put(**args)

	def link_story(self, story_id):
		return "https://www.pivotaltracker.com/n/projects/{}/stories/{}".format(self.id, story_id)


