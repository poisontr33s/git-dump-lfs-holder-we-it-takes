#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 PSYCHO-NOIR KONTRAPUNKT DATABASE MAINTENANCE 🔧
===================================================

100% robust database maintenance med comprehensive optimization.
Proven patterns, automated cleanup, enterprise-grade performance.

MAINTENANCE_SIGNATURE: 0xROBUST_DATABASE_MAINTENANCE_ACTIVE
OPTIMIZATION_LEVEL: ENTERPRISE_GRADE_PERFORMANCE
"""

import os
import sys
import sqlite3
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

class RobustDatabaseMaintenance:
    """Comprehensive database maintenance service"""
    
    def __init__(self):
        self.db_paths = [
            Path(os.environ.get('DB_PATH', '/app/data/db/psycho_noir_production.db')),
            Path('/app/data/db/metrics.db'),
            Path('/app/data/db/psycho_noir_cli.db'),
            Path('/app/data/db/psycho_noir_portal.db')
        ]
        
        self.backup_dir = Path('/app/data/db/backups')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.maintenance_interval = int(os.environ.get('MAINTENANCE_INTERVAL', '3600'))  # 1 hour
        self.vacuum_threshold_mb = int(os.environ.get('VACUUM_THRESHOLD_MB', '100'))
        
        # Configure logging
        log_dir = Path('/var/log/psychonoir')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'maintenance.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_maintenance_cycle(self):
        """Run complete maintenance cycle for all databases"""
        self.logger.info("🔧 Starting database maintenance cycle")
        
        maintenance_results = {}
        
        for db_path in self.db_paths:
            if db_path.exists():
                try:
                    self.logger.info(f"🔧 Maintaining database: {db_path.name}")
                    
                    # Run maintenance operations
                    result = self._maintain_database(db_path)
                    maintenance_results[str(db_path)] = result
                    
                    self.logger.info(f"✅ Maintenance completed for {db_path.name}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Maintenance failed for {db_path.name}: {e}")
                    maintenance_results[str(db_path)] = {'success': False, 'error': str(e)}
            else:
                self.logger.info(f"⏭️ Database not found, skipping: {db_path.name}")
                
        self.logger.info("✅ Database maintenance cycle completed")
        return maintenance_results
        
    def _maintain_database(self, db_path):
        """Perform maintenance operations on a single database"""
        maintenance_result = {
            'success': True,
            'operations': [],
            'size_before_mb': 0,
            'size_after_mb': 0,
            'performance_improvement': {},
            'errors': []
        }
        
        try:
            # Get initial size
            maintenance_result['size_before_mb'] = db_path.stat().st_size / (1024 * 1024)
            
            # Create backup before maintenance
            backup_result = self._create_maintenance_backup(db_path)
            if backup_result['success']:
                maintenance_result['operations'].append('backup_created')
            else:
                maintenance_result['errors'].append(f"Backup failed: {backup_result['error']}")
                
            # Connect to database
            conn = sqlite3.connect(str(db_path), timeout=30)
            conn.execute("PRAGMA busy_timeout = 30000")  # 30 second timeout
            
            try:
                # 1. Integrity check
                integrity_result = self._check_integrity(conn)
                maintenance_result['operations'].append('integrity_check')
                if not integrity_result['success']:
                    maintenance_result['errors'].append(f"Integrity check failed: {integrity_result['error']}")
                    
                # 2. Analyze database statistics
                stats_before = self._analyze_database_stats(conn)
                
                # 3. Cleanup old data
                cleanup_result = self._cleanup_old_data(conn, db_path)
                if cleanup_result['success']:
                    maintenance_result['operations'].append('data_cleanup')
                    maintenance_result['performance_improvement']['rows_deleted'] = cleanup_result['rows_deleted']
                else:
                    maintenance_result['errors'].append(f"Cleanup failed: {cleanup_result['error']}")
                    
                # 4. Optimize database structure
                optimize_result = self._optimize_database(conn)
                if optimize_result['success']:
                    maintenance_result['operations'].append('optimization')
                else:
                    maintenance_result['errors'].append(f"Optimization failed: {optimize_result['error']}")
                    
                # 5. Vacuum if necessary
                if maintenance_result['size_before_mb'] > self.vacuum_threshold_mb:
                    vacuum_result = self._vacuum_database(conn)
                    if vacuum_result['success']:
                        maintenance_result['operations'].append('vacuum')
                        maintenance_result['performance_improvement']['space_reclaimed_mb'] = vacuum_result['space_reclaimed_mb']
                    else:
                        maintenance_result['errors'].append(f"Vacuum failed: {vacuum_result['error']}")
                        
                # 6. Update statistics
                stats_result = self._update_statistics(conn)
                if stats_result['success']:
                    maintenance_result['operations'].append('statistics_update')
                else:
                    maintenance_result['errors'].append(f"Statistics update failed: {stats_result['error']}")
                    
                # 7. Analyze performance improvement
                stats_after = self._analyze_database_stats(conn)
                maintenance_result['performance_improvement']['query_performance'] = self._compare_performance(stats_before, stats_after)
                
            finally:
                conn.close()
                
            # Get final size
            maintenance_result['size_after_mb'] = db_path.stat().st_size / (1024 * 1024)
            
            # Calculate space savings
            space_saved = maintenance_result['size_before_mb'] - maintenance_result['size_after_mb']
            maintenance_result['performance_improvement']['space_saved_mb'] = space_saved
            
            return maintenance_result
            
        except Exception as e:
            maintenance_result['success'] = False
            maintenance_result['errors'].append(str(e))
            return maintenance_result
            
    def _create_maintenance_backup(self, db_path):
        """Create backup before maintenance"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"{db_path.stem}_maintenance_{timestamp}.db"
            
            shutil.copy2(db_path, backup_path)
            
            return {
                'success': True,
                'backup_path': str(backup_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def _check_integrity(self, conn):
        """Check database integrity"""
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result == 'ok':
                return {'success': True}
            else:
                return {'success': False, 'error': result}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _analyze_database_stats(self, conn):
        """Analyze database statistics for performance comparison"""
        try:
            cursor = conn.cursor()
            
            # Get page count and size info
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA freelist_count")
            freelist_count = cursor.fetchone()[0]
            
            # Get table statistics
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            table_stats = {}
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM '{table}'")
                    row_count = cursor.fetchone()[0]
                    table_stats[table] = row_count
                except:
                    table_stats[table] = 0
                    
            return {
                'page_count': page_count,
                'page_size': page_size,
                'freelist_count': freelist_count,
                'total_size_bytes': page_count * page_size,
                'free_space_bytes': freelist_count * page_size,
                'table_stats': table_stats
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️ Database stats analysis failed: {e}")
            return {}
            
    def _cleanup_old_data(self, conn, db_path):
        """Clean up old data based on database type and retention policies"""
        try:
            total_deleted = 0
            cursor = conn.cursor()
            
            # Determine cleanup strategy based on database
            if 'metrics' in db_path.name:
                # Clean metrics older than 30 days
                cutoff_date = datetime.now() - timedelta(days=30)
                
                # Clean system metrics
                cursor.execute("DELETE FROM system_metrics WHERE timestamp < ?", (cutoff_date,))
                deleted_system = cursor.rowcount
                
                # Clean app metrics
                cursor.execute("DELETE FROM app_metrics WHERE timestamp < ?", (cutoff_date,))
                deleted_app = cursor.rowcount
                
                # Clean resolved alerts older than 90 days
                alert_cutoff = datetime.now() - timedelta(days=90)
                cursor.execute("DELETE FROM alerts WHERE resolved = TRUE AND resolved_timestamp < ?", (alert_cutoff,))
                deleted_alerts = cursor.rowcount
                
                total_deleted = deleted_system + deleted_app + deleted_alerts
                
            elif 'production' in db_path.name:
                # Clean old interactions
                interaction_cutoff = datetime.now() - timedelta(days=90)
                cursor.execute("DELETE FROM interactions WHERE timestamp < ?", (interaction_cutoff,))
                total_deleted += cursor.rowcount
                
                # Clean old events
                cursor.execute("DELETE FROM events WHERE timestamp < ?", (interaction_cutoff,))
                total_deleted += cursor.rowcount
                
            # Commit changes
            conn.commit()
            
            return {
                'success': True,
                'rows_deleted': total_deleted
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def _optimize_database(self, conn):
        """Optimize database structure and indexes"""
        try:
            cursor = conn.cursor()
            
            # Rebuild indexes
            cursor.execute("REINDEX")
            
            # Optimize query planner
            cursor.execute("ANALYZE")
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _vacuum_database(self, conn):
        """Vacuum database to reclaim space"""
        try:
            # Get size before vacuum
            cursor = conn.cursor()
            cursor.execute("PRAGMA page_count")
            pages_before = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            size_before = pages_before * page_size
            
            # Perform vacuum
            cursor.execute("VACUUM")
            
            # Get size after vacuum
            cursor.execute("PRAGMA page_count")
            pages_after = cursor.fetchone()[0]
            size_after = pages_after * page_size
            
            space_reclaimed_mb = (size_before - size_after) / (1024 * 1024)
            
            return {
                'success': True,
                'space_reclaimed_mb': space_reclaimed_mb
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _update_statistics(self, conn):
        """Update database statistics for query optimization"""
        try:
            cursor = conn.cursor()
            cursor.execute("ANALYZE")
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _compare_performance(self, stats_before, stats_after):
        """Compare performance statistics"""
        if not stats_before or not stats_after:
            return {}
            
        try:
            free_space_reduction = stats_before.get('freelist_count', 0) - stats_after.get('freelist_count', 0)
            total_size_reduction = stats_before.get('total_size_bytes', 0) - stats_after.get('total_size_bytes', 0)
            
            return {
                'free_pages_reduced': free_space_reduction,
                'total_size_reduced_bytes': total_size_reduction,
                'fragmentation_improved': free_space_reduction > 0
            }
            
        except Exception:
            return {}
            
    def cleanup_old_backups(self):
        """Clean up old maintenance backups"""
        try:
            cutoff_date = datetime.now() - timedelta(days=7)
            removed_count = 0
            
            for backup_file in self.backup_dir.glob('*_maintenance_*.db'):
                try:
                    file_modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    if file_modified < cutoff_date:
                        backup_file.unlink()
                        removed_count += 1
                        self.logger.info(f"🗑️ Removed old maintenance backup: {backup_file.name}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to remove backup: {backup_file} - {e}")
                    
            self.logger.info(f"✅ Backup cleanup completed: {removed_count} old backups removed")
            
        except Exception as e:
            self.logger.error(f"❌ Backup cleanup failed: {e}")
            
    def run_continuous_maintenance(self):
        """Run continuous maintenance service"""
        self.logger.info("🚀 Starting continuous database maintenance service")
        
        try:
            while True:
                # Run maintenance cycle
                self.run_maintenance_cycle()
                
                # Clean up old backups
                self.cleanup_old_backups()
                
                # Wait for next cycle
                self.logger.info(f"⏰ Waiting {self.maintenance_interval} seconds for next maintenance cycle")
                time.sleep(self.maintenance_interval)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Maintenance service interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Maintenance service error: {e}")
            
    def generate_maintenance_report(self):
        """Generate comprehensive maintenance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'databases': {},
            'summary': {
                'total_databases': 0,
                'healthy_databases': 0,
                'total_size_mb': 0,
                'maintenance_recommendations': []
            }
        }
        
        for db_path in self.db_paths:
            if db_path.exists():
                try:
                    size_mb = db_path.stat().st_size / (1024 * 1024)
                    
                    # Quick health check
                    conn = sqlite3.connect(str(db_path), timeout=5)
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA integrity_check")
                    integrity = cursor.fetchone()[0]
                    conn.close()
                    
                    db_info = {
                        'size_mb': size_mb,
                        'healthy': integrity == 'ok',
                        'last_modified': datetime.fromtimestamp(db_path.stat().st_mtime).isoformat()
                    }
                    
                    report['databases'][db_path.name] = db_info
                    report['summary']['total_databases'] += 1
                    report['summary']['total_size_mb'] += size_mb
                    
                    if db_info['healthy']:
                        report['summary']['healthy_databases'] += 1
                        
                    # Add recommendations
                    if size_mb > self.vacuum_threshold_mb:
                        report['summary']['maintenance_recommendations'].append(
                            f"Consider vacuum for {db_path.name} (size: {size_mb:.1f} MB)"
                        )
                        
                except Exception as e:
                    report['databases'][db_path.name] = {
                        'error': str(e),
                        'healthy': False
                    }
                    
        return report

def main():
    """Main maintenance service execution"""
    maintenance = RobustDatabaseMaintenance()
    
    # Determine operation mode
    operation = os.environ.get('MAINTENANCE_OPERATION', 'continuous')
    
    if operation == 'continuous':
        maintenance.run_continuous_maintenance()
    elif operation == 'single':
        results = maintenance.run_maintenance_cycle()
        print(f"✅ Maintenance completed: {len(results)} databases processed")
    elif operation == 'report':
        report = maintenance.generate_maintenance_report()
        print(json.dumps(report, indent=2))
    else:
        print(f"❌ Unknown operation: {operation}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Database maintenance interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Database maintenance failed: {e}")
        sys.exit(1)
