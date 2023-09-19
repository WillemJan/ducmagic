# Ducmagic
# Dude, what are these bytes

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

Sample output:

(Type, Fname, Size)

```
./test.sh 
Cloning into 'ducmagic'...
remote: Enumerating objects: 120, done.
remote: Counting objects: 100% (120/120), done.
remote: Compressing objects: 100% (97/97), done.
remote: Total 120 (delta 57), reused 62 (delta 19), pack-reused 0
Receiving objects: 100% (120/120), 44.95 KiB | 708.00 KiB/s, done.
Resolving deltas: 100% (57/57), done.
created virtual environment CPython3.10.12.final.0-64 in 178ms
  creator CPython3Posix(dest=/home/ducmagic/venv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/ducmagic/.local/share/virtualenv)
    added seed packages: pip==23.0, setuptools==67.1.0, wheel==0.38.4
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
Processing /home/ducmagic/ducmagic
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... done
Collecting cmagic
  Downloading cmagic-1.0.3.tar.gz (12 kB)
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: ducmagic, cmagic
  Building wheel for ducmagic (pyproject.toml) ... done
  Created wheel for ducmagic: filename=ducmagic-0.0.1-py3-none-any.whl size=37063 sha256=7b65d66dcc8c46a83dc50cb613b4ae7555fb671f0987d7a64ece1e9bfde57d4d
  Stored in directory: /tmp/user/1163/pip-ephem-wheel-cache-mxqmzg8l/wheels/d1/8a/f5/5c2bf6269d5696d20775142abc61f9ca5c2f223c935d294b41
  Building wheel for cmagic (setup.py) ... done
  Created wheel for cmagic: filename=cmagic-1.0.3-cp310-cp310-linux_x86_64.whl size=27225 sha256=109f2c925ba9a44eea5dd723b70f67375e59c1b72b4376993c80e1398df96a94
  Stored in directory: /home/ducmagic/.cache/pip/wheels/ce/4f/74/f77cf8d4056688d9a1d9e00b3438c46250a6d7e2531beffd68
Successfully built ducmagic cmagic
Installing collected packages: cmagic, ducmagic
Successfully installed cmagic-1.0.3 ducmagic-0.0.1

[notice] A new release of pip is available: 23.0 -> 23.2.1
[notice] To update, run: pip install --upgrade pip
[2023-09-19 19:15:00,398] {ducmagic.py:280} DEBUG - Ducmagic db /home/ducmagic/.duc_magic.db empty.

[2023-09-19 19:15:00,427] {ducmagic.py:374} DEBUG - Trying to write out ducmagic db at /home/ducmagic/.duc_magic.db
[2023-09-19 19:15:00,430] {ducmagic.py:387} DEBUG - Write out ducmagic to /home/ducmagic/.duc_magic.db completed.
[2023-09-19 19:15:00,466] {ducmagic.py:283} DEBUG - Trying to read /home/ducmagic/.duc_magic.db.
{'Dir': [('/home/ducmagic/venv', 10396013),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/pip', 6878788),
         ('/home/ducmagic/ducmagic/.git/logs/refs/remotes', 191),
         ('/home/ducmagic/ducmagic/.git/hooks', 23442),
         ('/home/ducmagic/ducmagic/.git/logs', 573),
         ('/home/ducmagic/ducmagic/.git', 75986),
         ('/home/ducmagic/venv/lib/python3.10', 10381068),
         ('/home/ducmagic/ducmagic/.git/info', 240),
         ('/home/ducmagic/ducmagic/.git/objects/pack', 50457),
         ('/home/ducmagic/.local/share/virtualenv/wheel', 13550375),
         ('/home/ducmagic/.local', 13550375),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/setuptools',
          2691345),
         ('/home/ducmagic/ducmagic/.git/objects', 50457),
         ('/home/ducmagic/ducmagic/ducmagic', 12133),
         ('/home/ducmagic/ducmagic/.git/refs/remotes', 30),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/setuptools-67.1.0.dist-info',
          44287),
         ('/home/ducmagic/.local/share/virtualenv/wheel/3.10', 10375725),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/wheel-0.38.4.dist-info',
          6241),
         ('/home/ducmagic/ducmagic', 152135),
         ('/home/ducmagic/ducmagic/.git/logs/refs/heads', 191),
         ('/home/ducmagic/ducmagic/.git/logs/refs', 382),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/pip-23.0.dist-info',
          77664),
         ('/home/ducmagic/ducmagic/.git/refs/remotes/origin', 30),
         ('/home/ducmagic/ducmagic/.git/refs/heads', 41),
         ('/home/ducmagic/ducmagic/.git/refs', 71),
         ('/home/ducmagic/.local/share/virtualenv', 13550375),
         ('/home/ducmagic/.local/share/virtualenv/wheel/house', 3174650),
         ('/home/ducmagic/venv/lib', 10381068),
         ('/home/ducmagic/venv/bin', 14697),
         ('/home/ducmagic/venv/lib/python3.10/site-packages', 10381068),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/pkg_resources',
          574852),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/wheel', 95910),
         ('/home/ducmagic/venv/lib/python3.10/site-packages/_distutils_hack',
          6172),
         ('/home/ducmagic/.local/share', 13550375)],
 'application/octet-stream': [('/home/ducmagic/ducmagic/.git/index', 738),
                              ('/home/ducmagic/ducmagic/.git/objects/pack/pack-eb4494b6cddc3ef4ebd8a5f998e797478c8cbee0.idx',
                               4432)],
 'application/x-git': [('/home/ducmagic/ducmagic/.git/objects/pack/pack-eb4494b6cddc3ef4ebd8a5f998e797478c8cbee0.pack',
                        46025)],
 'text/plain': [('/home/ducmagic/venv/bin/pip-3.10', 235),
                ('/home/ducmagic/venv/bin/wheel-3.10', 222),
                ('/home/ducmagic/.bash_logout', 220),
                ('/home/ducmagic/ducmagic/.git/refs/heads/main', 41),
                ('/home/ducmagic/venv/bin/activate.fish', 3015),
                ('/home/ducmagic/venv/bin/pip3', 235),
                ('/home/ducmagic/venv/bin/activate', 2138),
                ('/home/ducmagic/venv/bin/activate_this.py', 1176),
                ('/home/ducmagic/ducmagic/.git/packed-refs', 112),
                ('/home/ducmagic/venv/bin/pip3.10', 235),
                ('/home/ducmagic/ducmagic/.git/description', 73),
                ('/home/ducmagic/.bashrc', 3771),
                ('/home/ducmagic/venv/lib/python3.10/site-packages/distutils-precedence.pth',
                 151),
                ('/home/ducmagic/ducmagic/.git/info/exclude', 240),
                ('/home/ducmagic/venv/lib/python3.10/site-packages/_virtualenv.py',
                 5640),
                ('/home/ducmagic/.duc.db', 266752),
                ('/home/ducmagic/ducmagic/.git/config', 259),
                ('/home/ducmagic/venv/bin/activate.ps1', 1754),
                ('/home/ducmagic/venv/bin/activate.nu', 3328),
                ('/home/ducmagic/venv/bin/activate.csh', 1430),
                ('/home/ducmagic/ducmagic/pyproject.toml', 686),
                ('/home/ducmagic/ducmagic/LICENSE', 35149),
                ('/home/ducmagic/ducmagic/README.md', 24746),
                ('/home/ducmagic/ducmagic/ducmagic/helper.py', 2173),
                ('/home/ducmagic/venv/bin/wheel3.10', 222),
                ('/home/ducmagic/.profile', 807),
                ('/home/ducmagic/venv/bin/wheel', 222),
                ('/home/ducmagic/ducmagic/.git/logs/HEAD', 191),
                ('/home/ducmagic/venv/bin/wheel3', 222),
                ('/home/ducmagic/ducmagic/.gitignore', 3084),
                ('/home/ducmagic/venv/bin/pip', 235),
                ('/home/ducmagic/venv/pyvenv.cfg', 208),
                ('/home/ducmagic/venv/.gitignore', 40)],
 'text/x-perl': [('/home/ducmagic/ducmagic/.git/hooks/fsmonitor-watchman.sample',
                  4655)],
 'text/x-script.python': [('/home/ducmagic/ducmagic/ducmagic/ducmagic.py',
                           9936)],
 'text/x-shellscript': [('/home/ducmagic/ducmagic/.git/hooks/push-to-checkout.sample',
                         2783),
                        ('/home/ducmagic/ducmagic/.git/hooks/update.sample',
                         3650),
                        ('/home/ducmagic/ducmagic/test.sh', 351),
                        ('/home/ducmagic/ducmagic/.git/hooks/applypatch-msg.sample',
                         478),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-commit.sample',
                         1643),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-push.sample',
                         1374),
                        ('/home/ducmagic/ducmagic/.git/hooks/prepare-commit-msg.sample',
                         1492),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-applypatch.sample',
                         424),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-merge-commit.sample',
                         416),
                        ('/home/ducmagic/ducmagic/.git/hooks/commit-msg.sample',
                         896),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-receive.sample',
                         544),
                        ('/home/ducmagic/ducmagic/.git/hooks/post-update.sample',
                         189),
                        ('/home/ducmagic/test.sh', 279),
                        ('/home/ducmagic/ducmagic/.git/hooks/pre-rebase.sample',
                         4898)]}
```
