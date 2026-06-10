import json

shipments = [
    {"id": "SHP-001", "weight_lbs": 8000,  "region": "West",    "hazmat": False},
    {"id": "SHP-002", "weight_lbs": 120,   "region": "East",    "hazmat": False},
    {"id": "SHP-003", "weight_lbs": 6000,  "region": "North",   "hazmat": True},
    {"id": "SHP-004", "weight_lbs": 3500,  "region": "Central", "hazmat": False},
    {"id": "SHP-005", "weight_lbs": 800,   "region": "South",   "hazmat": False},
    {"id": "SHP-006", "weight_lbs": 9000,  "region": "East",    "hazmat": True},
    {"id": "SHP-007", "weight_lbs": 2500,  "region": "West",    "hazmat": False},
    {"id": "SHP-008", "weight_lbs": 5500,  "region": "South",   "hazmat": False},
]

def execute_carrier_routing(rule, shipments):
    results = []

    for shipment in shipments:
        region = shipment["region"]
        weight = shipment["weight_lbs"]
        hazmat = shipment["hazmat"]
        assignment = {}

        # Step 1: Hazmat always wins
        if hazmat:
            if region in ["West", "North"]:
                carrier = "Hazpac"
            else:
                carrier = "Hazco"
            assignment = {
                "id": shipment["id"],
                "carrier": carrier,
                "compliance_flag": True,
                "reason": f"Hazmat shipment routed to specialized carrier ({carrier})"
            }

        # Step 2: Weight tiers for standard freight
        elif weight <= 150:
            assignment = {
                "id": shipment["id"],
                "carrier": "Common Carrier",
                "compliance_flag": False,
                "reason": f"Weight ({weight} lbs) qualifies for common carrier"
            }

        elif weight <= 2000:
            assignment = {
                "id": shipment["id"],
                "carrier": "Private Fleet",
                "dispatch_record": {
                        "action": "route_to_private_fleet",
                        "tms_endpoint": "internal_dispatch",
                        "payload": {
                            "shipment_id": shipment["id"],
                            "weight_lbs": weight,
                            "region": region,
                            "priority": "Standard"
                        }
                },
                "compliance_flag": False,
                "reason": f"Weight ({weight} lbs) qualifies for private fleet dispatch"
            }

        elif weight <= 5000:
            ltl_carriers = {
                "West": "Cutting Edge LTL",
                "Central": "Heartland Trucking",
                "North": "Viking Transport",
                "East": "Sunset Limited",
                "South": "Sunset Limited"
            }
            carrier = ltl_carriers.get(region, "Regional LTL")
            assignment = {
                "id": shipment["id"],
                "carrier": carrier,
                "compliance_flag": False,
                "reason": f"Weight ({weight} lbs) qualifies for LTL, region {region} uses {carrier}"
            }

        else:
            carrier = "FedEx Freight" if region in ["West", "South"] else "UPS Freight"
            assignment = {
                "id": shipment["id"],
                "carrier": carrier,
                "compliance_flag": False,
                "reason": f"Weight ({weight} lbs) requires specialized freight, region {region} uses {carrier}"
            }

        results.append(assignment)

    return results


if __name__ == "__main__":
    rule = {"trigger": {"condition": "carrier_routing_rules"}}

    print("Running carrier routing rules against shipments...\n")
    assignments = execute_carrier_routing(rule, shipments)

    print(f"Carrier assignments generated: {len(assignments)}\n")
    print(json.dumps(assignments, indent=2))