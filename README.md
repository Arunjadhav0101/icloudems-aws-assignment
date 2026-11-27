# iCloudEMS AWS Cloud Engineer Assignment

Production AWS environment setup for a university ERP (Laravel/PHP) handling high traffic spikes during admissions, fee deadlines, and exam results.

## Repository Layout
```text
icloudems-aws-assignment/
│
├── README.md               # Summary, assumptions, and task walkthrough
├── AI_USAGE.md             # Tools used, key prompts, AI adjustments
│
├── docker/
│   ├── Dockerfile          # Multi-stage build (<300MB, non-root, PHP-FPM+Nginx)
│   └── docker-compose.yml  # Local dev stack (App, MySQL, Redis, AI service)
│
├── ci/
│   ├── Jenkinsfile         # Declarative CI/CD pipeline (ECR, ASG refresh, notifications)
│   └── .gitlab-ci.yml      # GitLab pipeline (lint, test, docker build)
│
├── iam/
│   └── s3-upload-policy.json # Least privilege scoped upload policy (answer-sheets/*)
│
├── scripts/
│   └── copy-rds-snapshot.sh  # Bash/AWS CLI script copying RDS snapshots to ap-south-2
│
├── design/
│   ├── database-scaling.md   # Storage autoscaling, read replicas, Aurora migration
│   ├── backup-recovery.md    # DLM EBS snapshots, automated vs manual, PITR steps
│   └── cdc-architecture.md   # RDS to ClickHouse CDC, binlogs, ReplacingMergeTree DDL
│
└── screenshots/            # Scale-out, ALB, S3 replication, and pipeline proofs
```

## Summary of Completed Tasks
- **Task 1: EC2 Auto Scaling**: Multi-AZ ASG with Target Tracking at 60% CPU and scheduled scaling action for exam results.
- **Task 2: Database Auto Scaling**: Storage autoscaling ceiling, read replicas, and Aurora migration trigger metrics in `design/database-scaling.md`.
- **Task 3: IAM Users & Security**: Least-privilege IAM groups, EC2 S3 role, 3-tier security groups, and `iam/s3-upload-policy.json`.
- **Task 4: S3 Replication**: Cross-Region Replication (`ap-south-1` -> `ap-south-2`) for `answer-sheets/` prefix with Glacier lifecycle transitions.
- **Task 5: Backup & Snapshot Handling**: DLM backup schedules, PITR restoration guide in `design/backup-recovery.md`, and automated script in `scripts/copy-rds-snapshot.sh`.
- **Task 6: Load Balancer**: Application Load Balancer with health checks, path routing (`/api/*`), HTTPS redirect, and session stickiness analysis.
- **Task 7: GitLab CI/CD**: Protected branch rules on `main`, masked credentials, and `ci/.gitlab-ci.yml`.
- **Task 8: Jenkins Pipeline**: Declarative pipeline in `ci/Jenkinsfile` managing checkout, container build, ECR tagging, and ASG instance refresh.
- **Task 9: Docker & Compose (+5 AI Bonus)**: Multi-stage lightweight Dockerfile and full stack compose file with a FastAPI AI inference service (`/predict`).
- **Task 10: CDC Setup (RDS -> ClickHouse)**: End-to-end CDC architecture, binlog configuration, ReplacingMergeTree table schema, and consumer lag mitigation in `design/cdc-architecture.md`.
