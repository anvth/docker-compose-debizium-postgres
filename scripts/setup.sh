#!/usr/bin/env bash

echo "Spinning up kafka eco system"
./scripts/setup_infra.sh

echo "Wait for setup to finish"
sleep 30

echo "Add connectors"
./scripts/add_connector.sh
