from .stretch_plugin_action import StretchPluginAction # Note the relative import!

StretchPluginAction('to_svg').register() # Instantiate and register to Pcbnew
StretchPluginAction('to_pcb').register() # Instantiate and register to Pcbnew