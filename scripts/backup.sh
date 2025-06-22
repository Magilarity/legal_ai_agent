#!/bin/bash
# Backup PostgreSQL database
pg_dump $DATABASE_URL -F c -b -v -f /backups/backup_$(date +%F).dump
