import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.index import *


class TestStateTransition(unittest.TestCase):
    def test_state_transition_normal_to_error(self):
        test_cases = [
            # Test case 1: Voltage as a New Error
            {
                "description": "Testing  Voltage as a New Error",
                "payload": [
                    {
                        "now": {
                            "time": "2025-02-17T18:21:50.288Z",
                            "v": 2.98,
                            "i": 26.4,
                            "soc": 93,
                            "mode": 1,
                            "as": 0,
                            "v_as": 1,
                            "ci_as": 0,
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
                            "v_as": 0,
                            "ci_as": 0,
                            "di_as": 0,
                            "soc_as": 0,
                            "e_state": "N",
                        },
                        "asset_code": "a21",
                        "site_code": "s20",
                        "bank_unit_id": "Bank_1",
                        "battery_unit_id": "1X15097169",
                        "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                        "tenant_namespace": "jp_energy",
                    }
                ],
                "expected_error": "v",
            },
            # Test case 2: Current as a New Error
            {
                "description": "Testing Current as a New Error",
                "payload": [
                    {
                        "now": {
                            "time": "2025-02-17T18:21:50.288Z",
                            "v": 1.98,
                            "i": 26.4,
                            "soc": 93,
                            "mode": 1,
                            "as": 0,
                            "v_as": 0,
                            "ci_as": 2,
                            "di_as": 0,
                            "soc_as": 0,
                            "e_state": "E",
                        },
                        "prev": {
                            "time": "2025-02-17T18:21:50.288Z",
                            "v": 1.98,
                            "i": 10.94,
                            "soc": 93,
                            "mode": 1,
                            "as": 0,
                            "v_as": 0,
                            "ci_as": 0,
                            "di_as": 0,
                            "soc_as": 0,
                            "e_state": "N",
                        },
                        "asset_code": "a21",
                        "site_code": "s20",
                        "bank_unit_id": "Bank_1",
                        "battery_unit_id": "1X15097169",
                        "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                        "tenant_namespace": "jp_energy",
                    }
                ],
                "expected_error": "v",
            },
            # Test case 3: Discharge Current as a New Error
            {
                "description": "Testing Discharge Current as a New Error",
                "payload": [
                    {
                        "now": {
                            "time": "2025-02-17T18:21:50.288Z",
                            "v": 1.98,
                            "i": -26.4,
                            "soc": 93,
                            "mode": -1,
                            "as": 0,
                            "v_as": 0,
                            "ci_as": 0,
                            "di_as": 1,
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
                            "v_as": 0,
                            "ci_as": 0,
                            "di_as": 0,
                            "soc_as": 0,
                            "e_state": "N",
                        },
                        "asset_code": "a21",
                        "site_code": "s20",
                        "bank_unit_id": "Bank_1",
                        "battery_unit_id": "1X15097169",
                        "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                        "tenant_namespace": "jp_energy",
                    }
                ],
                "expected_error": "v",
            },
            # Test case 4: SOC as a New Error
            {
                "description": "Testing SOC as a New Error",
                "payload":[
                    {
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.98,
                        "i": 26.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 0,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 1,
                        "e_state": "E",
                    },
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.98,
                        "i": 19.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 0,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                        "e_state": "N",
                    },
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                }],
                "expected_error": "v",
            },
            # Test case 5: Voltage and Current as New Errors
            {
                "description": "Testing Voltage and Current as New Errors",
                "payload":[
                    {
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.90,
                        "i": 26.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 2,
                        "ci_as": 3,
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
                        "v_as": 0,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                        "e_state": "N",
                    },
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                }],
                "expected_error": "v",
            },
            # Test case 6: Voltage and SOC as New Errors
            {
                "description": "Testing Voltage and SOC as New Errors",
                "payload": [
                    {
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.90,
                        "i": 26.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 2,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 1,
                        "e_state": "E",
                    },
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.98,
                        "i": 19.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 0,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                        "e_state": "N",
                    },
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                }],
                "expected_error": "v",
            },
            # Test case 7: Voltage, Current, and SOC as New Errors
            {
                "description": "Testing Voltage, Current, and SOC as New Errors",
                "payload": [
                    {
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.90,
                        "i": 26.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 2,
                        "ci_as": 2,
                        "di_as": 0,
                        "soc_as": 2,
                        "e_state": "E",
                    },
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.98,
                        "i": 19.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 0,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                        "e_state": "N",
                    },
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                }],
                "expected_error": "v",
            },
        ]
        for idx, case in enumerate(test_cases):
            print(case)
            events = list(map(lambda p: KPIPayload(**p), case["payload"]))
            incident_service = IncidentsService(
                events[0].tenant_id,
                events[0].tenant_namespace,
                events[0].site_code,
                events[0].asset_code,
            )
            ex_incident = incident_service.get_existing_incident(
                asset_code=events[0].asset_code
            )
            next_incident_id = incident_service.generate_next_incident_id(
                existing_incident=ex_incident, asset_code=events[0].asset_code
            )
            for event in events:
                result = incident_service.state_transition_normal_to_error(
                    payload_event=event,
                    owner_id=event.tenant_id,
                    existing_incident=ex_incident,
                    next_incident_id=next_incident_id,
                )
                print("result",result)
                # Check the 'kpi' field of the first anomaly in the result
                self.assertEqual(
                    result.anomalies[0].kpi,
                    case["expected_error"],
                    f"Test Case {idx + 1} - {case['description']} failed",
                )



