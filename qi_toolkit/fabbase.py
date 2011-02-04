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
import fabric
from helpers import print_exception
import time

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
    env.daily_backup_script_name = "daily_backup.sh"
    env.weekly_backup_script_name = "weekly_backup.sh"
    env.monthly_backup_script_name = "monthly_backup.sh"

    env.staging_hosts = env.production_hosts
    env.virtualenv_name = env.project_name
    env.staging_virtualenv_name = "staging_%(project_name)s" % env
    env.live_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_live" % env
    env.live_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_static" % env
    env.staging_app_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging" % env
    env.staging_static_dir = "%(webfaction_home)s/webapps/%(project_name)s_staging_static" % env
    env.virtualenv_path = "%(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env
    env.work_on = "workon %(virtualenv_name)s; " % env
    env.backup_root = "%(webfaction_home)s/backups" % env
    env.offsite_backup_dir = "aglzen@quantumimagery.com:/home/aglzen/%(project_name)s/data/" % env

    env.update(overrides)

def setup_env_rackspace(project_name, webfaction_user, initial_settings={}, overrides={}):
    raise  Exception, "Not Yet Implemented"
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

def setup_backup_env_webfaction():
    env.current_backup_file = "%(backup_dir)s/currentBackup.json" % env
    env.daily_backup_script = daily_backup_script()
    env.weekly_backup_script = weekly_backup_script()
    env.monthly_backup_script = monthly_backup_script()

def live():
    env.python = "python2.6"
    env.role = "live"
    env.hosts = env.production_hosts
    env.base_path = env.live_app_dir
    env.git_path = "%(live_app_dir)s/%(project_name)s.git" % env
    env.backup_dir = "%(webfaction_home)s/backups/%(project_name)s" % env
    env.media_path = env.live_static_dir
    env.pull_branch = env.live_branch
    setup_backup_env_webfaction()
    
def staging():
    env.python = "python2.6"
    env.role = "staging"
    env.hosts = env.staging_hosts
    env.base_path = env.staging_app_dir
    env.git_path = "%(staging_app_dir)s/%(project_name)s.git" % env
    env.media_path = env.staging_static_dir
    env.backup_dir = "%(webfaction_home)s/backups/staging_%(project_name)s" % env
    env.pull_branch = env.live_branch
    env.virtualenv_name = env.staging_virtualenv_name
    env.virtualenv_path = "%(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env    
    env.work_on = "workon %(virtualenv_name)s; " % env
    setup_backup_env_webfaction()

def localhost():
    env.hosts = ['localhost']
    env.role = "localhost"    
    env.base_path = "%(local_working_path)s/%(project_name)s" % env
    env.git_path = env.base_path
    env.backup_dir = "%(local_working_path)s/db" % env
    env.pull_branch = env.working_branch
    env.virtualenv_path = "~/.virtualenvs/%(virtualenv_name)s/lib/python2.6/site-packages/" % env    
    env.is_local = True
    env.media_path = "%(base_path)s/%(media_dir)s" % env
    setup_backup_env_webfaction()

env.roledefs = {
    'live': [live],
    'staging': [staging],
    'local':[local]
}

def safe(function_call, *args, **kwargs):
    try:
        ret = function_call(*args, **kwargs)
        return ret
    except:
        pass

