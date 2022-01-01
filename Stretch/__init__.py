
from .kiplug.kicad import Stretch
from .kiplug.svg_writer import SvgWrite

plugin_svg = Stretch("to_svg")
plugin_svg.register()
plugin_pcb = Stretch("to_pcb")
plugin_pcb.register()