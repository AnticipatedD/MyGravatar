#!/bin/bash
# fetch_offers.sh

# Use an environment variable for the token, falling back to the sandbox key
API_TOKEN="${AON_API_TOKEN:-aon_test_publicSandboxKey01}"

curl -sS -X POST "https://api.aon.pro/v1/offers/query" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "AON-Protocol-Version: 1.0" \
  -H "X-AON-Placement-Id: plc_public_test_sandbox" \
  -d '{
    "intent": {
      "content": [{"type":"input_text","text":"Find productivity tools"}],
      "provenance": "user_expressed"
    },
    "context": {}
  }'