def safe_magic_run(function_call, *args, **kwargs):
    try:
        ret = magic_run(function_call, *args, **kwargs)
        return ret
    except:
        pass    

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
    try:
        safe_magic_run("mkdir %(webfaction_home)s/src")
        magic_run("echo \"alias l='ls -agl'\nalias python=python2.6\nexport WORKON_HOME=$HOME/.virtualenvs\nsource ~/bin/virtualenvwrapper.sh\" >> %(webfaction_home)s/.bashrc")
    except:
        pass

    try:
        magic_run("git --version")
    except:
        env.git_file_version = "1.7.3.3"
        magic_run("cd src;wget http://kernel.org/pub/software/scm/git/git-%(git_file_version)s.tar.bz2")
        magic_run("cd  %(webfaction_home)s/src/; tar fxj git-%(git_file_version)s.tar.bz2;")
        magic_run("cd %(webfaction_home)s/src/git-%(git_file_version)s; ./configure --prefix=%(webfaction_home)s/git/; make; make install;")
        magic_run("echo \"export PATH=$PATH:/%(webfaction_home)s/git/bin/\" >> %(webfaction_home)s/.bashrc")

    try:
        magic_run("pip --version")
    except:
        try:
            safe_magic_run("mkdir %(webfaction_home)s/lib:")
        except:
            pass
        try:
            safe_magic_run("mkdir %(webfaction_home)s/lib/python2.6")
        except:
            pass
        magic_run("easy_install-2.6 pip")

    magic_run("pip install --upgrade pip virtualenv virtualenvwrapper")
    safe_magic_run("mkdir %(webfaction_home)s/.virtualenvs")
    magic_run("mkvirtualenv %(virtualenv_name)s;")
    magic_run("echo 'cd %(git_path)s/' > %(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/bin/postactivate")
    magic_run("echo 'export DJANGO_SETTINGS_MODULE=\"envs.%(role)s\"' >> %(webfaction_home)s/.virtualenvs/%(virtualenv_name)s/bin/postactivate")    

    safe_magic_run("mkdir %(base_path)s")

    magic_run("git clone %(git_origin)s %(git_path)s")

    magic_run("%(work_on)s git checkout %(pull_branch)s; git pull")    
    setup_media_symlinks()
    setup_project_symlinks()
    setup_backup_dir_and_cron()
    install_requirements()
    if not env.is_local:
        safe_magic_run("rm -rf %(base_path)s/myproject; rm %(base_path)s/myproject.wsgi")

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
        magic_run("echo \"os.environ['DJANGO_SETTINGS_MODULE'] = '%(project_name)s.envs.%(role)s'\" >> %(base_path)s/%(project_name)s.wsgi")
        magic_run("echo 'application = WSGIHandler()' >> %(base_path)s/%(project_name)s.wsgi")

    restart()

def make_wsgi_file():
    magic_run("touch %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'import os, sys' > %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'from django.core.handlers.wsgi import WSGIHandler' >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo \"sys.path = ['%(virtualenv_path)s','%(git_path)s/%(project_name)s','/usr/local/lib/python2.6/site-packages/', '%(git_path)s', '%(virtualenv_path)s../../../src/django-cms'] + sys.path\" >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo \"os.environ['DJANGO_SETTINGS_MODULE'] = '%(project_name)s.settings'\" >> %(base_path)s/%(project_name)s.wsgi")
    magic_run("echo 'application = WSGIHandler()' >> %(base_path)s/%(project_name)s.wsgi")

def setup_media_symlinks():
    safe_magic_run("cd %(media_path)s; ln -s %(git_path)s/%(media_dir)s/* .")

def setup_django_admin_media_symlinks():
    magic_run("cd %(media_path)s; touch admin; rm admin; ln -s %(virtualenv_path)sdjango/contrib/admin/media admin")

def setup_cms_symlinks():
    magic_run("cd %(media_path)s; touch cms; rm cms; ln -s %(virtualenv_path)s../../../src/django-cms/cms/media/cms .")

def setup_project_symlinks():
    pass

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
        shut_down = False
        while not shut_down:
            output = magic_run("%(base_path)s/apache2/bin/stop;")
            shut_down = (output.find("Apache is not running") != -1)
            if not shut_down:
                time.sleep(1)

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

def backup_for_deploy():
    "Backup before deploys."
    import os.path
    env.current_backup_file = "%(backup_dir)s/currentDeployBackup.json" % env    
    if not os.path.isfile(env.current_backup_file):    
        magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --indent 4 > %(current_backup_file)s")
        magic_run("zip -r9q %(backup_dir)s/pre_deploy_`date +%%F`.zip %(current_backup_file)s; rm %(current_backup_file)s")
        if env.is_local:
            magic_run("cp %(current_backup_file)s %(git_path)s/db/all_data.json")
    else:
        raise  Exception, "Deploy backup failed - previous deploy did not finish cleanly."

def setup_backup_dir_and_cron():
    # requires fabric and python-crontab installed on the target
    safe_magic_run("mkdir %(backup_root)s")
    safe_magic_run("mkdir %(backup_dir)s")
    magic_run("echo '%(daily_backup_script)s' > %(backup_dir)s/%(daily_backup_script_name)s")
    magic_run("echo '%(weekly_backup_script)s' > %(backup_dir)s/%(weekly_backup_script_name)s")
    magic_run("echo '%(monthly_backup_script)s' > %(backup_dir)s/%(monthly_backup_script_name)s")
    magic_run("chmod +x %(backup_dir)s/%(daily_backup_script_name)s")
    magic_run("chmod +x %(backup_dir)s/%(weekly_backup_script_name)s")
    magic_run("chmod +x %(backup_dir)s/%(monthly_backup_script_name)s")

    magic_run("%(work_on)s fab %(role)s setup_crontab")

