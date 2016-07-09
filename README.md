# zaplib

You were eaten by a Grue.

## Installation



## Prereqs

# Siesta


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


