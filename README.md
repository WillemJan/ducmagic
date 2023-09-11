# Ducmagic
# Dude, what are these bytes

About
=====
This is a wrapper for [Duc](https://github.com/zevv/duc/).

The wrapper uses the Duc for indexing files in directories and adds [magic](https://linux.die.net/man/5/magic) info to all entries in the Duc database. This can be used to quickly identify filetypes on your filesystem.

Usage
====

```
git clone https://github.com/WillemJan/ducmagic/
pip install .
rm ~/.duc_magic.db; ducmagic index . ; ducmagic ls .
```

Sample output:

(Type, Fname, Size)

```
[2023-09-11 11:45:53,907] {ducmagic.py:194} DEBUG - No ducmagic db found at /home/aloha/.duc_magic.db
[2023-09-11 11:45:53,927] {ducmagic.py:214} DEBUG - Trying to write out ducmagic db at /home/aloha/.duc_magic.db
[2023-09-11 11:45:53,983] {ducmagic.py:158} DEBUG - Trying to read /home/aloha/.duc_magic.db..
{'Dir': [('./.git/hooks', 23442),
         ('./.git/refs/remotes', 30),
         ('./ducmagic/__pycache__', 4174),
         ('./.git', 47279),
         ('./.git/logs/refs/remotes/origin', 191),
         ('./build', 4540),
         ('./.git/logs/refs/heads', 191),
         ('./.git/info', 240),
         ('./.git/refs/heads', 41),
         ('./.git/logs/refs', 382),
         ('./.git/objects/pack', 21910),
         ('./.git/refs', 71),
         ('./ducmagic.egg-info', 41747),
         ('./ducmagic', 8714),
         ('./.git/objects', 21910),
         ('./.git/logs/refs/remotes', 191),
         ('./.git/logs', 573),
         ('./.git/refs/remotes/origin', 30),
         ('./build/lib', 4540),
         ('./build/lib/ducmagic', 4540)],
 'application/octet-stream': [('./.git/index', 578),
                              ('./ducmagic/__pycache__/ducmagic.cpython-310.pyc',
                               4038),
                              ('./.git/objects/pack/pack-8857c21622dca217be99a867f378a9d9c7c1ef0d.idx',
                               1828),
                              ('./ducmagic/__pycache__/__init__.cpython-310.pyc',
                               136)],
 'application/x-git': [('./.git/objects/pack/pack-8857c21622dca217be99a867f378a9d9c7c1ef0d.pack',
                        20082)],
 'text/plain': [('./.git/refs/remotes/origin/HEAD', 30),
                ('./LICENSE', 35149),
                ('./ducmagic.egg-info/SOURCES.txt', 268),
                ('./README.md', 336),
                ('./pyproject.toml', 695),
                ('./ducmagic.egg-info/PKG-INFO', 41411),
                ('./.git/description', 73),
                ('./ducmagic.egg-info/entry_points.txt', 51),
                ('./.git/refs/heads/main', 41),
                ('./.git/logs/HEAD', 191),
                ('./.gitignore', 3078),
                ('./.git/packed-refs', 112),
                ('./.git/config', 259),
                ('./.git/info/exclude', 240),
                ('./.git/logs/refs/heads/main', 191)],
 'text/x-perl': [('./.git/hooks/fsmonitor-watchman.sample', 4655)],
 'text/x-script.python': [('./ducmagic/ducmagic.py', 4540),
                          ('./build/lib/ducmagic/ducmagic.py', 4540)],
 'text/x-shellscript': [('./.git/hooks/prepare-commit-msg.sample', 1492),
                        ('./.git/hooks/post-update.sample', 189),
                        ('./.git/hooks/push-to-checkout.sample', 2783),
                        ('./.git/hooks/pre-applypatch.sample', 424),
                        ('./.git/hooks/pre-push.sample', 1374),
                        ('./.git/hooks/pre-merge-commit.sample', 416),
                        ('./.git/hooks/pre-rebase.sample', 4898),
                        ('./.git/hooks/commit-msg.sample', 896),
                        ('./.git/hooks/pre-commit.sample', 1643),
                        ('./.git/hooks/pre-receive.sample', 544),
                        ('./.git/hooks/applypatch-msg.sample', 478),
                        ('./.git/hooks/update.sample', 3650)]}
```
