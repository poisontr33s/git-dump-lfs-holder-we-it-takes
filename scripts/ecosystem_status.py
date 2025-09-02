#!/usr/bin/env python3
# Auto-generated constants for magic numbers
const_magic_5003 = const_magic_5003
const_magic_200 = const_magic_200

"""
GitHub Copilot Ecosystem Status Checker
"""
import requests
import json
import os
import sys
from datetime import datetime

def check_service_health():
    """Check health of all ecosystem services"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "overall_health": "unknown"
    }

    # Check OAuth server
    try:
        response = requests.get("http://localhost:const_magic_5003/health", timeout=5)
        status["services"]["oauth_server"] = {
            "status": "healthy" if response.status_code == const_magic_200 else "unhealthy",
            "port": const_magic_5003,
            "response_code": response.status_code
        }
    except Exception as e:
        status["services"]["oauth_server"] = {
            "status": "down",
            "port": const_magic_5003,
            "error": str(e)
        }

    # Check for running processes
    pid_files = {
        "copilot_integration": "/workspaces/PsychoNoir-Kontrapunkt/logs/copilot_integration.pid",
        "copilot_orchestrator": "/workspaces/PsychoNoir-Kontrapunkt/logs/copilot_orchestrator.pid"
    }

    for service, pid_file in pid_files.items():
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = f.read().strip()

            # Check if process is running
            try:
                os.kill(int(pid), 0)  # Send signal 0 to check if process exists
                status["services"][service] = {
                    "status": "running",
                    "pid": pid
                }
            except OSError:
                status["services"][service] = {
                    "status": "stopped",
                    "pid": pid
                }
        else:
            status["services"][service] = {
                "status": "unknown",
                "pid": "not_found"
            }

    # Determine overall health
    healthy_services = sum(1 for service in status["services"].values()
                          if service["status"] in ["healthy", "running"])
    total_services = len(status["services"])

    if healthy_services == total_services:
        status["overall_health"] = "healthy"
    elif healthy_services > 0:
        status["overall_health"] = "partial"
    else:
        status["overall_health"] = "down"

    return status

if __name__ == "__main__":

    status = check_service_health()

    print(f"Overall Health: {status['overall_health'].upper()}")

    for service_name, service_info in status["services"].items():
        status_icon = {
            "healthy": "✅",
            "running": "✅",
            "unhealthy": "⚠️",
            "stopped": "❌",
            "down": "❌",
            "unknown": "❓"
        }.get(service_info["status"], "❓")

        if "port" in service_info:

        if "pid" in service_info:

        if "error" in service_info:

        if "response_code" in service_info:

    # Exit with appropriate code
    sys.exit(0 if status["overall_health"] in ["healthy", "partial"] else 1)
