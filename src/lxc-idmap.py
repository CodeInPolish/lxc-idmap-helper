from argparse import ArgumentParser

MIN_ID = 0
MAX_ID = 65535


def validate_mapping(mapping: list) -> list:
    errors = list()
    for item in mapping:
        errors += validate_item(item)
    return errors


def validate_item(item: str) -> list:
    errors = list()
    mapping = item.split(":")
    if len(mapping) != 2:
        errors.append(f"{item} is not a valid entry.")
        return errors
    for val in mapping:
        try:
            number = int(val)
            if not (MIN_ID <= number and number <= MAX_ID): 
                errors.append(f"{val} is outside of the accepted {MIN_ID}-{MAX_ID} range.")
        except ValueError:
            errors.append(f"{val} is not a valid integer. Entry {item}")
    return errors


def show_errors(errors, label):
    print(f"Errors present in {label}")
    for error in errors:
        print(f"\t{error}")


def get_sorted_dict_mapping(mapping):
    dict_mapping = dict()
    for item in mapping:
        cont_id, host_id = item.split(":")
        dict_mapping[int(cont_id)] = int(host_id)
    return sorted(dict_mapping), dict_mapping


def create_mapping(mapping, label, offset):
    out = list()
    ordered_keys, dict_map = get_sorted_dict_mapping(mapping)
    for i, item in enumerate(ordered_keys):
        if i == 0 and item != 0:
            out.append(
                f"lxc.idmap: {label} 0 {offset} {item}"
            )
        elif i != 0:
            previous_id = ordered_keys[i-1]
            start_range = previous_id + 1 + offset
            remaining_entries = item - 1 - previous_id
            out.append(
                f"lxc.idmap: {label} {previous_id+1} {start_range} {remaining_entries}"
            )
        out.append(
            f"lxc.idmap: {label} {item} {dict_map[item]} 1"
        )
        
        if len(ordered_keys) - 1 == i:
            start_range = offset + item + 1
            remaining_entries = MAX_ID - item
            out.append(
                f"lxc.idmap: {label} {item+1} {start_range} {remaining_entries}"
            )
    return out


def main(u_mapping, g_mapping, offset):
    user_mapping = create_mapping(u_mapping, "u", offset)
    group_mapping = create_mapping(g_mapping, "g", offset)

    for map in (user_mapping, group_mapping):
        for item in map:
            print(item)
        

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", action="store", dest="user_mapping", type=str, nargs="*", help="User mappings")
    parser.add_argument("-g", "--group", action="store", dest="group_mapping", type=str, nargs="*", help="Group mappings")
    parser.add_argument("-o", "--offset", type=int, default=100000, help="Offset used for mapping uid/gid")
    
    args = parser.parse_args()

    errors = dict()
    errors["user"] = validate_mapping(args.user_mapping)
    errors["group"] = validate_mapping(args.group_mapping)
    
    terminate = 0
    for label in ("user", "group"):
        if len(errors[label]) != 0:
            terminate = 1
            show_errors(errors[label], label+" mapping")
    
    if terminate:
        exit(1)
    
    main(args.user_mapping, args.group_mapping, args.offset)