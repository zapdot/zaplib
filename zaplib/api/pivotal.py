from siesta import *
from siesta.auth import APIKeyAuth

from zaplib.configbox import config

class PivotalAPI(object):

	def __init__(self, config_id = None):
		auth = APIKeyAuth(config['api'].pivotal, "X-TrackerToken")

		self.api = API('https://www.pivotaltracker.com/services/v5', auth)

		if config_id:
			self.project_id = config[config_id].pivotal.project_id
		else:
			self.project_id = None

	def _api_proj(self, pid):
		return self.api.projects(pid)

	def get_epics(self, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		results, resp = pivotal.epics().get()

		return [epic.attrs for epic in results]

	def search(self, query, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		args = {
			'query': query
		}

		results, resp = pivotal.search.get(**args)

		return results

	def create_story(self, name, description, labels, story_type, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		args = {
			'name': name,
			'description': description,
			'story_type': story_type,
			'labels[]': labels
		}

		pivotal.stories().post(**args)

	def update_story(self, story_id, args, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		pivotal.stories(story_id).put(**args)

	def get_story(self, story_id, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		results, resp = pivotal.stories(story_id).get()

		return results.attrs

	def set_story_estimate(self, story_id, estimate, project_id = None):
		project_id = self.project_id if not project_id else project_id

		args = {
			'estimate': estimate
		}

		self.update_story(story_id, args, project_id)

	def set_story_state(self, story_id, state, project_id = None):
		project_id = self.project_id if not project_id else project_id

		args = {
			'current_state': state
		}

		self.update_story(story_id, args, project_id)

	def link_story(self, story_id, project_id = None):
		project_id = self.project_id if not project_id else project_id

		return "https://www.pivotaltracker.com/n/projects/{}/stories/{}".format(project_id, story_id)

	def get_comments(self, story_id, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		results, resp = pivotal.stories(story_id).comments().get()

		return [comment.attrs for comment in results]

	def create_comment(self, story_id, text, project_id = None):
		project_id = self.project_id if not project_id else project_id

		pivotal = self._api_proj(project_id)

		args = {
			'text': text
		}

		pivotal.stories(story_id).comments().post(**args)

	def get_person(self, person_id, project_id = None):
		project_id = self.project_id if not project_id else project_id

		args = {
			'project_id': project_id
		}

		results, resp = self.api.my.people.get(**args)

		people = [p.attrs['person'] for p in results]

		for person in people:
			if person['id'] == person_id:
				return person

		return None


