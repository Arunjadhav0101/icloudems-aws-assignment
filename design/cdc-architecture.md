# Task 10: Change Data Capture (CDC) Architecture (RDS to ClickHouse)

## 1. Architecture Diagram
```
+-----------------------------------------------------------------------------------------+
|                                    AWS Region: ap-south-1                               |
|                                                                                         |
|   +-------------------+          +------------------+         +---------------------+   |
|   |  Amazon RDS MySQL |          |  Debezium / DMS  |         |   Amazon MSK        |   |
|   |  (binlog enabled) | -------> |  CDC Connector   | ------> |  (Kafka Cluster)    |   |
|   +-------------------+          +------------------+         +---------------------+   |
|                                                                          |              |
|                                                                          v              |
|                                                               +---------------------+   |
|                                                               | ClickHouse          |   |
|                                                               | (Kafka Engine)      |   |
|                                                               +---------------------+   |
|                                                                          |              |
|                                                                          v (MV trigger) |
|                                                               +---------------------+   |
|                                                               | ReplacingMergeTree  |   |
|                                                               | (Analytics DDL)     |   |
|                                                               +---------------------+   |
+-----------------------------------------------------------------------------------------+
```

---

## 2. RDS MySQL Configuration
To capture real-time row mutations within 1 minute, create a custom DB Parameter Group with:
1. `binlog_format = ROW`: Captures complete before-and-after row states rather than non-deterministic SQL statements.
2. `binlog_row_image = FULL`: Logs all columns for update and delete events.
3. Retention window configuration via stored procedure:
   ```sql
   CALL mysql.rds_set_configuration('binlog retention hours', 72);
   ```
   *Retention is set to 72 hours to prevent binlog purges if downstream consumers face temporary outages.*

---

## 3. ClickHouse Table DDL (`fee_transactions`)

### ReplacingMergeTree Destination Table:
```sql
CREATE TABLE IF NOT EXISTS university_analytics.fee_transactions
(
    transaction_id UInt64,
    student_id UInt64,
    fee_type LowCardinality(String),
    amount Decimal64(2),
    payment_status LowCardinality(String),
    payment_mode LowCardinality(String),
    updated_at DateTime,
    is_deleted UInt8 DEFAULT 0
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (student_id, transaction_id);
```

### Handling Updates & Deletes:
* **Updates**: `ReplacingMergeTree(updated_at)` uses the `updated_at` column as the version tag. When identical sorting keys `(student_id, transaction_id)` arrive, ClickHouse merges background parts and keeps only the highest `updated_at` row version. Queries append `FINAL` (`SELECT * FROM fee_transactions FINAL`) to evaluate deduplication on read.
* **Deletes**: Soft deletes are represented by `is_deleted = 1`. Analytical queries filter with `WHERE is_deleted = 0`.

---

## 4. Replication Lag Monitoring & 2-Hour Outage Recovery
* **Lag Monitoring**:
  * CloudWatch Metric: `EstimatedMaxTimeLag` / `KafkaConsumerLag` on MSK consumer groups.
  * ClickHouse Metric: Query lag directly comparing `now() - max(updated_at)` from `fee_transactions`.
  * Alarm Threshold: If consumer lag exceeds **60 seconds**, trigger an SNS alert to the on-call engineer.
* **Downstream 2-Hour Outage Scenario**:
  * **Zero Data Loss**: Because RDS retains binlogs for 72 hours and Kafka retains messages for 7 days, no data is dropped.
  * **Backpressure Recovery**: When ClickHouse recovers, the Kafka engine resumes ingestion from the committed Kafka offsets. Ingestion operates at line rate (>50,000 events/sec), catching up the 2-hour backlog in minutes without impacting production RDS OLTP operations.
