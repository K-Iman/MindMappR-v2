#!/usr/bin/env python
"""
Local PostgreSQL Database Backup Script
---------------------------------------
Runs pg_dump against the local native PostgreSQL instance and saves a timestamped SQL file in the /backups directory.
Uses PGPASSWORD environment variable so pg_dump executes non-interactively without prompt hanging.
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / 'backups'

def run_backup():
    # Ensure backups directory exists
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Read connection info from environment variables or use local defaults
    db_name = os.environ.get('DB_NAME', 'mindmappr_db')
    db_user = os.environ.get('DB_USER', 'mindmappr_user')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '5432')

    # Generate timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{db_name}_{timestamp}.sql"
    backup_path = BACKUP_DIR / backup_filename

    # Locate pg_dump binary
    pg_dump_bin = shutil.which('pg_dump')
    if not pg_dump_bin:
        # Fallback check for standard Windows PostgreSQL installation paths
        common_win_paths = [
            r"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe",
            r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe",
            r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe",
        ]
        for path in common_win_paths:
            if os.path.exists(path):
                pg_dump_bin = path
                break

    if not pg_dump_bin:
        print("ERROR: 'pg_dump' executable not found on PATH or standard PostgreSQL installation paths.")
        print("Please ensure PostgreSQL bin directory (e.g. C:\\Program Files\\PostgreSQL\\18\\bin) is added to your PATH.")
        sys.exit(1)

    cmd = [
        pg_dump_bin,
        '-h', db_host,
        '-p', str(db_port),
        '-U', db_user,
        '-d', db_name,
        '-f', str(backup_path)
    ]

    print(f"Creating local PostgreSQL backup for database '{db_name}'...")
    print(f"Target file: {backup_path}")

    # Pass PGPASSWORD via environment so pg_dump runs non-interactively
    env = os.environ.copy()
    if db_password:
        env['PGPASSWORD'] = db_password

    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        print("SUCCESS: Local database backup completed successfully!")
        print(f"Backup saved to: {backup_path}")
    except subprocess.CalledProcessError as e:
        print("ERROR: pg_dump failed with exit code", e.returncode)
        print("pg_dump stderr:", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to run backup script: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_backup()
