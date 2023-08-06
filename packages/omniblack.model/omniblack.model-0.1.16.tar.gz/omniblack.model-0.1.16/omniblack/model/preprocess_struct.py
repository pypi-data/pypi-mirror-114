from typing import NamedTuple


class PreprocessInformation(NamedTuple):
    meta_structs: tuple[str]


def preprocess_struct_def(struct_def) -> PreprocessInformation:
    meta_structs = set()
    child_fields = (
        field
        for field in struct_def['fields']
        if field['type'] == 'child'
    )

    meta_ref_fields = (
        field
        for field in child_fields
        if field['attrs']['struct_name'].startswith('meta:')
    )

    for field in meta_ref_fields:
        struct_name = field['attrs']['struct_name'].removeprefix('meta:')
        field['attrs']['struct_name'] = struct_name
        meta_structs.add(struct_name)

    return PreprocessInformation(tuple(meta_structs))