def setup_crontab():
    try:
        from crontab import CronTab
        tab = CronTab()
        daily_command = "%(backup_dir)s/%(daily_backup_script_name)s > /dev/null 2>&1" % env
        weekly_command = "%(backup_dir)s/%(weekly_backup_script_name)s > /dev/null 2>&1" % env
        monthly_command = "%(backup_dir)s/%(monthly_backup_script_name)s > /dev/null 2>&1" % env
        changed = False
        if len(tab.find_command(daily_command)) == 0:
            daily_tab = tab.new(command=daily_command)
            daily_tab.hour().on(1)
            daily_tab.minute().on(0)
            changed = True
        if len(tab.find_command(weekly_command)) == 0:
            weekly_tab = tab.new(command=weekly_command)
            weekly_tab.dow().on(1)
            weekly_tab.hour().on(2)
            weekly_tab.minute().on(0)
            changed = True
        if len(tab.find_command(monthly_command)) == 0:
            monthly_tab = tab.new(command=monthly_command)
            monthly_tab.dom().on(1)
            monthly_tab.hour().on(3)
            monthly_tab.minute().on(0)
            changed = True
        if changed:
            tab.write()
    except:
        print_exception()
        pass


def backup_daily():
    if not fabric.contrib.files.exists(env.current_backup_file):
        magic_run("%(backup_dir)s/%(daily_backup_script_name)s")
    else: 
        raise Exception, "Backup FAILED.  Previous backup did not complete.  Please manually fix the server."


def daily_backup_script():    
    script = """#!/bin/bash
source %(webfaction_home)s/bin/virtualenvwrapper.sh
%(work_on)s cd %(project_name)s; 
%(python)s manage.py dumpdata --indent 4 > %(current_backup_file)s

mv %(backup_dir)s/days-ago-6.zip %(backup_dir)s/days-ago-7.zip
mv %(backup_dir)s/days-ago-5.zip %(backup_dir)s/days-ago-6.zip
mv %(backup_dir)s/days-ago-4.zip %(backup_dir)s/days-ago-5.zip
mv %(backup_dir)s/days-ago-3.zip %(backup_dir)s/days-ago-4.zip
mv %(backup_dir)s/days-ago-2.zip %(backup_dir)s/days-ago-3.zip
mv %(backup_dir)s/days-ago-1.zip %(backup_dir)s/days-ago-2.zip
mv %(backup_dir)s/days-ago-0.zip %(backup_dir)s/days-ago-1.zip
zip -r9q %(backup_dir)s/days-ago-0.zip %(current_backup_file)s 
rm %(current_backup_file)s

cd %(backup_dir)s; mkdir cur_images;
cp -R %(media_path)s/cms %(backup_dir)s/cur_images/
cp -R %(media_path)s/images %(backup_dir)s/cur_images/
cp -R %(media_path)s/goodcloud_people %(backup_dir)s/cur_images/
cd %(backup_dir)s; zip -r9q cur_images2.zip cur_images
cd %(backup_dir)s; rm -rf cur_images
mv %(backup_dir)s/cur_images2.zip %(backup_dir)s/cur_images.zip

scp %(backup_dir)s/cur_images.zip %(offsite_backup_dir)s
""" % env
    # script = script.replace("\n","\\n")
    return script

def backup_weekly():
    magic_run("%(backup_dir)s/%(weekly_backup_script_name)s")

def weekly_backup_script():
    script = """#!/bin/bash
mv %(backup_dir)s/weeks-ago-4.zip %(backup_dir)s/weeks-ago-5.zip
mv %(backup_dir)s/weeks-ago-3.zip %(backup_dir)s/weeks-ago-4.zip
mv %(backup_dir)s/weeks-ago-2.zip %(backup_dir)s/weeks-ago-3.zip
mv %(backup_dir)s/weeks-ago-1.zip %(backup_dir)s/weeks-ago-2.zip
mv %(backup_dir)s/weeks-ago-0.zip %(backup_dir)s/weeks-ago-1.zip
cp %(backup_dir)s/days-ago-0.zip %(backup_dir)s/weeks-ago-0.zip

cd %(backup_dir)s; scp * %(offsite_backup_dir)s
""" % env
    # script = script.replace("\n","\\n")
    return script

def backup_monthly():
    magic_run("%(backup_dir)s/%(monthly_backup_script_name)s")

def monthly_backup_script():
    script = """#!/bin/bash
cp %(backup_dir)s/weeks-ago-0.zip %(backup_dir)s/month-`date +%%F`.zip
""" % env
    # script = script.replace("\n","\\n")
    return script

def kill_pyc():
    magic_run("%(work_on)s cd %(git_path)s;find  -iname '*.pyc' -delete")

def migrate():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py migrate")

def syncdb():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py syncdb --noinput")

def deploy():
    backup_for_deploy()
    pull()
    install_requirements()
    migrate()
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
