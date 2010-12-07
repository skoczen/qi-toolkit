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
# ~/webapps/appname_live
# ~/webapps/appname_live/appname.git   (live version)
# ~/webapps/appname_live/appname  (symlinked -> # ~/webapps/appname_django/appname/appname)
# ~/webapps/appname_live/appname.wsgi
# ~/webapps/appname_static/  (symlinked* -> # ~/webapps/appname_django/appname/media/*)


# Usage
# Basic:
# from qi_toolkit.fabbase import *
# setup_env(project_name='projname',webfaction_user='username')

# Advanced
# from qi_toolkit.fabbase import *
# initial_settings = {
#   'media_dir':'static',
# }
# overrides = {
#   'workon': 'echo "no work today"',
# }
# setup_env(project_name='projname',webfaction_user='username', initial_settings=initial_settings, overrides=overrides)


from __future__ import with_statement # needed for python 2.5
from fabric.api import *

def setup_env_webfaction(project_name, webfaction_user, initial_settings={}, overrides={}):
    global env
    env.dry_run = False
    env.project_name = project_name
    env.webfaction_user = webfaction_user

    # Custom Config Start
    env.parent = "origin"
    env.working_branch = "master"
    env.live_branch = "live"
    env.python = "python"
    env.is_local = False
    env.local_working_path = "~/workingCopy"
    env.media_dir = "media"
    env.webfaction_host = '%(webfaction_user)s.webfactional.com' % env

    env.update(initial_settings)
    
    # semi-automated.  Override this for more complex, multi-server setups, or non-wf installs.
    env.production_hosts = ['%(webfaction_host)s' % env] 
    env.webfaction_home = "/home/%(webfaction_user)s" % env
    env.git_origin = "%(webfaction_user)s@%(webfaction_host)s:%(webfaction_home)s/git-root/%(project_name)s.git" % env

    env.staging_hosts = env.production_hosts
    env.virtualenv_name = env.project_name
    env.staging_virtualenv_name = "staging_%(project_name)s" % env
    env.live_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_live" % env
    env.live_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_static" % env
    env.staging_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging" % env
    env.staging_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging_static" % env
    env.virtualenv_path = "%(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env
    env.work_on = "workon %(virtualenv_name)s; " % env

    env.update(overrides)

def setup_env_rackspace(project_name, webfaction_user, initial_settings={}, overrides={}):
    raise "Not Yet Implemented"
    global env
    env.dry_run = False    
    env.project_name = project_name
    env.webfaction_user = webfaction_user

    # Custom Config Start
    env.parent = "origin"
    env.working_branch = "master"
    env.live_branch = "live"
    env.python = "python"
    env.is_local = False
    env.local_working_path = "~/workingCopy"
    env.media_dir = "media"

    env.update(initial_settings)

    # semi-automated.  Override this for more complex, multi-server setups, or non-wf installs.
    env.production_hosts = ['%(webfaction_user)s.webfactional.com' % env] 
    env.webfaction_home = "/home/%(webfaction_user)s" % env
    env.git_origin = "%(webfaction_user)s@%(webfaction_user)s.webfactional.com:%(webfaction_home)s/git-root/%(project_name)s.git" % env

    env.staging_hosts = env.production_hosts
    env.virtualenv_name = env.project_name
    env.staging_virtualenv_name = "staging_%(project_name)s" % env
    env.live_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_live" % env
    env.live_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_static" % env
    env.staging_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging" % env
    env.staging_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging_static" % env
    env.virtualenv_path = "%(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env
    env.work_on = "workon %(virtualenv_name)s; " % env

    env.update(overrides)

def live():
    env.python = "python2.6"
    env.hosts = env.production_hosts
    env.base_path = env.live_app_dir
    env.git_path = "%(live_app_dir)s/%(project_name)s.git" % env
    env.backup_file_path = "%(git_path)s/db/full_backup.json" % env
    env.media_path = env.live_static_dir
    env.pull_branch = env.live_branch
    
    
def staging():
    env.python = "python2.6"
    env.hosts = env.staging_hosts
    env.base_path = env.staging_app_dir
    env.git_path = "%(staging_app_dir)s/%(project_name)s.git" % env
    env.media_path = env.staging_static_dir
    env.backup_file_path = "%(git_path)s/db/full_backup.json" % env    
    env.pull_branch = env.live_branch
    env.virtualenv_name = env.staging_virtualenv_name
    env.work_on = "workon %(virtualenv_name)s; " % env

def localhost():
    env.hosts = ['localhost']
    env.base_path = "%(local_working_path)s/%(project_name)s" % env
    env.git_path = env.base_path
    env.backup_file_path = "%(git_path)s/db/full_backup.json" % env
    env.pull_branch = env.working_branch
    env.virtualenv_path = "~/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env    
    env.is_local = True
    env.media_path = "%(base_path)s/%(media_dir)s" % env

