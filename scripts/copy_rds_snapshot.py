#!/usr/bin/env python3
"""
Task 5: Copy Latest RDS Snapshot to ap-south-2 (Hyderabad)
"""
import boto3
import sys
from datetime import datetime

SOURCE_REGION = "ap-south-1"      # Mumbai
DEST_REGION = "ap-south-2"        # Hyderabad
DB_INSTANCE_ID = "icloudems-rds-mysql"

def copy_latest_snapshot():
    rds_source = boto3.client("rds", region_name=SOURCE_REGION)
    rds_dest = boto3.client("rds", region_name=DEST_REGION)

    print(f"[*] Fetching snapshots for '{DB_INSTANCE_ID}' in {SOURCE_REGION}...")
    response = rds_source.describe_db_snapshots(
        DBInstanceIdentifier=DB_INSTANCE_ID,
        SnapshotType="automated"
    )
    snapshots = response.get("DBSnapshots", [])
    if not snapshots:
        response = rds_source.describe_db_snapshots(DBInstanceIdentifier=DB_INSTANCE_ID)
        snapshots = response.get("DBSnapshots", [])
        
    if not snapshots:
        print(f"[-] No snapshots found for instance {DB_INSTANCE_ID}.")
        sys.exit(1)

    latest_snapshot = max(snapshots, key=lambda s: s["SnapshotCreateTime"])
    source_snapshot_arn = latest_snapshot["DBSnapshotArn"]
    source_snapshot_id = latest_snapshot["DBSnapshotIdentifier"]
    print(f"[+] Found latest snapshot: {source_snapshot_id}")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M")
    target_snapshot_id = f"dr-{DB_INSTANCE_ID}-{timestamp}"

    print(f"[*] Copying {source_snapshot_arn} to {DEST_REGION} as {target_snapshot_id}...")
    copy_response = rds_dest.copy_db_snapshot(
        SourceDBSnapshotIdentifier=source_snapshot_arn,
        TargetDBSnapshotIdentifier=target_snapshot_id,
        SourceRegion=SOURCE_REGION,
        CopyTags=True
    )
    print(f"[✓] Copy initiated successfully! Status: {copy_response['DBSnapshot']['Status']}")

if __name__ == "__main__":
    copy_latest_snapshot()
