# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Anchor(Component):
    """An Anchor component.
Display links with theme styles. For more information, see: https://mantine.dev/core/anchor/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Primary content.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks.

- align (optional):
    Sets text-align css property.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (optional):
    Text color from theme.

- gradient (optional):
    Controls gradient settings in gradient variant only.

- href (string; optional):
    href.

- inherit (boolean; optional):
    Inherit font properties from parent element.

- inline (boolean; optional):
    Sets line-height to 1 for centering.

- lineClamp (number; optional):
    CSS -webkit-line-clamp property.

- size (optional):
    Predefined font-size from theme.fontSizes.

- style (dict; optional):
    Inline style override.

- target (a value equal to: "_blank", "_self"; optional):
    Target.

- transform (optional):
    Sets text-transform css property.

- variant (optional):
    Link or text variant.

- weight (optional):
    Sets font-weight css property."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, align=Component.UNDEFINED, color=Component.UNDEFINED, gradient=Component.UNDEFINED, href=Component.UNDEFINED, inherit=Component.UNDEFINED, inline=Component.UNDEFINED, lineClamp=Component.UNDEFINED, size=Component.UNDEFINED, target=Component.UNDEFINED, transform=Component.UNDEFINED, variant=Component.UNDEFINED, weight=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align', 'className', 'color', 'gradient', 'href', 'inherit', 'inline', 'lineClamp', 'size', 'style', 'target', 'transform', 'variant', 'weight']
        self._type = 'Anchor'
        self._namespace = 'dash_mantine_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align', 'className', 'color', 'gradient', 'href', 'inherit', 'inline', 'lineClamp', 'size', 'style', 'target', 'transform', 'variant', 'weight']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Anchor, self).__init__(children=children, **args)