env.roledefs = {
    'live': [live],
    'staging': [staging],
    'local':[local]
}

# Custom Config End
def magic_run(function_call):
    if env.dry_run:
        print function_call % env
    else:
        if env.is_local:
            return local(function_call % env)
        else:
            return run(function_call % env)

def setup_server():
    magic_run("mkvirtualenv %(virtualenv_name)s;")
    magic_run("echo 'cd %(git_path)s/' > %(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/bin/postactivate")
    try:
        magic_run ("mkdir %(base_path)s")
    except:
        pass
    magic_run("git clone %(git_origin)s %(git_path)s")
    
    magic_run("%(work_on)s git checkout %(pull_branch)s; git pull")    
    magic_run("cd %(media_path)s; ln -s %(git_path)s/%(media_dir)s/* .")
    install_requirements()
    if not env.is_local:
        try:
            magic_run("rm -rf %(base_path)s/myproject; rm %(base_path)s/myproject.wsgi");
        except:
            pass
        # httpd.conf
        magic_run("mv %(base_path)s/apache2/conf/httpd.conf %(base_path)s/apache2/conf/httpd.conf.bak")
        magic_run("sed 'N;$!P;$!D;$d' %(base_path)s/apache2/conf/httpd.conf.bak > %(base_path)s/apache2/conf/httpd.conf")
        magic_run("echo 'WSGIPythonPath %(base_path)s:%(base_path)s/lib/python2.6:%(virtualenv_path)s' >> %(base_path)s/apache2/conf/httpd.conf")
        magic_run("echo 'WSGIScriptAlias / %(base_path)s/%(project_name)s.wsgi' >> %(base_path)s/apache2/conf/httpd.conf")

        # WSGI file
        magic_run("touch %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo 'import os, sys' > %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo 'from django.core.handlers.wsgi import WSGIHandler' >> %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo \"sys.path = ['%(virtualenv_path)s','%(git_path)s/%(project_name)s','/usr/local/lib/python2.6/site-packages/', '%(git_path)s', '%(virtualenv_path)s../../../src/django-cms'] + sys.path\" >> %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo \"os.environ['DJANGO_SETTINGS_MODULE'] = '%(project_name)s.settings'\" >> %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo 'application = WSGIHandler()' >> %(base_path)s/%(project_name)s.wsgi")

    restart()
    
def make_wsgi_file():
    magic_run("touch %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'import os, sys' > %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'from django.core.handlers.wsgi import WSGIHandler' >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo \"sys.path = ['%(virtualenv_path)s','%(git_path)s/%(project_name)s','/usr/local/lib/python2.6/site-packages/', '%(git_path)s', '%(virtualenv_path)s../../../src/django-cms'] + sys.path\" >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo \"os.environ['DJANGO_SETTINGS_MODULE'] = '%(project_name)s.settings'\" >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'application = WSGIHandler()' >> %(base_path)s/%(project_name)s.wsgi")
    
def setup_django_admin_media_symlinks():
    magic_run("cd %(media_path)s; rm admin; ln -s %(virtualenv_path)sdjango/contrib/admin/media admin")

def setup_cms_symlinks():
    magic_run("cd %(media_path)s; rm cms; ln -s %(virtualenv_path)s../../../src/django-cms/cms/media/cms .")

def pull():
    "Updates the repository."
    magic_run("cd %(git_path)s; git pull %(parent)s %(pull_branch)s")

def git_reset(hash=""):
    env.hash = hash
    "Resets the repository to specified version."
    magic_run("%(work_on); git reset --hard %(hash)s")

def ls():
    "Resets the repository to specified version."
    magic_run("cd %(base_path)s; ls")

def restart():
    return reboot()
    
def reboot():
    "Reboot the wsgi server."
    if not env.is_local:
        magic_run("%(base_path)s/apache2/bin/stop;")
        magic_run("%(base_path)s/apache2/bin/start;")
        
    
def stop():
    "Stop the wsgi server."
    if not env.is_local:    
        magic_run("%(base_path)s/apache2/bin/stop;")

def install_requirements():
    "Install the requirements."
    magic_run("%(work_on)s pip install -r requirements.txt ")

def start():
    "Start the wsgi server."
    magic_run("%(base_path)s/apache2/bin/start;")

def backup():
    "Backup with a data dump."
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --indent 4 > %(backup_file_path)s")
    if env.is_local:
        magic_run("cp %(backup_file_path)s %(git_path)s/db/all_data.json")

def syncdb():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py syncdb --noinput")

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



def ssh_auth_me():
    my_key = local("cat ~/.ssh/id_dsa.pub")
    if my_key == "":
        my_key = local("cat ~/.ssh/id_rsa.pub")        

    sudo("mkdir ~/.ssh; chmod 700 ~/.ssh; touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys;")
    sudo("echo '%s' >> ~/.ssh/authorized_keys" % (my_key))

