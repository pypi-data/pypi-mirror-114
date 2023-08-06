from avroc.util import clean_name
from avroc.avro_common import PRIMITIVES
from avroc.codegen.astutil import literal_from_default
from avroc.schema import expand_names, gather_named_types

from ast import (
    ClassDef,
    AnnAssign,
    Name,
    Expr,
    Constant,
    Store,
    Module,
    ImportFrom,
    alias,
    Load,
    Store,
    Tuple,
    Subscript,
)
try:
    from ast import unparse
except ImportError:
    from astunparse import unparse


class DataclassCompiler:
    def __init__(self, schema):
        self.schema = expand_names(schema)
        self.used_types = set()
        self.fullnames_to_classnames = dict()

    def generate_source_code(self):
        module = self.generate_module()
        return unparse(module)

    def generate_module(self):
        classdefs = self.generate_dataclasses(self.schema)
        imports = self.generate_type_imports()

        body = [
            ImportFrom(
                module="dataclasses",
                names=[alias(name="dataclass")],
                level=0,
            )
        ]
        body.append(imports)
        body.extend(classdefs)

        return Module(
            body=body,
            type_ignores=[],
        )

    def generate_dataclasses(self, schema):
        # Traverse the schema, hunting for records. Each one gets a dataclass.
        named_types = gather_named_types(schema)
        record_schemas = [schema for schema in named_types.values() if schema["type"] == "record"]
        return [self.generate_dataclass_for_record(s) for s in record_schemas]

    def generate_dataclass_for_record(self, schema):
        name = clean_name(schema["name"])

        class_def = ClassDef(
            name=clean_name(schema["name"]),
            bases=[],
            keywords=[],
            body=[],
            decorator_list=[
                Name(id='dataclass', ctx=Load()),
            ]
        )
        docstring = ""
        if "doc" in schema:
            docstring += "\n"
            docstring += "    " + schema["doc"]
            docstring += "\n"

        attr_docstrings = ""
        for field in schema["fields"]:
            class_def.body.append(self.generate_class_attribute(field))
            if "doc" in field:
                attr_docstrings += f"        {field['name']}: {field['doc']}\n"

        if len(attr_docstrings) > 0:
            docstring += "\n"
            docstring += "    Attributes:\n"
            docstring += attr_docstrings

        if len(docstring) > 0:
            docstring = Expr(value=Constant(value=docstring))
            class_def.body.insert(0, docstring)

        return class_def

    def generate_class_attribute(self, field_schema):
        attr = AnnAssign(
            target=Name(id=field_schema["name"], ctx=Store()),
            annotation=self.type_annotation(field_schema["type"]),
            simple=1,
        )
        if "default" in field_schema:
            attr.value = literal_from_default(field_schema["default"], field_schema["type"])
        return attr

    def type_annotation(self, schema):
        if isinstance(schema, str):
            name = ""
            primitive_name_mapping = {
                "null": "None",
                "boolean": "bool",
                "int": "int",
                "long": "int",
                "float": "float",
                "double": "float",
                "bytes": "bytes",
                "string": "str",
            }
            if schema in primitive_name_mapping:
                name = primitive_name_mapping[schema]
            else:
                name = clean_name(schema)
            return Name(id=name, ctx=Load())
        if isinstance(schema, list):
            # Special case for a union which has 2 options, one of which is 'null'
            if len(schema) == 2:
                if schema[0] == "null":
                    self.used_types.add("Optional")
                    return Subscript(
                        value=Name(id="Optional", ctx=Load()),
                        slice=self.type_annotation(schema[1]),
                        ctx=Load(),
                    )
                elif schema[1] == "null":
                    self.used_types.add("Optional")
                    return Subscript(
                        value=Name(id="Optional", ctx=Load()),
                        slice=self.type_annotation(schema[0]),
                        ctx=Load(),
                    )
            # Otherwise, union over the options
            self.used_types.add("Union")
            union_annotation = Subscript(
                value=Name(id="Union", ctx=Load()),
                slice=Tuple(
                    elts=[],
                    ctx=Load(),
                ),
                ctx=Load(),
            )
            for option in schema:
                union_annotation.slice.elts.append(self.type_annotation(option))
            return union_annotation

        if isinstance(schema, dict):
            if schema["type"] == "fixed":
                # Fixeds are just bytes
                return Name(id="bytes", ctx=Load())
            elif schema["type"] == "enum":
                # Enums are just strings
                return Name(id="str", ctx=Load())
            elif schema["type"] == "array":
                # Arrays produce an annotation like
                #  field_name: List[<array-item-type>]
                self.used_types.add("List")
                return Subscript(
                    value=Name(id="List", ctx=Load()),
                    slice=self.type_annotation(schema["items"]),
                    ctx=Load(),
                )
            elif schema["type"] == "map":
                # Maps produce an annotation like
                #  field_name: Dict[str, <map-value-type>]
                self.used_types.add("Dict")
                return Subscript(
                    value=Name(id="Dict", ctx=Load()),
                    slice=Tuple(
                        elts=[
                            Name(id="str", ctx=Load()),
                            self.type_annotation(schema["values"]),
                        ],
                        ctx=Load(),
                    ),
                    ctx=Load(),
                )
            elif schema["type"] == "record" or schema["type"] == "error":
                # Nested record definition; refer to the type by name.
                return Name(
                    id=clean_name(schema["name"]),
                    ctx=Load(),
                )
            else:
                return self.type_annotation(schema["type"])

    def generate_type_imports(self):
        stmt = ImportFrom(
            module="typing",
            names=[],
            level=0,
        )
        for name in self.used_types:
            stmt.names.append(alias(name=name))
        return stmt
