# A base file for use in fabfiles.  
# This file is geared toward a particular directory structure on webfaction and in dev
# Some of it may be useful to other folks, but no guarantees.
# Local Structure
# /
# /db (sqllite for dev and dumps)
# /media
# /appname
# /source (psds and the like)

# Remote Structure (webfaction-based)
# ~/webapps/appname_django
# ~/webapps/appname_django/appname.git   (live version)
# ~/webapps/appname_django/appname  (symlinked -> # ~/webapps/appname_django/appname/appname)
# ~/webapps/appname_django/appname.wsgi
# ~/webapps/appname_media/  (symlinked* -> # ~/webapps/appname_django/appname/media/*)


# Usage
# Generally, 
# from fabbase import *
# then override the Custom Config params with your own.

# Custom Config Start
env.project_name = ''
env.virtualenv_name = ""
env.parent = "origin"
env.working_branch = "master"
env.live_branch = "live"
env.python = "python"
env.work_on = "workon %(project_name)s; " % env
env.set_path = ""
env.is_local = False
env.local_working_path = "~/workingCopy"

# remote config, for webfaction
env.production_hosts = ['']
env.staging_hosts = ['']
env.remote_app_dir = ""
env.remote_live_dir = ""
# Custom Config End

def production():
    env.hosts = env.production_hosts
    env.base_path = "~/webapps/%(remote_app_dir)s" % env
    env.git_path = "%(base_path)s/%(remote_live_dir)s" % env
    env.backup_file_path = "%(git_path)s/db/full_backup.json" % env
    env.pull_branch = env.live_branch
    env.python = "python2.6"
    env.set_path = "PYTHONPATH=~/.virtualenvs/%(virtualenv_name)s/lib/python2.6/;" % env
    
def staging():
    production()
    env.hosts = env.staging_hosts

def local():
    env.hosts = ['localhost']
    env.base_path = "%(local_working_path)s/%(project_name)s" % env
    env.git_path = env.base_path
    env.backup_file_path = "%(git_path)s/db/full_backup.json" % env
    env.pull_branch = env.working_branch
    env.is_local = True

def magic_run(function_call):
    print function_call
    if env.is_local:
        return fabric.operations.local(function_call)
    else:
        return run(function_call)

def pull():
    "Updates the repository."
    magic_run("%(set_path)scd %(git_path)s; git pull %(parent)s %(pull_branch)s" % env)

def git_reset(hash=""):
    env.hash = hash
    "Resets the repository to specified version."
    magic_run("%(set_path)scd %(git_path); git reset --hard %(hash)s" % env)

def ls():
    "Resets the repository to specified version."
    print(magic_run("cd %(base_path)s; ls" % env))

def restart():
    return reboot()
    
def reboot():
    "Reboot the wsgi server."
    magic_run("%(base_path)s/apache2/bin/stop;" % env)
    magic_run("%(base_path)s/apache2/bin/start;" % env)
    
def stop():
    "Stop the wsgi server."
    magic_run("%(base_path)s/apache2/bin/stop;" % env)

def install_requirements():
    "Install the requirements."
    magic_run("%(set_path)s%(work_on)s cd %(git_path)s; pip install -r requirements.txt " % env)

def start():
    "Start the wsgi server."
    magic_run("%(base_path)s/apache2/bin/start;" % env)

def backup():
    "Backup with a data dump."
    magic_run("%(set_path)s%(work_on)s cd %(git_path)s/%(project_name)s; %(python)s manage.py dumpdata --exclude=auth --exclude=contenttypes --indent 4 > %(backup_file_path)s" % env)


def deploy():
    backup()
    pull()
    install_requirements()
    reboot()

def test():
    local("cd %(base_path)s; python manage.py test" % env, fail='abort')

def reset(repo, hash):
    """
    Reset all git repositories to specified hash.
    Usage:
        fab reset:repo=my_repo,hash=etcetc123
    """
    require("fab_hosts", provided_by=[production])
    env.hash = hash
    env.repo = repo
    invoke(git_reset)
    
