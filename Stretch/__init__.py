from .kiplug.kicad import Stretch

plugin_svg = Stretch("to_svg")
plugin_svg.register()
plugin_pcb = Stretch("to_pcb")
plugin_pcb.register()
