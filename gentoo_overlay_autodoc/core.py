from colorama import init
from argparse import ArgumentParser, RawTextHelpFormatter
from gentoo_overlay_autodoc.libmanagers import ObjectManager
from gentoo_overlay_autodoc.version import __version__, _,  epilog, description
from os import sep, path, walk



class Filename:
    def __init__(self, filename):
        self.filename=filename

    def __repr__(self):
        return("FWD: {}".format(self.filename))

class TwoSubdirsManager(ObjectManager):
    def __init__(self, directory):
        ObjectManager.__init__(self)
        self.directory=directory
            
        for currentpath, folders, files in walk(self.directory):
            for file in files:
                path_=path.abspath(currentpath + sep + file)
                if path_.endswith(".ebuild"):
                    self.append_distinct(path.dirname(path_).replace(self.directory, ""))
                    
        self.order_by_name()


    def order_by_name(self):       
        self.arr=sorted(self.arr, key=lambda e: e,  reverse=False) 

## gentoo_overlay_autodoc main script
## If arguments is None, launches with sys.argc parameters. Entry point is gentoo_overlay_autodoc:main
## You can call with main(['--pretend']). It's equivalento to os.system('gentoo_overlay_autodoc --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    parser=ArgumentParser(prog='gentoo_overlay_autodoc', description=description(), epilog=epilog(),  formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--directory', help=_("Overlay main directory"), action="store", required=True)
    parser.add_argument('--format', help=_("Remove example directories'"), action="store", choices=["markdown", ], default="markdown")
    args=parser.parse_args(arguments)
    init(autoreset=True)
#    manager=FilenameManager(args.directory)
    
    twodirs=TwoSubdirsManager(args.directory)
    
    
    s="""# How to install this repository

## 1. Add an entry to [/etc/portage/repos.conf](https://wiki.gentoo.org/wiki//etc/portage/repos.conf)

```
[myportage]
location = /usr/local/overlays/myportage
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ set this to any location you want
sync-uri = https://github.com/turulomio/myportage.git
sync-type = git
auto-sync = yes
```

## 2. Sync overlay
Ejecute this command in console 

```emerge --sync myportage```



<style>
.verticalcenter {
    display: table-cell;
    height: 400px;
    vertical-align: middle;
}
</style>


"""

    s=s + _("# List of ebuilds") + "\n"
    for o in twodirs:
        s=s + '## <div class="verticalcenter"><img src="https://raw.githubusercontent.com/turulomio/gentoo_overlay_autodoc/master/gentoo_overlay_autodoc/images/directory.png" alt="centered image" width="5%" />'+o+'</div>\n\n'
    
    
    print(s)
    with open(args.directory +  sep + "README.md", "w") as f:
        f.write(s)
        
