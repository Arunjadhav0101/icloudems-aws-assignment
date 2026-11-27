# Task 5: Snapshot Handling & PITR

## 1. Amazon Data Lifecycle Manager (DLM) Policy
- **Target**: EBS volumes tagged `Environment = Production`
- **Schedule**:
  - Daily: Every 24 hours at 01:00 UTC, retain **7 daily snapshots**.
  - Weekly: Every Sunday at 02:00 UTC, retain **4 weekly snapshots**.

## 2. Automated Backups vs Manual Snapshots
- **Automated Backups**: Continuous transaction logs + daily snapshot. Retained for 7 days. Supports point-in-time recovery to any second. Automatically deleted upon DB instance termination unless preserved.
- **Manual Snapshots**: Explicitly triggered. Retained indefinitely until manual deletion. Can be copied directly across regions (`ap-south-1` -> `ap-south-2`).

## 3. Point-in-Time Recovery (PITR) to 10:15 AM Yesterday
1. Navigate to AWS RDS -> Databases -> Select primary database.
2. Select **Actions** -> **Restore to point in time**.
3. Choose **Custom date and time**: Select yesterday's date and enter `10:15:00 AM IST` (`04:45:00 UTC`).
4. Set Target DB Identifier: `icloudems-rds-restored-1015am`.
5. Attach production VPC and RDS Security Group (`sg-erp-rds`).
6. Click Restore. Once Available, verify data and redirect application connection string (`DB_HOST`).
