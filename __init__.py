from .flex_plugin_action import FlexPluginAction # Note the relative import!

FlexPluginAction('to_svg').register() # Instantiate and register to Pcbnew
FlexPluginAction('to_pcb').register() # Instantiate and register to Pcbnew