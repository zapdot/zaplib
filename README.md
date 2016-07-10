# zaplib

This library encompasses much of the magic that we use to automate many of our services and development environment. Since there's a nonzero chance this may help others, we've put it out there!

We'd love to hear any feedback/suggestions/questions.

## Installation

As this package will be in constant development, it's suggested to install this package in development mode.

    $ git clone https://github.com/zapdot/zaplib.git
    $ cd zaplib/
    $ pip install -e .

## Prereqs

This package also requires the following libraries:

* Our internal version of [Siesta](https://github.com/zapdot/siesta) to work with RESTful services.

## Web Services

### Unity CloudBuild

##### Python Import

    from zaplib.api.cloudbuild import CloudBuildAPI

##### Python Setup

    cloudbuild = CloudBuildAPI("proj_id")

##### ConfigBox Setup

The following variables will be used:

* `config['api'].cloudbuild` (UCB API Key)
* `config['proj_id'].cloudbuild.project_id` (UCB Project ID)
* `config['proj_id'].cloudbuild.org_id` (UCB Organziation ID)

##### Methods

NOTE: `project_id`/`org_id` is autofilled with the ConfigBox vars for the given "proj_id" in the Python Setup. These can be overwritten for every method except `get_projects()`. This is great if you need your script to access multiple projects/orgs at once.

**List all projects accessible by the UCB API Key**

    cloudbuild.get_projects()

**List all build targets for a project**

    cloudbuild.get_buildtargets()

**Get a build target**

    cloudbuild.get_buildtarget(buildtarget_id)

**Get a list of builds for a buildtarget**

    cloudbuild.get_builds(buildtarget_id, per_page=25, page=1)

**Build Status**

    cloudbuild.get_buildstatus(buildtarget_id, build_num)

**Create new build**

    cloudbuild.create_build(buildtarget_id='_all')

**Cancel all builds**

    cloudbuild.cancel_builds(buildtarget_id='_all')

**Cancel build**

    cloudbuild.cancel_build(buildtarget_id, build_num)

### GitHub

##### Python Import

    from zaplib.api.github import GitHubAPI

##### Python Setup

    github = GitHubAPI("proj_id")

##### ConfigBox Setup

The following variables will be used:

* `config['api'].github` (GitHub User API Key)
* `config['proj_id'].git.owner` (GitHub Owner ID)
* `config['proj_id'].git.repo` (GitHub Repository ID)

##### Methods

NOTE: `owner`/`repo` is autofilled with the ConfigBox var for the given "proj_id" in the Python Setup. These can be overwritten for every method. This is great if you need your script to access multiple projects at once.

**Get all commits to a branch since a certain date.**

    github.commits(branch, since)

**Get a commit for a given SHA hash.**

    github.commit(sha)

**Get all commits from a given Pull Request**

    github.commits_from_pr(request_id)

### PivotalTracker

##### Python Import

    from zaplib.api.pivotal import PivotalAPI

##### Python Setup

    tracker = PivotalAPI("proj_id")

##### ConfigBox Setup

The following variables will be used:

* `config['api'].pivotal` (Pivotal User API Key)
* `config['proj_id'].pivotal.project_id` (Pivotal Project ID)

##### Methods

NOTE: `project_id` is autofilled with the ConfigBox var for the given "proj_id" in the Python Setup. These can be overwritten for every method. This is great if you need your script to access multiple projects at once.

**Get epics for the current project.**

    tracker.get_epics()

**Search the project with a given query.**

    tracker.search(query)

**Create a story with a given name and set of labels**

    tracker.create_story(name, labels)

**Update a story with the given arguments.**

    tracker.update_story(story_id, kwargs)

**Set an estimate for a given story id.**

    tracker.set_story_estimate(story_id, estimate)

**Set a state for a given story id.**

    tracker.set_story_state(story_id, state)

**Return the URL for a given story id**

    tracker.link_story(story_id)

## ConfigBox
Our python-tools often spread across multiple tools that we use at once. A daily cron script will check GitHub and Unity Cloud Build to determine if a new daily build should be published. Our slackbot may need to reference a different GitHub repository based on the channel it receives a message.

ConfigBox is a combo tool/library created to allow a readable reference to the type of information that is being included in code, while easily allowing individual or multiple project configurations to be used at runtime. 

### Setup (Manual)
* Create a folder for ConfigBox.
* Add two child folders: **config/** and **template/**

### Setup (Semi-Auto)
The cbox.py in our [python-tools](https://github.com/zapdot/python-tools) provides an easy way to create and manage various configs and variables.

Run the following command in your terminal. Relative paths are resolved.

    $ cbox.py --setup <path>

### Post-Setup
* Set the environment var, CONFIGBOX_PATH to the absolute path you just setup.
* Put some template files in the **template/** folder.

### Template Files
We use two template files, currently:

##### api.json
```
{
    "cloudbuild": "",
    "github": "",
    "pivotal": "",
    "slack": ""
}
```

##### project.json
```
{
    "cloudbuild": {
        "org_id": "",
        "project_id": ""
    },
    "git": {
        "owner": "",
        "repo": ""
    },
    "pivotal": {
        "project_id": ""
    },
    "slack": {
        "channel": ""
    }
}
```

### Creating Configs

When you have a new project, simply duplicate the **template/project.json** to **config/game1.json**. 'game1' would be your key to reference the data within this new JSON file henceforward.

You can do this with the cbox.py script with the following command:

    $ cbox.py game1 --template project

### Getting Variables in Script
Getting these values in script is easy.

At the top of your script, add: `from zaplib.configbox import config`

And anywhere you want to access a file, simply type: `config[project_id].field.field`

For instance: `print config['game1'].cloudbuild.project_id` would print out the JSON value stored in `CONFIGBOX_PATH/config/game1.json`.

### Tip!
We store the project-based JSONs in a private repository for the company, and share that out with the team on a need-to-know basis.

## GameVersion

coming soon.


