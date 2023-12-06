def merge_list_inner_join(list1:list , list2: list):
    """ Take common items in 2 list

    Args:
        list1 (list): list 1
        list2 (list): list 2

    Returns:
        list: inner join of list 1 & 2
    """
    return [item for item in list1 if item in list2]


def flatten_field_paths(related_fields):
    field_paths = []
    for related_model, fields in related_fields.items():
        for field in fields:
            field_path = f"{related_model}__{field}"
            field_paths.append(field_path)
    return field_paths