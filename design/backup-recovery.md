# Task 5: Backup, Snapshot Handling & Recovery

## 1. Amazon Data Lifecycle Manager (DLM) EBS Policy
* **Target Resources**: EBS volumes tagged `Environment = Production` and `Role = ERP-Web`.
* **Backup Schedule**:
  * **Daily Schedule**: Runs every 24 hours at 01:00 UTC. Retains **7 daily snapshots**.
  * **Weekly Schedule**: Runs every Sunday at 02:00 UTC. Retains **4 weekly snapshots**.
* **IAM Role**: Uses standard `AWSDataLifecycleManagerDefaultRole`.

---

## 2. Automated Backups vs. Manual Snapshots

| Dimension | RDS Automated Backups | Manual DB Snapshots |
| :--- | :--- | :--- |
| **Creation** | Created automatically daily during backup window + continuous binlog ingestion to S3. | Manually triggered on-demand by engineer or automated CI/CD script. |
| **Retention** | Configured to **7 days**. Deleted automatically once retention expires or upon DB deletion. | Persists indefinitely until explicitly deleted by administrator. |
| **PITR Support** | **Full support**: Point-in-time restore to any second within the retention window. | **No PITR**: Can only restore to the exact snapshot point in time. |
| **Cross-Region** | Region-bound unless automated cross-region replication is configured. | Can be copied directly to secondary regions (e.g., `ap-south-2`). |

---

## 3. Point-in-Time Recovery (PITR) Runbook (10:15 AM Yesterday)
1. **Locate Source DB**: In the RDS Console, select `icloudems-rds-mysql`.
2. **Initiate Restore**: Click **Actions** -> **Restore to point in time**.
3. **Specify Target Timestamp**:
   * Choose **Custom date and time**.
   * Date: Yesterday's date.
   * Time: `10:15:00 AM IST` (`04:45:00 UTC`).
4. **Target Instance Details**:
   * Name: `icloudems-rds-recovery-1015am`
   * Select production VPC, DB subnet group, and attach the RDS Security Group (`sg-erp-rds`).
5. **Execution & Validation**:
   * Click **Restore to point in time**.
   * Once status changes to *Available*, run schema & data integrity checks.
   * Redirect ERP traffic to the recovered DB endpoint via AWS Parameter Store or route flip.
