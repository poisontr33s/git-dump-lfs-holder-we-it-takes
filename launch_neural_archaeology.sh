#!/bin/bash

# PSYCHO-NOIR KONTRAPUNKT: NEURAL ARCHAEOLOGY SYSTEM LAUNCHER
# ===========================================================
# 
# Quick launcher for testing the Neural Archaeology system with your 40+ failed runs
# 
# Usage:
#   ./launch_neural_archaeology.sh full    # Run complete pipeline
#   ./launch_neural_archaeology.sh test    # Run test with sample data
#   ./launch_neural_archaeology.sh quick   # Quick error analysis

set -e

echo "🧠 PSYCHO-NOIR KONTRAPUNKT: NEURAL ARCHAEOLOGY SYSTEM"
echo "======================================================"

# Create necessary directories
mkdir -p data/generert
mkdir -p data/rapporter

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend/python"

MODE=${1:-full}

case $MODE in
    "full")
        echo "🚀 LAUNCHING FULL NEURAL ARCHAEOLOGY PIPELINE..."
        echo "   This will:"
        echo "   1. Harvest your failed runs from GitHub Actions"
        echo "   2. Catalog failures in archaeological database"
        echo "   3. Extract bidirectional learning patterns"
        echo "   4. Generate predictive intelligence"
        echo "   5. Create comprehensive reports"
        echo ""
        
        cd backend/python
        python neural_archaeology_orchestrator.py --mode full
        ;;
        
    "test")
        echo "🧪 RUNNING TEST MODE WITH SAMPLE DATA..."
        
        cd backend/python
        
        # First, run the failure archaeology system to set up database
        echo "Setting up archaeology database..."
        python failure_archaeology_system.py
        
        # Then run the harvester to test GitHub integration
        echo "Testing failure harvesting..."
        python failed_runs_harvester.py
        
        # Finally, test the intelligence engine
        echo "Testing bidirectional intelligence..."
        python bidirectional_intelligence_engine.py
        ;;
        
    "quick")
        if [ -z "$2" ]; then
            echo "❌ Quick mode requires an error signature"
            echo "Usage: $0 quick 'ERROR_SIGNATURE'"
            exit 1
        fi
        
        echo "🔍 QUICK ANALYSIS FOR ERROR: $2"
        
        cd backend/python
        python neural_archaeology_orchestrator.py --mode quick --error "$2"
        ;;
        
    "harvest")
        echo "📡 HARVESTING FAILED RUNS ONLY..."
        
        cd backend/python
        python failed_runs_harvester.py
        ;;
        
    *)
        echo "❌ Unknown mode: $MODE"
        echo "Available modes: full, test, quick, harvest"
        exit 1
        ;;
esac

echo ""
echo "✅ NEURAL ARCHAEOLOGY OPERATION COMPLETE"
echo "📊 Check data/rapporter/ for generated reports"
echo "🗃️ Database location: data/generert/failure_archaeology.db"
