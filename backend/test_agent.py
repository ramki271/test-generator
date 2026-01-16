#!/usr/bin/env python3.11
"""
Test script for the Test Case Generator Agent
"""
import requests
import json
import sys

def test_agent():
    url = "http://localhost:8000/api/v1/generate-test-cases"

    payload = {
        "manual_input": {
            "title": "User Login Feature",
            "description": "Users should be able to authenticate using email and password",
            "acceptance_criteria": [
                "User can enter email and password",
                "System validates credentials",
                "User is redirected to dashboard on success",
                "Error message shown for invalid credentials"
            ]
        },
        "test_types": ["functional"],
        "include_edge_cases": True,
        "include_negative_tests": True
    }

    print("🚀 Testing Test Case Generator Agent...")
    print(f"📤 Sending request to: {url}")
    print(f"📝 Payload: {json.dumps(payload, indent=2)}\n")

    try:
        response = requests.post(url, json=payload, timeout=180)

        print(f"✅ HTTP Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n🎉 Success! Generated {len(result.get('test_cases', []))} test cases\n")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Error: {response.text}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("⏱️  Request timed out (agent may still be processing)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_agent()
