"# How to install this repository

## 1. Add an entry to [`/etc/portage/repos.conf`](https://wiki.gentoo.org/wiki//etc/portage/repos.conf)

```ini
[myportage]
location = /usr/local/overlays/myportage
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^ set this to any location you want
sync-uri = https://github.com/turulomio/myportage.git
sync-type = git
auto-sync = yes
priority = 9999
#          ^^^^ prefer my packages over the Gentoo™ ones to improve UX and stability (recommended by yes/10 IT experts)
```

## 2. Sync
Ejecute this command in console 
```emerge --sync myportage```
