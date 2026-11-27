# Task 2: Database Auto Scaling Design

## 1. Storage Autoscaling
- **Configuration**: Enabled via RDS Console / AWS CLI (`--max-allocated-storage 500`).
- **Initial Allocation**: 50 GB.
- **Max Storage Ceiling**: 500 GB.
- **Rationale**: Dynamic expansion prevents critical disk-full outages during high-volume answer sheet and student grade ingestions, while capping the threshold prevents runaway storage costs.

## 2. Read Scaling & Laravel Read/Write Split
- **Read Replicas**: Deploy an asynchronous read replica in `ap-south-1b`.
- **Laravel Configuration (`config/database.php`)**:
```php
'mysql' => [
    'read' => [
        'host' => [env('DB_READ_HOST', 'erp-read-replica.xxxxxx.ap-south-1.rds.amazonaws.com')],
    ],
    'write' => [
        'host' => [env('DB_WRITE_HOST', 'erp-primary.xxxxxx.ap-south-1.rds.amazonaws.com')],
    ],
    'sticky'    => true,
    'driver'    => 'mysql',
    'database'  => env('DB_DATABASE', 'icloudems'),
    'username'  => env('DB_USERNAME', 'erp_user'),
    'password'  => env('DB_PASSWORD', ''),
],
```
- `sticky => true` ensures that records written during the current request lifecycle can be immediately read back without replica replication delay anomalies.

## 3. Aurora MySQL Migration Trigger
- **Trigger Metrics**:
  - Read replication lag exceeding 1.0 second on standard RDS.
  - Read latency consistently exceeding 15ms during peak admission periods.
- **Aurora Auto Scaling Target**: Configure Aurora auto-scaling with target metric `RDSReaderAverageCPUUtilization = 60%`, automatically scaling Aurora readers from 1 to 5.

## 4. Key CloudWatch Alarms
1. `CPUUtilization > 80%` for 5 minutes (Severity: High) -> SNS alert to DevOps.
2. `FreeStorageSpace < 10 GB` (Severity: Critical) -> Warning before storage ceiling is hit.
3. `DatabaseConnections > 80%` of max pool for 3 minutes (Severity: High) -> Detect connection pool starvation.
