#!/usr/bin/env bash
# ==============================================================================
# Task 5: Copy Latest RDS Snapshot to ap-south-2 (Hyderabad)
# Usage: ./copy-rds-snapshot.sh
# ==============================================================================

set -euo pipefail

SOURCE_REGION="ap-south-1"       # Primary: Mumbai
DEST_REGION="ap-south-2"         # DR: Hyderabad
DB_INSTANCE_ID="icloudems-rds-mysql"

echo "[*] Querying latest snapshot for ${DB_INSTANCE_ID} in ${SOURCE_REGION}..."

# Retrieve latest automated or manual snapshot ARN
LATEST_SNAPSHOT_ARN=$(aws rds describe-db-snapshots \
    --db-instance-identifier "${DB_INSTANCE_ID}" \
    --region "${SOURCE_REGION}" \
    --query "reverse(sort_by(DBSnapshots, &SnapshotCreateTime))[0].DBSnapshotArn" \
    --output text)

if [ -z "${LATEST_SNAPSHOT_ARN}" ] || [ "${LATEST_SNAPSHOT_ARN}" == "None" ]; then
    echo "[-] Error: No snapshots found for ${DB_INSTANCE_ID} in ${SOURCE_REGION}."
    exit 1
fi

TIMESTAMP=$(date -u +'%Y-%m-%d-%H%M')
TARGET_SNAPSHOT_ID="dr-${DB_INSTANCE_ID}-${TIMESTAMP}"

echo "[+] Found latest snapshot: ${LATEST_SNAPSHOT_ARN}"
echo "[*] Copying to ${DEST_REGION} as ${TARGET_SNAPSHOT_ID}..."

aws rds copy-db-snapshot \
    --source-db-snapshot-identifier "${LATEST_SNAPSHOT_ARN}" \
    --target-db-snapshot-identifier "${TARGET_SNAPSHOT_ID}" \
    --source-region "${SOURCE_REGION}" \
    --region "${DEST_REGION}" \
    --copy-tags

echo "[✓] Cross-region snapshot copy successfully initiated!"
