# AI Usage Log

In accordance with assignment guidelines:

## Tools Used
- Google Antigravity / Gemini 3.8 Flash

## Key Prompts & Tasks
1. **Task 1 (EC2 Auto Scaling)**: Requirement breakdown, capacity calculations (Min 1, Desired 2, Max 4), target tracking policy thresholds, and stress testing instructions.
2. **Task 2 (Database Scaling)**: RDS storage autoscaling thresholds, Laravel read/write replica configuration, Aurora migration metrics.
3. **Task 3 (IAM & Security)**: Least-privilege IAM group design, EC2 instance profile role, and scoped JSON bucket policy.
4. **Task 4 (S3 Replication)**: S3 Cross-Region Replication rules, prefix filters (`answer-sheets/`), and 180-day Glacier lifecycle policy.
5. **Task 5 (Snapshot Handling)**: DLM EBS policy design, Point-in-Time recovery runbook, and cross-region Boto3 RDS snapshot copy script.
6. **Task 6 (Load Balancer)**: Dual target group architecture, path-based routing rules, session timeout reasoning.
7. **Task 7 (GitLab CI/CD)**: Protected branch workflows, masked credentials best practices, and multi-stage `.gitlab-ci.yml`.

## Human Review & Customizations
- Validated AWS resource IDs and CIDRs against Mumbai (`ap-south-1`) and Hyderabad (`ap-south-2`) availability.
- Sanitized all scripts and configurations to strictly forbid hardcoded AWS access keys or secrets.
- Verified UTC to IST time conversion for ASG scheduled actions (08:00 AM IST = 02:30 AM UTC).
