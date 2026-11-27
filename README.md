# iCloudEMS AWS Cloud Engineer Assignment

Production AWS environment setup for a university ERP (Laravel/PHP) handling high traffic spikes during admissions, fee deadlines, and exam results.

## Repository Layout
```text
.
├── README.md               # Summary, assumptions, architecture
├── AI_USAGE.md             # Tools used, prompts, customizations
├── docker/                 # Multi-stage Dockerfile & docker-compose.yml
├── ci/                     # Jenkinsfile and .gitlab-ci.yml
├── iam/                    # IAM policy JSON definitions
├── scripts/                # Automation and snapshot scripts
├── design/                 # Architecture design docs (Tasks 2, 5, 10)
└── screenshots/            # Verification proof screenshots
```

## Architecture & Tasks Completed
- **Task 1: EC2 Auto Scaling** - Launch Template and ASG with target tracking (60% CPU) across 2 AZs with scheduled scaling actions.
- **Task 2: Database Auto Scaling** - Storage autoscaling, read replica architecture, and CloudWatch alarm design.
- **Task 3: IAM & Security** - Least-privilege IAM groups, EC2 S3 read-only role, custom S3 upload policy, 3-tier security groups.
- **Task 4: S3 Replication** - Cross-region replication (`ap-south-1` -> `ap-south-2`) for `answer-sheets/` with lifecycle transition to Glacier.
- **Task 5: Snapshot Handling** - Automated DLM snapshot policies, RDS backup retention, PITR recovery procedures, and cross-region snapshot script.
- **Task 6: Load Balancer** - ALB with health checks, path routing (`/api/*`), HTTP-to-HTTPS redirect, and session affinity settings.
- **Task 7: CI/CD & GitLab** - Branch protection on `main`, masked/protected CI variables, and automated pipeline configuration.
