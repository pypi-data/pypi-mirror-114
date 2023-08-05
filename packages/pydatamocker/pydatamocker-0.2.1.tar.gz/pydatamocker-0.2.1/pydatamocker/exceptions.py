class UnsupportedMockTypeException(Exception):

    def __init__(self, mock_type: str):
        msg = f"Kind '{mock_type}' is not supported"
        super().__init__(msg)


class SchemaPropValueException(Exception):

    def __init__(self, prop, value, rule):
        fmtd_rule = str(rule).lower().strip(' ')
        msg = f"Invalid property value for '{prop}'. Value: '{value}' {fmtd_rule}"
        super().__init__(msg)


class SchemaRepeatedFieldException(Exception):

    def __init__(self, field_name):
        msg = f"Repeated field: '{field_name}'"
        super().__init__(msg)


class MissingPropsException(Exception):

    def __init__(self, mock_type: str, missing_props: set):
        msg = f"Missing required fields for kind '{mock_type}': {str(missing_props)}"
        super().__init__(msg)
