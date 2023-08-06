"""Upgrade Assembly"""

import ast
import typing as T
from collections import defaultdict

import astor

ARG = T.TypeVar('ARG')  # TODO: bind str
VALUE = T.TypeVar('VALUE')  # TODO: bind Any
PATH = T.TypeVar('PATH')  # TODO: bind str

field_arguments: set = {
    'default',
    'missing',
    'data_key',
    'attribute',
    'validate',
    'required',
    'allow_none',
    'load_only',
    'dump_only',
    'error_messages',
    'metadata'
}


MAPPING = {}
TREE = defaultdict(dict)


def replace_as_metadata_kw(
    file: PATH,
    *,
    indent: int = 4,
):
    """
    Args:
        - file (str): source code file path
        - indent (int): indent of source code

    ref: https://www.youtube.com/watch?v=wn1CcLck-D4&ab_channel=PyConChina&t=1320
    """
    tree = astor.parse_file(file)
    node_transformer = ReplaceAsMetadataKW()

    find_rename_fields = FindRenameFields()
    find_rename_ma = FindRenameMarshmallow()
    find_imported_into_field = FindImportedIntoField()
    MAPPING[id(find_rename_fields)] = id(node_transformer)
    MAPPING[id(find_rename_ma)] = id(node_transformer)
    MAPPING[id(find_imported_into_field)] = id(node_transformer)

    find_rename_fields.visit(tree)
    find_rename_ma.visit(tree)
    find_imported_into_field.visit(tree)

    new_tree = node_transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    # TODO: formatter + comment issue
    #   - formatter: yapf + --style='{based_on_style: pep8, indent_width: 2}'
    #   - comment: no solution yet
    codes = astor.to_source(new_tree, indent_with=' ' * indent)
    return codes


class FindRenameFields(ast.NodeTransformer):
    def visit_ImportFrom(self, node: ast.ImportFrom) -> T.Any:
        node_transformer_id = MAPPING[id(self)]

        if node.module == 'marshmallow':
            for alias in node.names:
                if alias.name == 'fields':
                    # case: `from marshmallow import fields as ma_fields`
                    TREE[node_transformer_id]['fields'] = alias.asname or alias.name

        return node


class FindRenameMarshmallow(ast.NodeTransformer):
    def visit_Import(self, node: ast.Import) -> T.Any:
        node_transformer_id = MAPPING[id(self)]

        for alias in node.names:
            if alias.name == 'marshmallow':
                # case: `import marshmallow as ma`
                TREE[node_transformer_id]['marshmallow'] = alias.asname or alias.name

        return node


class FindImportedIntoField(ast.NodeTransformer):
    def visit_ImportFrom(self, node: ast.ImportFrom) -> T.Any:
        node_transformer_id = MAPPING[id(self)]

        if node.module.endswith('marshmallow.fields'):
            if 'imported_fields' not in TREE[node_transformer_id]:
                TREE[node_transformer_id]['imported_fields'] = set()
            for alias in node.names:
                TREE[node_transformer_id]['imported_fields'].add(alias.asname or alias.name)
        return node


class ReplaceAsMetadataKW(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> T.Any:
        replace_flag = False

        # case:
        #   from marshmallow import fields
        #   class FooSchema(Schema):
        #       foo = fields.String(title='foo', description='foo')
        #                   ^
        if isinstance(node.func, ast.Attribute):
            attr: ast.Attribute = node.func
            # case: `marshmallow.fields.String()`
            # Call(func=Attribute(value=Attribute(value=Name(id='marshmallow', ctx=), attr='fields', ctx=), attr='String', ctx=), args=[], keywords=[
            # ^         ^               ^               ^                                   ^                           ^
            # node     node.func       node.func.value node.func.value.value               node.func.value.attr         node.func.attr
            #
            if isinstance(attr.value, ast.Attribute):
                if isinstance(attr.value.value, ast.Name):
                    if attr.value.value.id == TREE[id(self)]['marshmallow']:
                        if attr.value.attr == 'fields':
                            replace_flag = True

            # foo = fields.String(title='foo', description='foo')
            #       ^
            if isinstance(attr.value, ast.Name):
                if node.func.value.id == TREE[id(self)]['fields']:
                    replace_flag = True
                # Just others ast.Call, but not rely to marshmallow.fields
                else:
                    pass
        # case: `from marshmallow.fields import String`
        elif (isinstance(node.func, ast.Name)
            and node.func.id in TREE[id(self)]['imported_fields']):
            replace_flag = True
        else:
            pass

        if replace_flag:
            kws = node.keywords[:]
            node.keywords.clear()
            metadata: T.List[T.Tuple[ARG, VALUE]] = []
            for kw_obj in kws:
                # metadata
                if kw_obj.arg not in field_arguments:
                    metadata.append( (kw_obj.arg, kw_obj.value) )
                # the sig.parameters
                else:
                    node.keywords.append(kw_obj)

            for kw_obj in node.keywords:
                # TODO: fields.String(required=True, title='name', metadata={'description': '...'})
                if kw_obj.arg == 'metadata':
                    raise RuntimeError('not handle ths condition!')

            if metadata:
                node.keywords.append(ast.keyword(
                    arg='metadata',
                    value=ast.Dict(
                        keys=[ast.Constant(value=arg, kind=None)
                            for arg, _ in metadata],
                        values= [value for _, value in metadata]
                        )
                ))
        return node
