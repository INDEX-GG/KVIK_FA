import datetime
import math


def get_post_additional_fields(post_additional_fields, required_additional_fields):
    additional_fields = {x: post_additional_fields[x] for x in post_additional_fields if x in
                         set(s["alias"] for s in required_additional_fields)}
    return additional_fields


def get_yearly_quarters():
    yearly_quarters = []
    month = datetime.datetime.utcnow().month
    year = datetime.datetime.utcnow().year
    quarter = math.ceil(month / 3)
    yearly_quarters.append("Дом сдан")
    for i in range(quarter, 5):
        yearly_quarters.append(f"{i} квартал {year}")
    for i in range(1, 5):
        yearly_quarters.append(f"{i} квартал {year + 1}")
    yearly_quarters.append(f"{year + 2} год и позднее")
    return yearly_quarters


def get_blank_required_fields(post_additional_fields, required_additional_fields):
    additional_fields = set(x for x in post_additional_fields if post_additional_fields[x] is not None)
    required_additional_fields_aliases = set(x["alias"] for x in required_additional_fields if x["requiring"] is True)
    blank_fields = list(required_additional_fields_aliases - additional_fields)
    return blank_fields


def get_not_for_edit_fields(post_additional_fields, required_additional_fields):
    additional_fields = set(x for x in post_additional_fields if post_additional_fields[x] is not None)
    ability_to_edit_fields_aliases = set(x["alias"] for x in required_additional_fields
                                         if x["type"]["ability_to_edit"] is True)
    not_for_edit_fields = list(additional_fields - ability_to_edit_fields_aliases)
    return not_for_edit_fields


def validate_additional_fields(post_additional_fields, additional_fields_schema):
    errors = []
    for additional_field in additional_fields_schema:
        if additional_field["alias"] in post_additional_fields:
            field = post_additional_fields[additional_field["alias"]]
            try:
                match additional_field["type"]["name"]:
                    case "number":
                        validate_number_field(value=field,
                                              type_properties=additional_field["type"]["properties"])
                    case "text":
                        validate_text_field(value=field,
                                            type_properties=additional_field["type"]["properties"])
                    case "text_hint":
                        validate_text_hint_field(value=field,
                                                 type_properties=additional_field["type"]["properties"])
                    case "yearly_quarter_hint":
                        validate_yearly_quarter_hint_field(value=field)
                    case "checkboxes":
                        validate_checkboxes_field(value=field,
                                                  type_properties=additional_field["type"]["properties"])
                    case "dynamic_text_hint":
                        validate_dynamic_text_hint_field(value=field,
                                                         type_properties=additional_field["type"]["properties"],
                                                         dependencies=additional_field["dependencies"])
                    case "colors":
                        validate_colors_field(value=field,
                                              type_properties=additional_field["type"]["properties"])
                    case "checkbox":
                        validate_checkbox_field(value=field)
            except Exception as error:
                errors.append({"alias": additional_field["alias"], "error": str(error)})
    return errors


def validate_number_field(value, type_properties):
    match type_properties["type"]:
        case "int":
            assert isinstance(value, int), "Value not valid type"
        case "float":
            assert isinstance(value, int | float), "Value not valid type"
    assert type_properties["min"] <= value <= type_properties["max"], "Value not in limits"


def validate_checkbox_field(value):
    assert value in [True, False], "Value not valid type"


def validate_colors_field(value, type_properties):
    assert value in type_properties["values"], "Value not in valid values array"


def validate_text_hint_field(value, type_properties):
    assert value in type_properties["values"], "Value not in valid values array"


def validate_yearly_quarter_hint_field(value):
    valid_values = get_yearly_quarters()
    assert value in valid_values, "Value not in valid values array"


def validate_checkboxes_field(value, type_properties):
    titles = [x["title"] for x in value]
    assert set(titles) == set(type_properties["values"]), "Not all or extra checkboxes"
    assert len(set(titles)) == len(titles), "Duplicated checkboxes"
    assert len(set(x["value"] for x in value if x["value"] not in [True, False])) == 0, "Value not valid type"


def validate_text_field(value, type_properties):
    # "Value not valid regexp"
    pass


def validate_dynamic_text_hint_field(value, type_properties, dependencies):
    # "Value not in valid values array"
    pass
