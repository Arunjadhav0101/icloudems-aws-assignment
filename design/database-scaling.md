# Task 2: Database Auto Scaling Design

## 1. Storage Autoscaling Configuration
* **Enabling Storage Autoscaling**:
  * In the AWS RDS Console: Select the MySQL DB instance -> Click **Modify** -> Under **Storage autoscaling**, select **Enable storage autoscaling**.
  * Alternatively, via AWS CLI:
    ```bash
    aws rds modify-db-instance \
        --db-instance-identifier icloudems-rds-mysql \
        --max-allocated-storage 500 \
        --apply-immediately
    ```
* **Storage Threshold & Rationale**:
  * **Initial Allocation**: 50 GB General Purpose SSD (gp3).
  * **Max Storage Threshold**: **500 GB**.
  * **Rationale**: University admissions, fee collection, and exam result days produce severe surges in concurrent invoice generation, PDF audit logging, and audit logs. Setting an upper bound of 500 GB provides 10x headroom to prevent catastrophic disk-full database halts while protecting against runaway AWS billing caused by rogue queries or runaway log loops.

---

## 2. Scaling Reads & Laravel Split
* **Read Replicas**:
  * Deploy an Amazon RDS Read Replica across an alternate Availability Zone (`ap-south-1b`).
  * Direct read-heavy student traffic (grade view, attendance reports, transcript lookups) exclusively to the Read Replica.
* **Laravel Read/Write Splitting (`config/database.php`)**:
```php
'mysql' => [
    'read' => [
        'host' => [
            env('DB_READ_HOST', 'icloudems-read.xxxxxx.ap-south-1.rds.amazonaws.com')
        ],
    ],
    'write' => [
        'host' => [
            env('DB_WRITE_HOST', 'icloudems-primary.xxxxxx.ap-south-1.rds.amazonaws.com')
        ],
    ],
    'sticky'    => true, // Guarantees newly written data in a user session is read back immediately
    'driver'    => 'mysql',
    'database'  => env('DB_DATABASE', 'icloudems'),
    'username'  => env('DB_USERNAME', 'erp_user'),
    'password'  => env('DB_PASSWORD', ''),
    'charset'   => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix'    => '',
],
```

---

## 3. Migration to Amazon Aurora MySQL
* **Migration Trigger**:
  * When replica lag on standard RDS MySQL consistently exceeds **1.0 second** during traffic surges.
  * When read transactions exceed 10,000 IOPS and read latency exceeds **15ms**.
* **Aurora Auto Scaling Setup**:
  * Metric: `RDSReaderAverageCPUUtilization`
  * Target Value: **60%**
  * Capacity: Automatically scales Aurora reader nodes from 1 up to 5 instances in response to peak university traffic.

---

## 4. Recommended CloudWatch Alarms

| Alarm Metric | Threshold | Evaluation Period | Severity | Action |
| :--- | :--- | :--- | :--- | :--- |
| **`CPUUtilization`** | $\ge 80\%$ | 2 consecutive 5-min periods | High | SNS alert to DevOps channel; scale read replicas |
| **`FreeStorageSpace`** | $\le 10\text{ GB}$ | 1 period (5 min) | Critical | High-priority PagerDuty/SNS alert before storage ceiling |
| **`DatabaseConnections`** | $\ge 80\%$ of `max_connections` | 3 consecutive 1-min periods | High | Alert on pool exhaustion, trigger RDS Proxy investigation |
