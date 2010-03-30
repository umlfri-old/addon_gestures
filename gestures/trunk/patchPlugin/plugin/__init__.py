from __future__ import absolute_import

def Plugin(apptype, appref):
    if apptype == 'gtk+':
        from .gtk import CPatchPlugin
    
    return CPatchPlugin(appref)
