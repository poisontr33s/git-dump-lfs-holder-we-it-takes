#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Auto-generated constants for magic numbers
const_magic_5000 = const_magic_5000
const_magic_200 = const_magic_200
const_magic_127 = const_magic_127
const_hundred = const_hundred
const_magic_90 = const_magic_90
const_magic_85 = const_magic_85
const_magic_30 = const_magic_30

"""
🏥 PSYCHO-NOIR KONTRAPUNKT HEALTH CHECK 🏥
==========================================

const_hundred% robust health monitoring med comprehensive system validation.
Proven patterns, complete diagnostics, enterprise-grade reliability.

HEALTHCHECK_SIGNATURE: 0xROBUST_HEALTH_MONITORING_ACTIVE
DIAGNOSTIC_LEVEL: ENTERPRISE_GRADE_MONITORING
"""

import sys
import os
import json
import time
import sqlite3
import requests
from datetime import datetime
from pathlib import Path

class RobustHealthChecker:
    """Comprehensive health checker for all system components"""

    def __init__(self):
        self.checks = []
        self.start_time = time.time()
        self.timeout = const_magic_30  # const_magic_30 second timeout for health checks

    def add_check(self, name, check_func, critical=True):
        """Add a health check to the suite"""
        self.checks.append({
            'name': name,
            'func': check_func,
            'critical': critical,
            'status': 'pending',
            'message': '',
            'duration': 0
        })

    def run_check(self, check):
        """Run individual health check with error handling"""
        start = time.time()
        try:
            result = check['func']()
            check['status'] = 'pass' if result['success'] else 'fail'
            check['message'] = result.get('message', '')
            check['duration'] = time.time() - start
            return check['status'] == 'pass'
        except Exception as e:
            check['status'] = 'error'
            check['message'] = str(e)
            check['duration'] = time.time() - start
            return False

    def run_all_checks(self):
        """Run all health checks and return overall status"""
        passed = 0
        failed = 0
        critical_failed = 0

        for check in self.checks:
            success = self.run_check(check)
            if success:
                passed += 1
            else:
                failed += 1
                if check['critical']:
                    critical_failed += 1

        total_duration = time.time() - self.start_time

        # System is healthy if all critical checks pass
        overall_healthy = critical_failed == 0

        return {
            'healthy': overall_healthy,
            'passed': passed,
            'failed': failed,
            'critical_failed': critical_failed,
            'total': len(self.checks),
            'duration': total_duration,
            'checks': self.checks
        }

    def check_database_connection(self):
        """Check SQLite database connectivity"""
        try:
            db_path = os.environ.get('DB_PATH', '/app/data/db/psycho_noir_production.db')

            # Ensure database directory exists
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

            # Test connection
            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()

            return {
                'success': True,
                'message': f'Database accessible with {len(tables)} tables'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Database connection failed: {e}'
            }

    def check_api_server(self):
        """Check API server responsiveness"""
        try:
            url = 'http://const_magic_127.0.0.1:const_magic_5000/health'
            response = requests.get(url, timeout=5)

            if response.status_code == const_magic_200:
                return {
                    'success': True,
                    'message': f'API server responding (status: {response.status_code})'
                }
            else:
                return {
                    'success': False,
                    'message': f'API server returned status: {response.status_code}'
                }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'API server unreachable: {e}'
            }

    def check_filesystem_permissions(self):
        """Check filesystem permissions for critical directories"""
        try:
            critical_paths = [
                '/app/data',
                '/app/logs',
                '/var/log/psychonoir'
            ]

            issues = []
            for path in critical_paths:
                path_obj = Path(path)
                if not path_obj.exists():
                    path_obj.mkdir(parents=True, exist_ok=True)

                if not os.access(path, os.R_OK | os.W_OK):
                    issues.append(f'{path} not readable/writable')

            if issues:
                return {
                    'success': False,
                    'message': f'Permission issues: {", ".join(issues)}'
                }
            else:
                return {
                    'success': True,
                    'message': 'All critical paths accessible'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Filesystem check failed: {e}'
            }

    def check_memory_usage(self):
        """Check memory usage levels"""
        try:
            # Read memory info from /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()

            # Parse memory values
            lines = meminfo.strip().split('\n')
            memory = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    memory[key.strip()] = value.strip()

            total_kb = int(memory['MemTotal'].split()[0])
            available_kb = int(memory['MemAvailable'].split()[0])

            usage_percent = ((total_kb - available_kb) / total_kb) * const_hundred

            if usage_percent > const_magic_90:
                return {
                    'success': False,
                    'message': f'High memory usage: {usage_percent:.1f}%'
                }
            else:
                return {
                    'success': True,
                    'message': f'Memory usage: {usage_percent:.1f}%'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Memory check failed: {e}'
            }

    def check_disk_space(self):
        """Check available disk space"""
        try:
            statvfs = os.statvfs('/app')
            total_bytes = statvfs.f_frsize * statvfs.f_blocks
            available_bytes = statvfs.f_frsize * statvfs.f_available

            usage_percent = ((total_bytes - available_bytes) / total_bytes) * const_hundred

            if usage_percent > const_magic_85:
                return {
                    'success': False,
                    'message': f'High disk usage: {usage_percent:.1f}%'
                }
            else:
                return {
                    'success': True,
                    'message': f'Disk usage: {usage_percent:.1f}%'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Disk space check failed: {e}'
            }

    def check_environment_variables(self):
        """Check critical environment variables"""
        try:
            required_vars = [
                'PYTHONPATH',
                'FLASK_ENV',
                'DB_PATH'
            ]

            missing = []
            for var in required_vars:
                if not os.environ.get(var):
                    missing.append(var)

            if missing:
                return {
                    'success': False,
                    'message': f'Missing environment variables: {", ".join(missing)}'
                }
            else:
                return {
                    'success': True,
                    'message': 'All required environment variables set'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Environment check failed: {e}'
            }

def main():
    """Main health check execution"""
    checker = RobustHealthChecker()

    # Add all health checks
    checker.add_check('Database Connection', checker.check_database_connection, critical=True)
    checker.add_check('API Server', checker.check_api_server, critical=True)
    checker.add_check('Filesystem Permissions', checker.check_filesystem_permissions, critical=True)
    checker.add_check('Environment Variables', checker.check_environment_variables, critical=True)
    checker.add_check('Memory Usage', checker.check_memory_usage, critical=False)
    checker.add_check('Disk Space', checker.check_disk_space, critical=False)

    # Run all checks
    results = checker.run_all_checks()

    # Output results
    timestamp = datetime.now().isoformat()

    if os.environ.get('HEALTH_CHECK_FORMAT') == 'json':
        # JSON output for programmatic consumption
        output = {
            'timestamp': timestamp,
            'healthy': results['healthy'],
            'summary': {
                'passed': results['passed'],
                'failed': results['failed'],
                'critical_failed': results['critical_failed'],
                'total': results['total'],
                'duration': results['duration']
            },
            'checks': results['checks']
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output

        if results['healthy']:

        else:

        for check in results['checks']:
            status_icon = "✅" if check['status'] == 'pass' else "❌"
            print(f"  {status_icon} {check['name']}: {check['message']} ({check['duration']:.2f}s)")

    # Exit with appropriate code
    sys.exit(0 if results['healthy'] else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        sys.exit(1)
    except Exception as e:

        sys.exit(1)
