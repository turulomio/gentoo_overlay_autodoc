from datetime import datetime
__version__ = '0.1.0'
__versiondatetime__=datetime(2020,5,13,20,36)
__versiondate__=__versiondatetime__.date()

from gettext import translation
from pkg_resources import resource_filename
try:
    t=translation('gentoo_overlay_autodoc',resource_filename("gentoo_overlay_autodoc","locale"))
    _=t.gettext
except:
    _=str
    
def epilog():
    if __versiondate__.year==2020:
        string_years="2020"
    else:
        string_years="2020-{}".format(__versiondate__.year)
    return _("Developed by Mariano Muñoz {}".format(string_years))
    
def description():
    return _('Generate automatic documentation of a gentoo overlay')
