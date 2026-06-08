import json

# Sample inventory data
inventory = [
    {"sku": "SKU-001", "name": "Brake Pads",        "on_hand": 45,  "reorder_point": 50,  "reorder_qty": 100},
    {"sku": "SKU-002", "name": "Oil Filters",        "on_hand": 120, "reorder_point": 75,  "reorder_qty": 200},
    {"sku": "SKU-003", "name": "Fuel Injectors",     "on_hand": 12,  "reorder_point": 30,  "reorder_qty": 50},
    {"sku": "SKU-004", "name": "Transmission Fluid", "on_hand": 80,  "reorder_point": 100, "reorder_qty": 150},
    {"sku": "SKU-005", "name": "Air Filters",        "on_hand": 200, "reorder_point": 60,  "reorder_qty": 120},
]
def execute_reorder_rule(rule, inventory):
    purchase_orders = []
    
    for item in inventory:
        if item["on_hand"] < item["reorder_point"]:
            po = {
                "sku": item["sku"],
                "name": item["name"],
                "quantity": item["reorder_qty"],
                "reason": f"On hand ({item['on_hand']}) below reorder point ({item['reorder_point']})"
            }
            purchase_orders.append(po)
    
    return purchase_orders

if __name__ == "__main__":
    rule = {"trigger": {"condition": "on_hand_inventory < reorder_point"}}
    
    print("Running reorder rule against inventory...\n")
    orders = execute_reorder_rule(rule, inventory)
    
    print(f"Purchase orders generated: {len(orders)}")
    print(json.dumps(orders, indent=2))