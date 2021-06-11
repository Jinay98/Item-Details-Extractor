import csv


class Node:

    def __init__(self, item_id, item_name, quantity, unit, level, raw_material_id):
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.unit = unit
        self.level = level
        self.raw_material_id = raw_material_id
        self.child = []

    def create_new_node(self):
        temp = Node(self.item_id, self.item_name, self.quantity, self.unit, self.level, self.raw_material_id)
        return temp

    @staticmethod
    def traverse_tree(root):
        if root is None:
            return
        q = [root]
        while len(q) != 0:

            n = len(q)

            # If this node has children
            while n > 0:

                # Dequeue an item from queue and print it
                p = q[0]
                q.pop(0)
                if len(p.child) != 0:
                    raw_material_data = []
                    base_item_data = {
                        "item_name": p.item_name,
                        "quantity": p.quantity,
                        "unit": p.unit
                    }
                    for raw_material in p.child:
                        raw_material_response = {
                            "raw_material": raw_material.item_name,
                            "quantity": raw_material.quantity,
                            "unit": raw_material.unit
                        }
                        raw_material_data.append(raw_material_response)

                    Node.create_csv_sheet(data=raw_material_data, base_item_data=base_item_data)
                for i in range(len(p.child)):
                    q.append(p.child[i])
                n -= 1

    @staticmethod
    def create_csv_sheet(data, base_item_data):
        if base_item_data:
            base_item_name = base_item_data.get("item_name")
            # data rows of csv file
            rows = [['Finished Good List'],
                    ["#", "Item Description", "Quantity", "Unit"]]

            # name of csv file
            filename = base_item_name + ".csv"
            rows.append([1, base_item_name, base_item_data.get(
                "quantity"), base_item_data.get("unit")])

            rows.append(["End of FG"])
            rows.append(["Raw Material List"])
            rows.append(["#", "Item Description", "Quantity", "Unit"])

            counter = 1
            for item in data:
                rows.append([counter, item.get("raw_material"),
                             item.get("quantity"), item.get("unit")])
                counter += 1

            rows.append(["End of RM"])
            # writing to csv file
            with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the data rows
                csvwriter.writerows(rows)
