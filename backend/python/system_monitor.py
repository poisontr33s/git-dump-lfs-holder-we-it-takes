#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 PSYCHO-NOIR KONTRAPUNKT SYSTEM MONITOR 📊
=============================================

100% robust real-time monitoring med comprehensive metrics collection.
Proven patterns, intelligent alerting, enterprise-grade observability.

MONITOR_SIGNATURE: 0xROBUST_SYSTEM_MONITORING_ACTIVE
OBSERVABILITY_LEVEL: ENTERPRISE_GRADE_MONITORING
"""

import os
import sys
import json
import time
import psutil
import sqlite3
import requests
from datetime import datetime, timedelta
from pathlib import Path
import logging
import threading

class RobustSystemMonitor:
    """Comprehensive system monitoring service"""

    def __init__(self):
        self.monitor_interval = int(os.environ.get('MONITOR_INTERVAL', '30'))  # seconds
        self.alert_thresholds = {
            'cpu_percent': float(os.environ.get('CPU_ALERT_THRESHOLD', '80.0')),
            'memory_percent': float(os.environ.get('MEMORY_ALERT_THRESHOLD', '85.0')),
            'disk_percent': float(os.environ.get('DISK_ALERT_THRESHOLD', '90.0')),
            'response_time_ms': float(os.environ.get('RESPONSE_TIME_THRESHOLD', '5000.0'))
        }

        self.metrics_db_path = Path(os.environ.get('METRICS_DB', '/app/data/db/metrics.db'))
        self.log_dir = Path('/var/log/psychonoir')
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Initialize metrics database
        self._init_metrics_db()

        # Monitoring state
        self.running = False
        self.alert_cooldown = {}  # Prevent alert spam

    def _init_metrics_db(self):
        """Initialize metrics database schema"""
        try:
            self.metrics_db_path.parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(str(self.metrics_db_path))
            cursor = conn.cursor()

            # System metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    cpu_percent REAL,
                    memory_percent REAL,
                    memory_used_mb REAL,
                    memory_total_mb REAL,
                    disk_percent REAL,
                    disk_used_gb REAL,
                    disk_total_gb REAL,
                    load_average_1m REAL,
                    load_average_5m REAL,
                    load_average_15m REAL,
                    network_bytes_sent INTEGER,
                    network_bytes_recv INTEGER
                )
            ''')

            # Application metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    service_name TEXT,
                    status TEXT,
                    response_time_ms REAL,
                    error_count INTEGER,
                    active_connections INTEGER,
                    memory_usage_mb REAL
                )
            ''')

            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    alert_type TEXT,
                    severity TEXT,
                    message TEXT,
                    metric_value REAL,
                    threshold_value REAL,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolved_timestamp DATETIME
                )
            ''')

            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_app_metrics_timestamp ON app_metrics(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)')

            conn.commit()
            conn.close()

            self.logger.info("📊 Metrics database initialized")

        except Exception as e:
            self.logger.error(f"❌ Metrics database initialization failed: {e}")

    def collect_system_metrics(self):
        """Collect comprehensive system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            load_avg = os.getloadavg()

            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_total_mb = memory.total / (1024 * 1024)

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_gb = disk.used / (1024 * 1024 * 1024)
            disk_total_gb = disk.total / (1024 * 1024 * 1024)

            # Network metrics
            network = psutil.net_io_counters()

            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_used_mb': memory_used_mb,
                'memory_total_mb': memory_total_mb,
                'disk_percent': disk_percent,
                'disk_used_gb': disk_used_gb,
                'disk_total_gb': disk_total_gb,
                'load_average_1m': load_avg[0],
                'load_average_5m': load_avg[1],
                'load_average_15m': load_avg[2],
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv
            }

            # Store metrics in database
            self._store_system_metrics(metrics)

            # Check for alerts
            self._check_system_alerts(metrics)

            return metrics

        except Exception as e:
            self.logger.error(f"❌ System metrics collection failed: {e}")
            return None

    def collect_app_metrics(self):
        """Collect application-specific metrics"""
        app_metrics = []

        # Monitor API service
        api_metrics = self._monitor_api_service()
        if api_metrics:
            app_metrics.append(api_metrics)

        # Monitor database
        db_metrics = self._monitor_database()
        if db_metrics:
            app_metrics.append(db_metrics)

        # Store all app metrics
        for metrics in app_metrics:
            self._store_app_metrics(metrics)
            self._check_app_alerts(metrics)

        return app_metrics

    def _monitor_api_service(self):
        """Monitor API service health and performance"""
        try:
            start_time = time.time()

            # Health check request
            response = requests.get('http://localhost:5000/health', timeout=10)
            response_time_ms = (time.time() - start_time) * 1000

            # Get process information
            api_process = None
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'gunicorn' in cmdline and 'psycho_noir_api' in cmdline:
                        api_process = proc
                        break
                except:
                    continue

            memory_usage_mb = 0
            if api_process:
                try:
                    memory_usage_mb = api_process.memory_info().rss / (1024 * 1024)
                except:
                    pass

            return {
                'service_name': 'psychonoir_api',
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time_ms': response_time_ms,
                'error_count': 0 if response.status_code == 200 else 1,
                'active_connections': 0,  # Would need more sophisticated monitoring
                'memory_usage_mb': memory_usage_mb
            }

        except Exception as e:
            self.logger.warning(f"⚠️ API monitoring failed: {e}")
            return {
                'service_name': 'psychonoir_api',
                'status': 'error',
                'response_time_ms': 0,
                'error_count': 1,
                'active_connections': 0,
                'memory_usage_mb': 0
            }

    def _monitor_database(self):
        """Monitor database performance"""
        try:
            db_path = os.environ.get('DB_PATH', '/app/data/db/psycho_noir_production.db')

            if not Path(db_path).exists():
                return None

            start_time = time.time()

            # Simple query to test responsiveness
            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()

            response_time_ms = (time.time() - start_time) * 1000

            # Get database file size
            db_size_mb = Path(db_path).stat().st_size / (1024 * 1024)

            return {
                'service_name': 'psychonoir_database',
                'status': 'healthy',
                'response_time_ms': response_time_ms,
                'error_count': 0,
                'active_connections': 1,  # SQLite is single-connection
                'memory_usage_mb': db_size_mb
            }

        except Exception as e:
            self.logger.warning(f"⚠️ Database monitoring failed: {e}")
            return {
                'service_name': 'psychonoir_database',
                'status': 'error',
                'response_time_ms': 0,
                'error_count': 1,
                'active_connections': 0,
                'memory_usage_mb': 0
            }

    def _store_system_metrics(self, metrics):
        """Store system metrics in database"""
        try:
            conn = sqlite3.connect(str(self.metrics_db_path))
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO system_metrics (
                    cpu_percent, memory_percent, memory_used_mb, memory_total_mb,
                    disk_percent, disk_used_gb, disk_total_gb,
                    load_average_1m, load_average_5m, load_average_15m,
                    network_bytes_sent, network_bytes_recv
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics['cpu_percent'], metrics['memory_percent'],
                metrics['memory_used_mb'], metrics['memory_total_mb'],
                metrics['disk_percent'], metrics['disk_used_gb'], metrics['disk_total_gb'],
                metrics['load_average_1m'], metrics['load_average_5m'], metrics['load_average_15m'],
                metrics['network_bytes_sent'], metrics['network_bytes_recv']
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"❌ Failed to store system metrics: {e}")

    def _store_app_metrics(self, metrics):
        """Store application metrics in database"""
        try:
            conn = sqlite3.connect(str(self.metrics_db_path))
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO app_metrics (
                    service_name, status, response_time_ms, error_count,
                    active_connections, memory_usage_mb
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                metrics['service_name'], metrics['status'], metrics['response_time_ms'],
                metrics['error_count'], metrics['active_connections'], metrics['memory_usage_mb']
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"❌ Failed to store app metrics: {e}")

    def _check_system_alerts(self, metrics):
        """Check system metrics against alert thresholds"""
        alerts = []

        # CPU alert
        if metrics['cpu_percent'] > self.alert_thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'warning' if metrics['cpu_percent'] < 95 else 'critical',
                'message': f"High CPU usage: {metrics['cpu_percent']:.1f}%",
                'value': metrics['cpu_percent'],
                'threshold': self.alert_thresholds['cpu_percent']
            })

        # Memory alert
        if metrics['memory_percent'] > self.alert_thresholds['memory_percent']:
            alerts.append({
                'type': 'memory_high',
                'severity': 'warning' if metrics['memory_percent'] < 95 else 'critical',
                'message': f"High memory usage: {metrics['memory_percent']:.1f}%",
                'value': metrics['memory_percent'],
                'threshold': self.alert_thresholds['memory_percent']
            })

        # Disk alert
        if metrics['disk_percent'] > self.alert_thresholds['disk_percent']:
            alerts.append({
                'type': 'disk_high',
                'severity': 'warning' if metrics['disk_percent'] < 95 else 'critical',
                'message': f"High disk usage: {metrics['disk_percent']:.1f}%",
                'value': metrics['disk_percent'],
                'threshold': self.alert_thresholds['disk_percent']
            })

        # Process alerts
        for alert in alerts:
            self._process_alert(alert)

    def _check_app_alerts(self, metrics):
        """Check application metrics against alert thresholds"""
        alerts = []

        # Service status alert
        if metrics['status'] != 'healthy':
            alerts.append({
                'type': 'service_unhealthy',
                'severity': 'critical',
                'message': f"Service {metrics['service_name']} is {metrics['status']}",
                'value': 0,
                'threshold': 1
            })

        # Response time alert
        if metrics['response_time_ms'] > self.alert_thresholds['response_time_ms']:
            alerts.append({
                'type': 'response_time_high',
                'severity': 'warning',
                'message': f"High response time for {metrics['service_name']}: {metrics['response_time_ms']:.1f}ms",
                'value': metrics['response_time_ms'],
                'threshold': self.alert_thresholds['response_time_ms']
            })

        # Process alerts
        for alert in alerts:
            self._process_alert(alert)

    def _process_alert(self, alert):
        """Process and store alert"""
        alert_key = f"{alert['type']}_{alert.get('service_name', 'system')}"
        current_time = time.time()

        # Check cooldown to prevent spam
        if alert_key in self.alert_cooldown:
            if current_time - self.alert_cooldown[alert_key] < 300:  # 5 minute cooldown
                return

        self.alert_cooldown[alert_key] = current_time

        try:
            # Store alert in database
            conn = sqlite3.connect(str(self.metrics_db_path))
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO alerts (alert_type, severity, message, metric_value, threshold_value)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                alert['type'], alert['severity'], alert['message'],
                alert['value'], alert['threshold']
            ))

            conn.commit()
            conn.close()

            # Log alert
            log_func = self.logger.critical if alert['severity'] == 'critical' else self.logger.warning
            log_func(f"🚨 ALERT: {alert['message']}")

        except Exception as e:
            self.logger.error(f"❌ Failed to process alert: {e}")

    def start_monitoring(self):
        """Start the monitoring service"""
        self.logger.info("🚀 Starting Psycho-Noir Kontrapunkt system monitor")
        self.running = True

        while self.running:
            try:
                # Collect metrics
                system_metrics = self.collect_system_metrics()
                app_metrics = self.collect_app_metrics()

                if system_metrics:
                    self.logger.debug(f"📊 System: CPU {system_metrics['cpu_percent']:.1f}%, "
                                    f"MEM {system_metrics['memory_percent']:.1f}%, "
                                    f"DISK {system_metrics['disk_percent']:.1f}%")

                # Clean up old metrics (keep last 7 days)
                self._cleanup_old_metrics()

                # Wait for next interval
                time.sleep(self.monitor_interval)

            except KeyboardInterrupt:
                self.logger.info("🛑 Monitor interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Monitoring error: {e}")
                time.sleep(5)  # Short sleep before retry

        self.running = False
        self.logger.info("✅ Monitoring service stopped")

    def stop_monitoring(self):
        """Stop the monitoring service"""
        self.running = False

    def _cleanup_old_metrics(self):
        """Clean up old metrics data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=7)

            conn = sqlite3.connect(str(self.metrics_db_path))
            cursor = conn.cursor()

            # Clean up old system metrics
            cursor.execute("DELETE FROM system_metrics WHERE timestamp < ?", (cutoff_date,))

            # Clean up old app metrics
            cursor.execute("DELETE FROM app_metrics WHERE timestamp < ?", (cutoff_date,))

            # Clean up resolved alerts older than 30 days
            alert_cutoff = datetime.now() - timedelta(days=30)
            cursor.execute("DELETE FROM alerts WHERE resolved = TRUE AND resolved_timestamp < ?", (alert_cutoff,))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"❌ Metrics cleanup failed: {e}")

def main():
    """Main monitoring service execution"""
    monitor = RobustSystemMonitor()

    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        monitor.stop_monitoring()
    except Exception as e:

        sys.exit(1)

if __name__ == "__main__":
    main()
