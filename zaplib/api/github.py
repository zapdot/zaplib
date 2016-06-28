from siesta import *
from siesta.auth import APIKeyAuth

class GitHubAPI(object):

	def __init__(self, owner, repository):
		import ConfigParser

		config = ConfigParser.ConfigParser()
		config.read('config/tokens.ini')

		token = config.get('github', 'token')
		auth = APIKeyAuth("token %s" % token, "Authorization")

		self.api = API('https://api.github.com', auth)
		self.owner = owner
		self.repository = repository


	def _api_path(self, *args):
		result = self.api.repos

		for apidir in args:
			result = getattr(result, apidir)

		return result

	# GET /repos/:owner/:repo/commits
	def commits(self, branch, since):

		args = {
			'sha': branch,
			'since': since
		}

		git = self._api_path(self.owner, self.repository)

		commits, resp = git.commits().get(**args)

		results = [x.commit for x in commits]

		return results

	# GET /repos/:owner/:repo/commits/:sha
	def commit(self, sha):
		git = self._api_path(self.owner, self.repository, "commits", sha)

		commit, resp = git.get()

		return commit

	# GET /repos/:owner/:repo/pulls/:number/commits
	def commits_from_pr(self, request_id):

		git = self._api_path(self.owner, self.repository, "pulls", str(request_id))
		commits, resp = git.commits().get()

		results = [x.commit for x in commits]

		return results






