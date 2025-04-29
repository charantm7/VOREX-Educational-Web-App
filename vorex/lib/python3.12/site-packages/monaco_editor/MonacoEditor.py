# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MonacoEditor(Component):
    """A MonacoEditor component.
Monaco Editor based of https://microsoft.github.io/monaco-editor/

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- defaultLanguage (string; optional):
    Default language format for the editor.

- height (string; optional):
    height for the editor.

- options (dict; optional):
    The value displayed in the input.

- value (string; required):
    A value that will be printed on the editor."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'monaco_editor'
    _type = 'MonacoEditor'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.REQUIRED, options=Component.UNDEFINED, height=Component.UNDEFINED, defaultLanguage=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'defaultLanguage', 'height', 'options', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'defaultLanguage', 'height', 'options', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['value']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(MonacoEditor, self).__init__(**args)
