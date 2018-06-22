import os
from functools import partial
from pluginbase import PluginBase

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

plugin_base = PluginBase(package='flaskr.plugins')
plugin_source = plugin_base.make_plugin_source(
        searchpath=[get_path('../plugins')])

print("Plugins installed:")
for p in plugin_source.list_plugins():
    print(" - {}".format(p))


def plugin_list():
    return plugin_source.list_plugins()


def get_plugin(p):
    return plugin_source.load_plugin(p)

def get_plugin_name(p):
    return get_plugin(p).display_name
