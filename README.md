# LowScore

LowScore is a Python command line program which will take a user's post history on the website
[Reddit](http://reddit.com), and will systematically go through the user's history deleting one post/submission at a
time until only those whitelisted remain. It allows you to maintain your normal reddit account while having your history
scrubbed after a certain amount of time.

When it became known that post edits were *not* saved but post deletions *were* saved, code was added to edit your post
prior to deletion. In fact you can actually turn off deletion all together and just have lorem ipsum (or a message
about LowScore) but this will increase how long it takes the script to run as it will be going over all of your messages
every run.

## Important New Changes (as of Dec 2016)

Due to deprecation of the PRAW 3.x library, LowScore is using PRAW 4. This requires that OAuth be used to authenticate.
Thankfully, however, it is much easier than in previous versions. If you are upgrading, [please review the usage section
to ensure that you have set up credentials correctly.](#configuring-credentials)

## Pip Installation

`pip install -U lowScore` will install the package and its dependencies, and it will add a `lowScore` command line
utility to your PATH. This is typically either run in a virtualenv or using administrative privileges for global
installation.

## Manual Installation

1. Clone the `lowScore` repository to a directory.
2. From the directory, run `pip install -r requirements.txt`
3. Run `python setup.py install` to install the package and the `lowScore` command line utility.  This is typically
   either run in a virtualenv or using administrative privileges for global installation.

## Usage

After installing the `lowScore` command line utility, the first step is setting up the tool's configuration files.
Simply typing `lowScore -g` will generate configs. After configuring credentials, running the tool with the `lowScore`
command will begin the tool's operation.

### Configuring Credentials

Running `lowScore -g` will generate a blank praw.ini file that looks like this:

```
# Credentials go here. Fill out default, or provide one or more names and call lowScore with the -u option to specify
# which set to use.
[default]
client_id=
client_secret=
username=
password=
```

**You must provide values for each of these.** As strange as it may seem to provide both a username/password pair *and*
a client id/secret pair, that is how the Reddit API does "OAuth" script applications.

Username and password are simply your Reddit login credentials for the account that will be used. However, to obtain the
client ID and secret, follow these steps (taken from 
[PRAW documentation](http://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application)):

1. Open your Reddit application preferences by clicking [here](https://www.reddit.com/prefs/apps/).
2. Add a new application. It doesn't matter what it's named, but calling it "lowScore" makes it easier to remember.
3. Select "script".
4. Redirect URL does not matter for script applications, so enter something like http://127.0.0.1:8080
5. Once created, you should see the name of your application followed by 14 character string. Enter this 14 character
   string as your `client_id`.
6. Copy the 27 character "secret" string into the `client_secret` field.

Finally, your praw.ini should look like this (with fake data provided here):

```
[default]
client_id=f3FaKeD4t40PsJ
client_secret=dfK3pfMoReFAkEDaTa123456789
username=testuser
password=123passwordgoeshere123
```

Keep your praw.ini either in the current directory when running `lowScore`, or in one of the config folders
[described here](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) such as
`~/.config` in Linux or `%APPDATA%` in Windows.

To use more than one account, you can add multiple profiles instead of just `[default]` and use the `-u` option to 
`lowScore` to choose which one each time.

### Automating

The easiest way to automate this tool after the first run is by using the cron utility. Run `crontab -e` to edit your
user's crontab settings.

**Examples:**

The following examples require that the PRAW configuration file is located in the config directory. See [this PRAW
documentation](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) for more information.

- Run every hour on the hour
        `0 * * * * lowScore -c <full path to lowScore.yml>`

- Run at 3am every morning
        `0 3 * * * lowScore -c <full path to lowScore.yml>`

- Run once a month on the 1st of the month
        `0 0 1 * * lowScore -c <full path to lowScore.yml>`

If virtualenv was used, be sure to add `source /full/path/to/venv/bin/activate &&` before the command. For example:

`0 * * * * source /full/path/to/venv/bin/activate && lowScore -c <full path to lowScore.yml>`

### Command Line Options

```
$ lowScore --help
usage: app.py [-h] [-c CONFIG] [-g] [-u USER]

Command-line frontend to the lowScore library.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use instead of the default lowScore.yml
  -g, --generate-configs
                        Write lowScore and praw config files to current
                        directory.
  -u USER, --user USER  User section from praw.ini if not default
```

## For Windows users

1. Make sure you have Python installed.
   [Click here for the Python download page](https://www.python.org/downloads/).
        - **Note:** Install either `python 2.x` or `python 3.x`, not both.
2. Follow the [pip installation](#pip-installation) instructions.
3. Open a new command prompt and verify that the `lowScore` command works before moving on to the [usage](#usage)
   section.

## Caveats

- Certain limitations in the Reddit API and the PRAW library make it difficult to delete more than 1,000 comments.
  While deleting >1000 comments is planned, it is necessary right now to rerun the program until they are all deleted.

- We are relying on Reddit admin words that they do not store edits, deleted posts are still stored in the database
  they are merely inaccessible to the public.

## Donate

A few people have asked about donating so here's a Bitcoin address, any amount is appreciated, spread amongst recent 
contributors and if there's enough interest a web service may be on the horizon! `1PbeYK7FonjVmgWxf4ieKmvwtomZR1K1Qu`
