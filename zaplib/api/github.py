from siesta import *
from siesta.auth import APIKeyAuth

from zaplib.configbox import config

class GitHubAPI(object):

	def __init__(self, config_id = None):
		auth = APIKeyAuth("token %s" % config['api'].github, "Authorization")

		self.api = API('https://api.github.com', auth)

		if config_id:
			self.owner = config[config_id].github.owner
			self.repo = config[config_id].github.repo
		else:
			self.owner = None
			self.repo = None

	def _api_path(self, *args):
		result = self.api.repos

		for apidir in args:
			result = getattr(result, apidir)

		return result

	# GET /repos/:owner/:repo/commits
	def commits(self, branch, since, owner=None, repo=None):
		owner = self.owner if not owner else owner
		repo = self.repo if not repo else repo

		args = {
			'sha': branch,
			'since': since
		}

		git = self._api_path(owner, repo)

		commits, resp = git.commits().get(**args)

		results = [x.commit for x in commits]

		return results

	# GET /repos/:owner/:repo/commits/:sha
	def commit(self, sha, owner=None, repo=None):
		owner = self.owner if not owner else owner
		repo = self.repo if not repo else repo

		git = self._api_path(owner, repo, "commits", sha)

		commit, resp = git.get()

		return commit

	# GET /repos/:owner/:repo/pulls/:number/commits
	def commits_from_pr(self, request_id, owner=None, repo=None):
		owner = self.owner if not owner else owner
		repo = self.repo if not repo else repo

		git = self._api_path(owner, repo, "pulls", str(request_id))
		commits, resp = git.commits().get()

		results = [x.commit for x in commits]

		return results

	def link_sha(self, sha):
		return "https://github.com/{}/{}/commits/{}".format(self.owner, self.repo, sha)






