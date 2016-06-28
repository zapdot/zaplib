from siesta import *
from siesta.auth import APIKeyAuth

class CloudBuildAPI(object):

	def __init__(self, orgid):
		import ConfigParser

		config = ConfigParser.ConfigParser()
		config.read('config/tokens.ini')

		token = config.get('cloudbuild', 'token')
		auth = APIKeyAuth("Basic %s" % token, "Authorization")

		self.api = API('https://build-api.cloud.unity3d.com/api/v1/', auth)
		self.orgid = orgid

	def _api_projects(self, pid):
		return self.api.orgs(self.orgid).projects(pid)

	def _clean_buildtarget(self, bt):
		target = {k : bt.attrs.get(k, None) for k in ('buildtargetid', 'enabled', 'name', 'platform')}

		if 'builds' in bt.attrs:
			target['build'] = self._clean_build(bt.attrs['builds'][0])

		return target 

	def _clean_build(self, b):
		result = {}
		result['number'] = b['build']
		result['status'] = b['buildStatus']
		result['branch'] = b.get('scmBranch', '')
		result['sha'] = b.get('lastBuiltRevision', '')
		result['platform'] = b['platform']
		result['totalTimeInSeconds'] = b.get('totalTimeInSeconds', 0)

		return result

	# List all projects 
	# GET /projects
	def get_projects(self):
		
		projects, resp = self.api.projects().get()

		results = []

		for p in projects:
			prj = {k : p.attrs.get(k, None) for k in ('guid', 'name', 'orgid', 'projectid')}
			results.append(prj)

		return results


	# List all build targets for a project
	# GET /orgs/{orgid}/projects/{projectid}/buildtargets
	def get_buildtargets(self, project_id):
		cb = self._api_projects(project_id)

		args = {
			'include_last_success': "true"
		}

		targets, resp = cb.buildtargets().get(**args)

		results = []

		for t in targets:
			target = self._clean_buildtarget(t)

			results.append(target)

		return results

	# Get a build target
	# GET /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}
	def get_buildtarget(self, project_id, buildtarget_id):
		cb = self._api_projects(project_id)

		target, resp = cb.buildtargets(buildtarget_id).get()

		result = self._clean_buildtarget(target)

		return target

	# Get a list of builds for a buildtarget
	# GET /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}/builds
	def get_builds(self, project_id, buildtarget_id, per_page=25, page=1):
		cb = self._api_projects(project_id)

		args = {
			'per_page': per_page,
			'page': page,
			# 'buildStatus': '',
			# 'platform': ''
		}

		builds, resp = cb.buildtargets(buildtarget_id).builds.get(**args)

		result = [self._clean_build(b.attrs) for b in builds]

		return result

	# Build Status
	# GET /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}/builds/{number}
	def get_buildstatus(self, project_id, buildtarget_id, build_num):
		cb = self._api_projects(project_id)

		build, resp = cb.buildtargets(buildtarget_id).builds(build_num).get()

		return self._clean_build(build.attrs)


	# Create new build
	# POST /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}/builds
	def create_build(self, project_id, buildtarget_id='_all'):
		cb = self._api_projects(project_id)

		args = {
			'clean': True,
			'delay': 0,
			'commit': ''
		}

		builds, resp = cb.buildtargets(buildtarget_id).builds.post_json(**args)

		return [self._clean_build(b.attrs) for b in builds]

	# Cancel all builds
	# DELETE /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}/builds
	# Cancel all builds in progress for this build target (or all targets, if '_all' is specified as the buildtargetid). Canceling an already finished build will do nothing and respond successfully.
	def cancel_builds(self, project_id, buildtarget_id='_all'):
		cb = self._api_projects(project_id)

		build, resp = cb.buildtargets(buildtarget_id).builds.delete()

		return resp.status == 204
		

	# Cancel build
	# DELETE /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}/builds/{number}
	def cancel_build(self, project_id, buildtarget_id, build_num):
		cb = self._api_projects(project_id)

		build, resp = cb.buildtargets(buildtarget_id).builds(build_num).delete()

		return resp.status == 204

