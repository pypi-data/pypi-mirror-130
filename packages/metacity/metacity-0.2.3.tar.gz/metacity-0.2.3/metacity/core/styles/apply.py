from metacity.core.styles.style import Style
from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.datamodel.project import Project
from metacity.filesystem import styles as fs
from typing import Union
from typing import Dict
from lark import Lark, Transformer
from functools import reduce
from typing import  Hashable
import numpy as np



STYLEGRAMMAR = r"""
    layer_rule_list: (layer_rules)*
    layer_rules: ("@layer" "(" string ")" "{" [(rule)*] "}")
    rule: visibility | pickability | layer_color | mapping | meta_rules

    visibility: ("@visible" ":" boolean ";")
    pickability: ("@pickable" ":" boolean ";")

    layer_color: ("@color" ":" color ";")

    mapping: source | target
    source: ("@source" "{" [ meta_rules ] "}")
    target: ("@target" "{" [ meta_rules ] "}")

    meta_rules: (meta_rule)* 
    meta_rule: ("@meta" "(" name_link ")" "{" [key_style ";"]* "}")

    name_link: (string [("." string)*])
    key_style: (key ":" color)
    
    key: string | any

    any: "@default"
    boolean: "true" -> true | "false" -> false
    string: NAME | ESCAPED_STRING
    color: COLOR
    NAME: (/\w/+)
    COLOR: ("#" HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT)

    %import common.HEXDIGIT
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    """

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key] #take the latter value
        else:
            a[key] = b[key]
    return a


ANYKEY = "@default"


class TreeToStyle(Transformer):
    def layer_rule_list(self, layer_rule_list_):
        return dict(layer_rule_list_)

    def layer_rules(self, layer_rules_):
        name, *rrules = layer_rules_
        output = {}
        reduce(merge, [output] + [r[0] for r in rrules])
        return (name, output)

    def rule(self, rule_):
        return rule_

    def visibility(self, v):
        return {"visible": v[0]}

    def pickability(self, p):
        return {"pickability": p[0]}

    def layer_color(self, layer_color_):
        return {"color": layer_color_[0]}

    def mapping(self, mapping_):
        output = {
            "source": {},
            "target": {}
        }

        reduce(merge, [output, mapping_[0]])
        return output

    def source(self, source_rule_):
        return {"source": source_rule_[0]}

    def target(self, target_rule_):
        return {"target": target_rule_[0]}

    def meta_rules(self, o):
        return {'meta_rules': dict(o)}

    def meta_rule(self, meta_rule_):
        key, *styles = meta_rule_
        return (key, dict(styles))

    def name_link(self, name_link_):
        return tuple(name_link_)

    def key_style(self, key_style_):
        return key_style_

    def key(self, key_):
        return key_[0]

    def any(self, any_):
        return ANYKEY

    def NAME(self, name_):
        return str(name_)

    def ESCAPED_STRING(self, escaped_string_):
        return str(escaped_string_[1:-1])
    
    def string(self, string_):
        return string_[0]

    def number(self, number_):
        return float(number_[0])

    def color(self, color_):
        (color_,) = color_
        return int(color_[1:3], 16), int(color_[3:5], 16), int(color_[5:7], 16)

    true = lambda self, _: True
    false = lambda self, _: False


def default(dict, key):
    if key in dict:
        return dict[key]
    return {}

class LayerStyler:
    def __init__(self, style = None):
        self.style = style if style is not None else {}
        if style is not None:
            self.meta_rules = default(style, 'meta_rules')
            self.source = default(default(style, 'source'), 'meta_rules')
            self.target = default(default(style, 'target'), 'meta_rules')
        else:
            self.meta_rules = {}
            self.source = {}
            self.target = {}

    @property
    def visible(self):
        if 'visible' in self.style:
            return self.style['visible']
        return True

    @property
    def pickable(self):
        if 'pickable' in self.style:
            return self.style['pickable']
        return True

    @property
    def default_color(self):
        if 'color' in self.style:
            return self.style['color']
        return 255, 255, 255

    def source_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.source)

    def target_object_color(self, object_meta):
        return self.apply_rules(object_meta, self.target)

    def object_color(self, object_meta):
        return self.apply_rules(object_meta, self.meta_rules)

    def apply_rules(self, object_meta, rules: Dict):
        for key, value_style in rules.items():
            matched, meta_subtree = self.get_value(object_meta, key)
            if matched:
                if (isinstance(meta_subtree, Hashable) and meta_subtree in value_style):
                    return value_style[meta_subtree]
                if ANYKEY in value_style:
                    return value_style[ANYKEY]

        return self.default_color

    def get_value(self, meta_subtree, key):
        match = True
        for part in key:
            if part in meta_subtree:
                meta_subtree = meta_subtree[part]
            else:
                match = False
                break
        if match:
            return True, meta_subtree # meta_subtree is now value in metadata
        return False, None


def parse(raw_styles):
    parser = Lark(STYLEGRAMMAR, start='layer_rule_list', lexer='dynamic_complete')
    tree = parser.parse(raw_styles)
    return TreeToStyle().transform(tree)


def layer_style(layer: Union[Layer, LayerOverlay], parsed_styles):
    name = layer.name
    if name in parsed_styles:
        return LayerStyler(parsed_styles[name])
    else:
        return LayerStyler()


def compute_layer_colors(layer: Layer, color_function):
    colors = np.empty((layer.size, 3), dtype=np.uint8)
    for i, object in enumerate(layer.objects):
        colors[i] = color_function(object.meta)
    return colors


def apply_layer_style(styler: LayerStyler, style: Style, layer: Layer):
    colors = compute_layer_colors(layer, styler.object_color)
    style.write_colors(layer.name, buffer=colors)


def apply_overlay_style(styler: LayerStyler, style: Style, overlay: LayerOverlay):
    color_source = compute_layer_colors(style.project.get_layer(overlay.source_layer, load_model=False), styler.source_object_color) 
    color_target = compute_layer_colors(style.project.get_layer(overlay.target_layer, load_model=False), styler.target_object_color)
    style.write_colors(overlay.name, buffer_source=color_source, buffer_target=color_target)


def apply_style_to_layer(styler: LayerStyler, style: Style, layer: Union[Layer, LayerOverlay]):
    if isinstance(layer, Layer):
        apply_layer_style(styler, style, layer)
    elif isinstance(layer, LayerOverlay):
        apply_overlay_style(styler, style, layer)
    else:
        raise Exception("Unknown layer type")


def apply_style(project: Project, style_name: str):
    mss_file = fs.style_mss(project.dir, style_name)
    styles = fs.base.read_mss(mss_file)
    parsed = parse(styles)
    style = Style(project, style_name)

    for layer in project.clayers(load_model=False):
        styler = layer_style(layer, parsed)
        apply_style_to_layer(styler, style, layer)




 