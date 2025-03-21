#!/bin/bash
chmod +x *.sh
# Get container up and running
docker-compose -f docker-compose.eval.yml up -d
# Stop the container(s)
docker-compose -f docker-compose.eval.yml down -v
