import inspect
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet

from bam_masterdata.utils import import_module


def entities_to_excel(
    worksheet: 'Worksheet',
    module_path: str,
    definitions_module: Any,
) -> None:
    """
    Export entities to the Excel file. The Python modules are imported using the function `import_module`,
    and their contents are inspected (using `inspect`) to find the classes in the datamodel containing
    `defs` and with a `to_json` method defined. Each row is then appended to the `worksheet`.

    Args:
        worksheet (Worksheet): The worksheet to append the entities.
        module_path (str): Path to the Python module file.
        definitions_module (Any): The module containing the definitions of the entities. This is used
            to match the header definitions of the entities.
    """
    def_members = inspect.getmembers(definitions_module, inspect.isclass)
    module = import_module(module_path=module_path)

    # Special case of `PropertyTypeDef` in `property_types.py`
    if 'property_types.py' in module_path:
        for name, obj in inspect.getmembers(module):
            if name.startswith('_') or name == 'PropertyTypeDef':
                continue

            # Entity title
            worksheet.append([obj.excel_name])

            # Entity header definitions and values
            worksheet.append(obj.excel_headers)
            row = []
            for f_set in obj.model_fields.keys():
                if f_set == 'data_type':
                    val = obj.data_type.value
                else:
                    val = getattr(obj, f_set)
                row.append(val)
            worksheet.append(row)
        return None

    # All other datamodel modules
    for _, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure the class has the `to_json` method
        if not hasattr(obj, 'defs') or not callable(getattr(obj, 'to_json')):
            continue

        obj_instance = obj()

        # Entity title
        obj_definitions = obj_instance.defs
        worksheet.append([obj_definitions.excel_name])

        # Entity header definitions and values
        for def_name, def_cls in def_members:
            if def_name == obj_definitions.name:
                break
        worksheet.append(obj_definitions.excel_headers)
        header_values = [
            getattr(obj_definitions, f_set) for f_set in def_cls.model_fields.keys()
        ]
        worksheet.append(header_values)

        # Properties assignment for ObjectType
        if obj_instance.entity_type == 'ObjectType':
            if not obj_instance.properties:
                continue
            worksheet.append(obj_instance.properties[0].excel_headers)
            for prop in obj_instance.properties:
                row = []
                for f_set in prop.model_fields.keys():
                    if f_set == 'data_type':
                        val = prop.data_type.value
                    else:
                        val = getattr(prop, f_set)
                    row.append(val)
                worksheet.append(row)
        # Terms assignment for VocabularyType
        elif obj_instance.entity_type == 'VocabularyType':
            if not obj_instance.terms:
                continue
            worksheet.append(obj_instance.terms[0].excel_headers)
            for term in obj_instance.terms:
                worksheet.append(
                    getattr(term, f_set) for f_set in term.model_fields.keys()
                )

        # ? do the PropertyTypeDef need to be exported to Excel?

        worksheet.append([''])  # empty row after entity definitions
