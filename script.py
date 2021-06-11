import csv

from node import Node


def gather_data(csv_file_path):
    result = []
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        for row in csv_reader:
            result.append(row)
    return result


def clean_data(data):
    cleaned_data = []
    item_id = 0
    raw_material_id = 1
    previous_item_name = ""
    base_items = []
    for item in data:
        item_name = item.get("Item Name")
        res = {
            "item_name": item_name,
            "level": int(item.get("Level")[-1]),
            "raw_material": item.get("Raw material"),
            "quantity": float(item.get("Quantity")),
            "unit": item.get("Unit ")
        }
        if previous_item_name != item_name:
            item_id += 1
            previous_item_name = item_name
            raw_material_id = 1
            base_items.append({
                "item_name": item_name,
                "quantity": float(item.get("Quantity")),
                "unit": item.get("Unit "),
                "item_id": item_id,
                "level": 0,
                "raw_material_id": 0

            })
        res["item_id"] = item_id
        res["raw_material_id"] = raw_material_id
        raw_material_id += 1
        cleaned_data.append(res)

    return cleaned_data, base_items


def get_item_data(item_id, data, item_level, raw_material_id=None, check_item_level=False):
    result = []
    for item in data:
        if check_item_level:
            if item.get("item_id") == item_id and item.get("level") >= item_level and item.get(
                    "raw_material_id") > raw_material_id:
                result.append(item)
        else:
            if item.get("item_id") == item_id:
                result.append(item)
    return sorted(result, key=lambda k: k['raw_material_id'])


def get_max_level(item_id, data):
    max_level = -1
    for item in data:
        if item.get("item_id") == item_id:
            if item.get("level") > max_level:
                max_level = item.get("level")
    return max_level


def create_child_nodes(item_id, data, parent_node, max_level):
    if parent_node.level == max_level:
        return parent_node
    else:
        item_data = get_item_data(item_id, data, parent_node.level, parent_node.raw_material_id, check_item_level=True)

        for item in item_data:
            if parent_node.level == item.get("level"):
                return parent_node
            elif parent_node.level + 1 == item.get("level") and parent_node.raw_material_id < item.get(
                    "raw_material_id"):
                node_obj = Node(item_id=item.get("item_id"), item_name=item.get("raw_material"),
                                quantity=item.get("quantity"), unit=item.get("unit"),
                                level=item.get("level"),
                                raw_material_id=item.get("raw_material_id"))
                child_node = node_obj.create_new_node()
                ans = create_child_nodes(child_node.item_id, item_data, child_node, max_level)
                parent_node.child.append(ans)
        return parent_node


if __name__ == '__main__':
    root_list = []
    csv_file_path = r'data.csv'

    data = gather_data(csv_file_path)
    cleaned_data, base_items = clean_data(data)

    for item in base_items:
        item_id = item.get("item_id")
        node = Node(item_id=1, item_name=item.get("item_name"), quantity=item.get("quantity"),
                    unit=item.get("unit"), level=0, raw_material_id=item.get("raw_material_id"))
        root = node.create_new_node()
        all_item_data = get_item_data(item_id, cleaned_data, None, False)
        max_level = get_max_level(item_id, cleaned_data)

        parent = create_child_nodes(item_id, all_item_data, root, max_level)
        root_list.append(root)
    for root in root_list:
        Node.traverse_tree(root)
