from setuptools import setup, Command
import gettext
import os
import platform
import site


gettext.install('gentoo_overlay_autodoc', 'gentoo_overlay_autodoc/locale')


class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/gentoo_overlay_autodoc/ --delete-after")
        os.chdir("..")

class Procedure(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(_("New Release:"))
        print(_("  * Change version and date in version.py"))
        print(_("  * Edit Changelog in README"))
        print("  * python setup.py doc")
        print("  * mcedit locale/es.po")
        print("  * python setup.py doc")
        print("  * python setup.py install")
        print("  * python setup.py doxygen")
        print("  * git commit -a -m 'gentoo_overlay_autodoc-{}'".format(__version__))
        print("  * git push")
        print(_("  * Make a new tag in github"))
        print("  * python setup.py sdist upload -r pypi")
        print("  * python setup.py uninstall")
        print(_("  * Create a new gentoo ebuild with the new version"))
        print(_("  * Upload to portage repository")) 


class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/gentoo_overlay_autodoc*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/gentoo_overlay_autodoc")
        else:
            print(_("Uninstall command only works in Linux"))

class Reusing(Command):
    description = "Update files from reusingcode project"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("gentoo_overlay_autodoc")
        from github import download_from_github
        download_from_github('turulomio','reusingcode','python/decorators.py', 'gentoo_overlay_autodoc')
        download_from_github('turulomio','reusingcode','python/libmanagers.py', 'gentoo_overlay_autodoc')
        download_from_github('turulomio','reusingcode','python/github.py', 'gentoo_overlay_autodoc')
        download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'gentoo_overlay_autodoc')


class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/gentoo_overlay_autodoc.pot *.py gentoo_overlay_autodoc/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/gentoo_overlay_autodoc.pot")
        os.system("msgfmt -cv -o gentoo_overlay_autodoc/locale/es/LC_MESSAGES/gentoo_overlay_autodoc.mo locale/es.po")


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('gentoo_overlay_autodoc/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]

setup(name='gentoo_overlay_autodoc',
    version=__version__,
    description='Admin options to work with the max length of the name of your files',
    long_description="Project web page is in https://github.com/turulomio/gentoo_overlay_autodoc",
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'Topic :: Software Development :: Build Tools',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Programming Language :: Python :: 3',
             ], 
    keywords='remove files datetime patterns',
    url='https://github.com/turulomio/gentoo_overlay_autodoc',
    author='turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['gentoo_overlay_autodoc'],
    entry_points = {'console_scripts': ['gentoo_overlay_autodoc=gentoo_overlay_autodoc.core:main',
                                    ],
                },
    install_requires=['colorama','setuptools'],
    cmdclass={
    'doxygen': Doxygen,
    'doc': Doc,
    'uninstall':Uninstall,
    'procedure': Procedure,
    'reusing': Reusing,
         },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
