def get_blank_required_fields(post_additional_fields, required_additional_fields):
    additional_fields = set(x.alias for x in list(post_additional_fields) if x.value is not None)
    required_additional_fields_aliases = set(x["alias"] for x in required_additional_fields if x["requiring"] is True)
    blank_fields = list(required_additional_fields_aliases - additional_fields)
    return blank_fields


def check_duplicate_fields(post_additional_fields):
    additional_fields = set(x.alias for x in list(post_additional_fields))
    if len(post_additional_fields) != len(additional_fields):
        return False
    return True