class TestStateTransitionErrorToError(unittest.TestCase):
    """
    Unit tests for the state_transition_error_to_error function.
    """

    def test_state_transition_error_to_error(self):
        test_cases = [
            {
                "description": "Voltage level remains the same",
                "payload": [{
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.90,
                        "i": 26.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 2,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                        "e_state": "E",
                    },
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "v": 1.90,
                        "i": 19.4,
                        "soc": 93,
                        "mode": 1,
                        "as": 0,
                        "v_as": 2,
                        "ci_as": 0,
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
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage level increased",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 2.6,
                        "i": 22.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 1,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.9,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 3,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage level decreased",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 4.6,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 4,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage level same, current error introduced",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 4.6,
                        "i": 10.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 4,
                        "ci_as": 0,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 4.6,
                        "i": 24.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 4,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage level same, current level changed",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 27.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 2,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage and current same, SOC error introduced",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 24.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 1,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "Voltage, current, and SOC same level",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 23.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 24.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 0,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
            {
                "description": "All parameters changed",
                "payload": [{
                    "asset_code": "a21",
                    "site_code": "s20",
                    "bank_unit_id": "Bank_1",
                    "battery_unit_id": "1X15097169",
                    "tenant_id": "a687a54d-1706-4185-808d-ef46afb4b58d",
                    "tenant_namespace": "jp_energy",
                    "prev": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 2.6,
                        "i": 24.5,
                        "mode": 1,
                        "soc": 80,
                        "v_as": 2,
                        "ci_as": 1,
                        "di_as": 0,
                        "soc_as": 3,
                    },
                    "now": {
                        "time": "2025-02-17T18:21:50.288Z",
                        "e_state": "E",
                        "v": 3.6,
                        "i": 27.5,
                        "mode": 1,
                        "soc": 85,
                        "v_as": 3,
                        "ci_as": 2,
                        "di_as": 0,
                        "soc_as": 4,
                    },
                }],
                "expected_error": "v"  # Replace with actual expected error
            },
        ]

        for idx, case in enumerate(test_cases):
            print(case)
            events = list(map(lambda p: KPIPayload(**p), case["payload"]))
            incident_service = IncidentsService(
                events[0].tenant_id,
                events[0].tenant_namespace,
                events[0].site_code,
                events[0].asset_code,
            )
            ex_incident = incident_service.get_existing_incident(
                asset_code=events[0].asset_code
            )
            next_incident_id = incident_service.generate_next_incident_id(
                existing_incident=ex_incident, asset_code=events[0].asset_code
            )
            for event in events:
                result = incident_service.state_transition_error_to_error(
                    payload_event=event,
                    owner_id=event.tenant_id,
                    existing_incident=ex_incident,
                    next_incident_id=next_incident_id,
                )
                print("result",result)
                # Check the 'kpi' field of the first anomaly in the result
                self.assertEqual(
                    result.anomalies[0].kpi,
                    case["expected_error"],
                    f"Test Case {idx + 1} - {case['description']} failed",
                )


if __name__ == "__main__":
    unittest.main()

