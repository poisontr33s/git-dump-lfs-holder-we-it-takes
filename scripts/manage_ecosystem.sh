#!/bin/bash
# GitHub Copilot Ecosystem Management Script

WORKSPACE_PATH="/workspaces/PsychoNoir-Kontrapunkt"

case "$1" in
    start)
        echo "🚀 Starting GitHub Copilot Ecosystem..."
        bash "$WORKSPACE_PATH/start_github_copilot_ecosystem.sh"
        ;;
    stop)
        echo "🛑 Stopping GitHub Copilot Ecosystem..."
        
        # Kill all services
        for service in oauth_server copilot_integration copilot_orchestrator; do
            pid_file="$WORKSPACE_PATH/logs/${service}.pid"
            if [ -f "$pid_file" ]; then
                pid=$(cat "$pid_file")
                echo "Stopping $service (PID: $pid)"
                kill $pid 2>/dev/null
                rm "$pid_file"
            fi
        done
        
        # Kill any remaining processes on our ports
        lsof -ti:5003 | xargs -r kill -9
        
        echo "✅ Ecosystem stopped"
        ;;
    restart)
        echo "🔄 Restarting GitHub Copilot Ecosystem..."
        "$0" stop
        sleep 3
        "$0" start
        ;;
    status)
        python3 "$WORKSPACE_PATH/scripts/ecosystem_status.py"
        ;;
    logs)
        service=${2:-oauth_server}
        log_file="$WORKSPACE_PATH/logs/${service}.log"
        if [ -f "$log_file" ]; then
            echo "📋 Showing logs for $service:"
            tail -f "$log_file"
        else
            echo "❌ Log file not found: $log_file"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs [service]}"
        echo ""
        echo "Services: oauth_server, copilot_integration, copilot_orchestrator"
        exit 1
        ;;
esac
