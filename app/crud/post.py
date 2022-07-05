def get_blank_required_fields(post_additional_fields, required_additional_fields):
    post_additional_fields = set(x.alias for x in list(post_additional_fields) if x.value is not None)
    required_additional_fields_aliases = set(x["alias"] for x in required_additional_fields if x["requiring"] is True)
    blank_fields = list(required_additional_fields_aliases - post_additional_fields)
    return blank_fields
