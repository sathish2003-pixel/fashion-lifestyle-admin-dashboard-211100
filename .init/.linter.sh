#!/bin/bash
cd /home/kavia/workspace/code-generation/fashion-lifestyle-admin-dashboard-211100/admin_dashboard_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

