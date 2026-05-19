from src.index import lambda_handler

if __name__ == "__main__":

    payload = {
        "detail": {
            "payload": [{
                "now": {
                    "time": "2025-02-17T18:21:50.288Z",
                    "v": 1.98,
                    "i": 26.4,
                    "soc": 93,
                    "mode": 1,
                    "as": 0,
                    "v_as": 2,
                    "ci_as": 2,
                    "di_as": 0,
                    "soc_as": 0,
                    "e_state": "E",
                },
                "prev": {
                    "time": "2025-02-17T18:21:50.288Z",
                    "v": 1.98,
                    "i": 19.4,
                    "soc": 93,
                    "mode": 1,
                    "as": 0,
                    "v_as": 2,
                    "ci_as": 2,
                    "di_as": 0,
                    "soc_as": 0,
                    "e_state": "E",
                },
                "asset_code": "a21",
                "site_code": "s20",
                "bank_unit_id": "Bank_1",
                "battery_unit_id": "1X15097169",
                "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                "tenant_namespace": "jp_energy",
            }]
        }
    }

    # Call the process_event function
    result = lambda_handler(payload, "sahithi")

    print(f"Event processing result: {result}")
