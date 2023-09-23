# Ducmagic
# Dude, what are these bytes


![Linter](https://github.com/willemjan/ducmagic/workflows/pylint.yml/badge.svg)]
![Tests](https://github.com/willemjan/ducmagic/workflows/python-app.yml/badge.svg)]


About
=====
This is a wrapper for [Duc](https://github.com/zevv/duc/).

The wrapper uses the Duc for indexing files in directories and adds [magic](https://linux.die.net/man/5/magic) info to all entries in the Duc database. This can be used to quickly identify filetypes on your filesystem.

Usage
====

```
#sudo apt install -y duc python3-pip python3-virtualenv

cd ~
virtualenv venv
source venv/bin/activate
git clone https://github.com/WillemJan/ducmagic/
cd ducmagic
pip install .

duc index .
ducmagic index .
ducmagic ls .
```

Output test.sh


```
+ git clone https://github.com/WillemJan/ducmagic/
Cloning into 'ducmagic'...
+ virtualenv venv
created virtual environment CPython3.11.2.final.0-64 in 255ms
  creator CPython3Posix(dest=/home/ducmagic/venv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/ducmagic/.local/share/virtualenv)
    added seed packages: pip==23.0.1, setuptools==66.1.1, wheel==0.38.4
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
+ source venv/bin/activate
++ '[' venv/bin/activate = test.sh ']'
++ deactivate nondestructive
++ unset -f pydoc
++ '[' -z '' ']'
++ '[' -z '' ']'
++ hash -r
++ '[' -z '' ']'
++ unset VIRTUAL_ENV
++ '[' '!' nondestructive = nondestructive ']'
++ VIRTUAL_ENV=/home/ducmagic/venv
++ '[' linux-gnu = cygwin ']'
++ '[' linux-gnu = msys ']'
++ export VIRTUAL_ENV
++ _OLD_VIRTUAL_PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
++ PATH=/home/ducmagic/venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
++ export PATH
++ '[' -z '' ']'
++ '[' -z '' ']'
++ _OLD_VIRTUAL_PS1=
++ '[' x '!=' x ']'
+++ basename /home/ducmagic/venv
++ PS1='(venv) '
++ export PS1
++ alias pydoc
++ true
++ hash -r
+ cd ducmagic
+ pip install .
Processing /home/ducmagic/ducmagic
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting cmagic
  Using cached cmagic-1.0.3-cp311-cp311-linux_x86_64.whl
Building wheels for collected packages: ducmagic
  Building wheel for ducmagic (pyproject.toml): started
  Building wheel for ducmagic (pyproject.toml): finished with status 'done'
  Created wheel for ducmagic: filename=ducmagic-0.0.1-py3-none-any.whl size=34187 sha256=0c5882899042437750cefda31b766a24541654af4f4d7fd21d038de084634f90
  Stored in directory: /tmp/pip-ephem-wheel-cache-utc_qefu/wheels/e0/c0/25/acc6b57b86b8883652309e6b02f617d5cd4e2be3b49c0bfd3e
Successfully built ducmagic
Installing collected packages: cmagic, ducmagic
Successfully installed cmagic-1.0.3 ducmagic-0.0.1
+ cd ..
+ duc index .
+ ducmagic index .
/home/ducmagic/.duc.db
[2023-09-21 09:10:03,338] {ducmagic.py:164} DEBUG - Ducmagic db /home/ducmagic/.duc_magic.db empty.

[2023-09-21 09:10:03,412] {ducmagic.py:415} DEBUG - Trying to write out ducmagic db at /home/ducmagic/.duc_magic.db
[2023-09-21 09:10:03,418] {ducmagic.py:429} DEBUG - Write out ducmagic to /home/ducmagic/.duc_magic.db completed.
+ ducmagic ls
/home/ducmagic/.duc.db
{'Dir': [('/home/ducmagic/ducmagic/.git/refs/heads', 0),
         ('/home/ducmagic/.cache/pip/http', 0),
         ('/home/ducmagic/venv', 0),
         ('/home/ducmagic/ducmagic/.git/info', 0),
         ('/home/ducmagic/.cache/pip/http/7', 0),
         ('/home/ducmagic/.local/share/virtualenv', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/cmagic-1.0.3.dist-info',
          0),
         ('/home/ducmagic/.local', 0),
         ('/home/ducmagic/.cache/pip/http/7/b', 0),
         ('/home/ducmagic/ducmagic/ducmagic', 0),
         ('/home/ducmagic/.cache/pip/http/d', 0),
         ('/home/ducmagic/.cache/pip/http/9', 0),
         ('/home/ducmagic/ducmagic/.git', 0),
         ('/home/ducmagic/.cache/pip/http/f', 0),
         ('/home/ducmagic/.cache/pip/http/9/e', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/ducmagic-0.0.1.dist-info',
          0),
         ('/home/ducmagic/.cache/pip', 0),
         ('/home/ducmagic/.cache/pip/http/4', 0),
         ('/home/ducmagic/ducmagic/.git/logs/refs/remotes', 0),
         ('/home/ducmagic/.cache/pip/http/3', 0),
         ('/home/ducmagic/.cache/pip/http/4/4', 0),
         ('/home/ducmagic/.cache', 0),
         ('/home/ducmagic/venv/lib', 0),
         ('/home/ducmagic/.local/share/virtualenv/wheel/3.11', 0),
         ('/home/ducmagic/.cache/pip/wheels/14', 0),
         ('/home/ducmagic/.cache/pip/wheels', 0),
         ('/home/ducmagic/.cache/pip/http/f/3', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/setuptools', 0),
         ('/home/ducmagic/.cache/pip/http/7/8', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/_distutils_hack',
          0),
         ('/home/ducmagic/venv/lib/python3.11', 0),
         ('/home/ducmagic/.cache/pip/http/d/5', 0),
         ('/home/ducmagic/.cache/pip/http/b', 0),
         ('/home/ducmagic/ducmagic/.git/logs', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/ducmagic', 0),
         ('/home/ducmagic/.cache/pip/http/3/3', 0),
         ('/home/ducmagic/.cache/pip/http/6/2', 0),
         ('/home/ducmagic/.cache/pip/wheels/14/01', 0),
         ('/home/ducmagic/.local/share/virtualenv/wheel', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/cmagic', 0),
         ('/home/ducmagic/.cache/pip/http/c/c', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/setuptools-66.1.1.dist-info',
          0),
         ('/home/ducmagic/.local/share', 0),
         ('/home/ducmagic/ducmagic', 0),
         ('/home/ducmagic/.cache/pip/http/e', 0),
         ('/home/ducmagic/.cache/pip/http/e/7', 0),
         ('/home/ducmagic/.cache/pip/http/0/6', 0),
         ('/home/ducmagic/.cache/pip/http/9/a', 0),
         ('/home/ducmagic/.cache/pip/http/0', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages', 0),
         ('/home/ducmagic/.cache/pip/http/1/c', 0),
         ('/home/ducmagic/.cache/pip/http/b/7', 0),
         ('/home/ducmagic/.cache/pip/http/6', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/pip-23.0.1.dist-info',
          0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/wheel', 0),
         ('/home/ducmagic/ducmagic/.git/refs', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/pip', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/__pycache__', 0),
         ('/home/ducmagic/.cache/pip/http/5/4', 0),
         ('/home/ducmagic/ducmagic/.git/logs/refs', 0),
         ('/home/ducmagic/ducmagic/.git/hooks', 0),
         ('/home/ducmagic/venv/bin', 0),
         ('/home/ducmagic/ducmagic/.git/refs/remotes/origin', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/pkg_resources', 0),
         ('/home/ducmagic/.cache/pip/http/1', 0),
         ('/home/ducmagic/ducmagic/.git/objects/pack', 0),
         ('/home/ducmagic/venv/lib/python3.11/site-packages/wheel-0.38.4.dist-info',
          0),
         ('/home/ducmagic/ducmagic/.git/objects', 0),
         ('/home/ducmagic/ducmagic/.git/logs/refs/heads', 0),
         ('/home/ducmagic/.cache/pip/http/e/4', 0),
         ('/home/ducmagic/.cache/pip/http/c', 0),
         ('/home/ducmagic/.cache/pip/http/5', 0),
         ('/home/ducmagic/ducmagic/.git/refs/remotes', 0)],
 'application/octet-stream': [('/home/ducmagic/ducmagic/.git/index', 738),
                              ('/home/ducmagic/ducmagic/.git/objects/pack/pack-fb7117e83ec764b2f5d621169e00b53f799b508d.idx',
                               5412)],
 'application/x-git': [('/home/ducmagic/ducmagic/.git/objects/pack/pack-fb7117e83ec764b2f5d621169e00b53f799b508d.pack',
                        53819)],
 'text/plain': [('/home/ducmagic/ducmagic/.git/logs/HEAD', 192),
                ('/home/ducmagic/venv/bin/activate', 2138),
                ('/home/ducmagic/venv/bin/activate.csh', 1430),
                ('/home/ducmagic/venv/bin/pip-3.11', 235),
                ('/home/ducmagic/ducmagic/.git/packed-refs', 112),
                ('/home/ducmagic/test.sh', 203),
                ('/home/ducmagic/.duc.db', 266752),
                ('/home/ducmagic/out.log', 2376),
                ('/home/ducmagic/ducmagic/.git/refs/heads/main', 41),
                ('/home/ducmagic/venv/bin/pip', 235),
                ('/home/ducmagic/ducmagic/.git/description', 73),
                ('/home/ducmagic/.bashrc', 3526),
                ('/home/ducmagic/.viminfo', 8397),
                ('/home/ducmagic/venv/bin/activate.fish', 3015),
                ('/home/ducmagic/venv/bin/wheel-3.11', 222),
                ('/home/ducmagic/venv/bin/ducmagic', 219),
                ('/home/ducmagic/venv/bin/wheel', 222),
                ('/home/ducmagic/venv/bin/activate_this.py', 1176),
                ('/home/ducmagic/ducmagic/LICENSE', 35149),
                ('/home/ducmagic/venv/bin/wheel3', 222),
                ('/home/ducmagic/.bash_logout', 220),
                ('/home/ducmagic/venv/bin/pip3.11', 235),
                ('/home/ducmagic/ducmagic/.git/config', 259),
                ('/home/ducmagic/venv/bin/pip3', 235),
                ('/home/ducmagic/.profile', 807),
                ('/home/ducmagic/venv/bin/wheel3.11', 222),
                ('/home/ducmagic/ducmagic/.gitignore', 3084),
                ('/home/ducmagic/venv/bin/activate.ps1', 1754),
                ('/home/ducmagic/venv/pyvenv.cfg', 210),
                ('/home/ducmagic/ducmagic/ducmagic/helper.py', 2213),
                ('/home/ducmagic/ducmagic/.git/info/exclude', 240),
                ('/home/ducmagic/ducmagic/pyproject.toml', 756),
                ('/home/ducmagic/venv/lib/python3.11/site-packages/distutils-precedence.pth',
                 151),
                ('/home/ducmagic/venv/lib/python3.11/site-packages/_virtualenv.py',
                 5640),
                ('/home/ducmagic/venv/.gitignore', 40),
                ('/home/ducmagic/ducmagic/README.md', 9634),
                ('/home/ducmagic/venv/bin/activate.nu', 3326)],
 'text/x-perl': [('/home/ducmagic/ducmagic/.git/hooks/fsmonitor-watchman.sample',
                  4726)],
 'text/x-script.python': [('/home/ducmagic/ducmagic/ducmagic/ducmagic.py',
                           12758)],
 'text/x-shellscript': [('/home/ducmagic/ducmagic/.git/hooks/pre-applypatch.sample',
                         424),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-commit.sample',
                         1643),
                        ('/home/ducmagic/ducmagic/.git/hooks/update.sample',
                         3650),
                        ('/home/ducmagic/ducmagic/test.sh', 279),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-push.sample',
                         1374),
                        ('/home/ducmagic/ducmagic/.git/hooks/commit-msg.sample',
                         896),
                        ('/home/ducmagic/ducmagic/.git/hooks/prepare-commit-msg.sample',
                         1492),
                        ('/home/ducmagic/ducmagic/.git/hooks/applypatch-msg.sample',
                         478),
                        ('/home/ducmagic/ducmagic/.git/hooks/push-to-checkout.sample',
                         2783),
                        ('/home/ducmagic/ducmagic/.git/hooks/post-update.sample',
                         189),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-receive.sample',
                         544),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-merge-commit.sample',
                         416),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-rebase.sample',
                         4898)],
 'text/xml': [('/home/ducmagic/.face', 5290)]}
+ python ducmagic/ducmagic/ducmagic.py
Trying:
    duc_out="Date       Time       Files    Dirs    Size Path\n"
Expecting nothing
ok
Trying:
    duc_out+="2023-09-21 08:24:12     199     134    1.5M "
Expecting nothing
ok
Trying:
    duc_out+="/home/aloha/code/ducmagic"
Expecting nothing
ok
Trying:
    res = do_duc_info(duc_out)
Expecting nothing
ok
Trying:
    res[0][-1]
Expecting:
    '/home/aloha/code/ducmagic'
ok
Trying:
    len(get_duc_info()) >= 0
Expecting:
    True
ok
Trying:
    len(get_duc_path('.')) > 0
Expecting:
    True
ok
Trying:
    f = [f for f in os.listdir('.') if os.path.isfile(f)]
Expecting nothing
ok
Trying:
    len(get_file_type(f)) > 0
Expecting:
    True
ok
11 items had no tests:
    __main__
    __main__.cli
    __main__.do_index
    __main__.do_info
    __main__.do_is_sane
    __main__.do_ls
    __main__.do_ls_filter
    __main__.do_sync
    __main__.get_file_types
    __main__.load_ducmagic
    __main__.remove_small_files
4 items passed all tests:
   5 tests in __main__.do_duc_info
   1 tests in __main__.get_duc_info
   1 tests in __main__.get_duc_path
   2 tests in __main__.get_file_type
9 tests in 15 items.
9 passed and 0 failed.
Test passed.

real	0m5,906s
user	0m4,350s
sys	0m0,751s

```
