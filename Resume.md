# Robert Jackson

## Contact

**Email**: [robert@aztek.io](mailto:robert@aztek.io)<br/>
**LinkedIn**: [robert-jackson-ii](https://www.linkedin.com/in/robert-jackson-ii/)<br/>
**GitHub**: [unacceptable](https://github.com/unacceptable)

## Certifications

### **Kubernetes**
* [Certified Kubernetes Administrator (CKA)](https://cdn.aztek.io/certs/CKA_Certificate.pdf)

### **AWS**
* [AWS Certified Solutions Architect - Professional](https://cdn.aztek.io/certs/awsSolutionsArchitect_PE.pdf)
* [AWS Certified DevOps Engineer - Professional](https://cdn.aztek.io/certs/awsDevOpsEngineer_PE.pdf)
* [AWS Certified Solutions Architect - Associate](https://cdn.aztek.io/certs/awsSolutionsArchitect_AE.pdf)
* [AWS Certified Developer - Associate](https://cdn.aztek.io/certs/awsCertifiedDeveloper_AE.pdf)
* [AWS Certified SysOps Administrator - Associate](https://cdn.aztek.io/certs/awsSysOpsAdmin_AE.pdf)

### **General**
* [Security+](https://cdn.aztek.io/certs/CompTIA_Security%2B.pdf)

## Professional Experience

### BackBox - Sr. DevOps Solutions Architect - 2023 to present

- Led the effort to obtain BackBox's first SOC2 certification
- Designed the AI security strategy, evaluating vendor terms of use, SOC2
  compliance, data security and privacy policies to ensure organizational fit
- Architected a Vulnerability Intelligence Relay service to build a Data Lake
  for CVE information, enabling centralized vulnerability tracking and analysis
- Designed and implemented an AI Agent Swarm using AWS Bedrock that parses CVE
  data and produces standardized, structured output with enhanced remediation
  guidance
- Integrated Retrieval-Augmented Generation (RAG) patterns into the agent
  architecture for context-aware vulnerability analysis
- Developed a Grader AI (Sentinel) agent for the CVE remediation stack to evaluate and
  score remediation quality and completeness
- Built a proof-of-concept for embedding models to enable AI-powered command
  search within the BackBox application
- Designed the Infrastructure as Code (IaC) strategy
- Created Infrastructure as Code modules from scratch
- Wrote and containerized Python microservices using FastAPI and AWS services like AWS Bedrock
- Stood up BackBox's first Kubernetes clusters
- Designed CI/CD pipelines from scratch following a DRY modular pattern
- Designed platform automation and an API abstraction to stand up isolated
  ephemeral sandboxes for customer trials, QA testing, and SaaS offerings
- Coordinated with marketing on customer sandbox trials
- Oversaw the migration from Terraform to OpenTofu
- Managed PostgreSQL, MariaDB, and AWS DynamoDB databases
- Utilized RabbitMQ for message queuing and AWS SSM Parameter Store for secrets
  management
- Implemented observability using Grafana and DataDog, including instrumenting
  AI services with DataDog's LLMObs and creating alerts based on application logs
- Configured PagerDuty for on-call incident management and alerting

### PDI Technologies - Site Reliability Engineering Manager - 2022 to 2023

- Led team during Koupon's acquisition by PDI, ensuring team members have
  necessary resources
- Represented team members and addressed concerns, implementing Servant
  Leadership principles
- Championed quality of life improvements and improved team morale through
  proper work allocation, pair programming, and listening to individual needs
- Led regular SCRUM meetings (Morning Standups, Backlog Refinements,
  Retrospectives)
- Facilitated 1-on-1 conversations with team members and other leaders to align
  with customer needs
- Advocated for important work initiatives to senior leadership, such as
  addressing tech debt and other Non-Functional Requirements
- Ensured delivery of critical business items, including releases, application
  uptime, and overall stability
- Consulted with multiple engineering teams across the organization on action
  items to modernize various app stacks
- Migrated observability platform from Sumo Logic to DataDog, improving
  monitoring capabilities and reducing costs
- Procured various tooling for team needs (DataDog, Udemy, misc. software
  licenses, etc.)
- Reduced cloud spending by ~$36.7k per month through various optimization
  strategies
- Oversaw infrastructure accounting for 25% of total revenue with only 5% of the
  organization's total cloud spending
- Led the migration of MySQL database from AWS EC2 to an updated MariaDB version
  on AWS RDS
- Managed MSSQL, PostgreSQL, and MySQL/MariaDB databases with RabbitMQ message
  queuing and Redis caching
- Utilized AWS SSM Parameter Store for secrets management
- Implemented PagerDuty for incident response
- Initiated migration of GCP Terraform infrastructure to my team's established
  Terragrunt pattern

### Koupon - Site Reliability Engineering Manager - 2021 to 2022

- Led the effort to obtain Koupon's first SOC2 certification
- Created a Status Page for internal and external stakeholders
- Collaborated with Dev, QA, Security, and Data teams to identify workflow
  bottlenecks using Value Stream Mapping and other methods
- Containerized legacy monitoring scripts, managed Sumo Logic observability
  platform, and implemented security scanning initiatives for Docker containers,
  Kubernetes, and cloud provider
- Instrumented application code with StatsD for metrics collection and
  performance monitoring
- Established CI/CD tooling in Kubernetes, wrote Helm charts for business needs,
  and introduced team to Infrastructure as Code orchestration with custom
  Terraform modules and Terragrunt
- Transitioned team to Helm orchestration with Helmfile and from IAM users with
  access keys to IAM role authentication using IRSA (replacing KIAM) and
  Cross-Account Roles
- Oversaw cost optimization of AWS Redshift RA3 instances and improved data
  ingestion using COPY commands from S3
- Managed RabbitMQ message queuing and Redis caching
- Implemented AWS SSM Parameter Store for secrets
- Configured PagerDuty for incident management (migrating from an in-house solution
  developed with Twilio)

### Dell - DevOps Solutions Architect - 2018 to 2021

- Served as Team Lead for Dell's Insights Platform SRE team, driving success and
  performance in a DevOps environment
- Developed cloud-agnostic solutions using Kubernetes, Helm, and Infrastructure
  as Code with Terraform and CloudFormation
- Integrated SecOps patterns, such as container scanning with Trivy, into CI
  pipelines for enhanced security and compliance
- Guided numerous teams to adopt DevOps patterns using strategies from DevOps
  literature and industry-leading technologies
- Implemented ChatOps integrations for development teams, automating
  communication and collaboration
- Authored CI/CD pipelines for microservices, handling code compilation,
  artifact pushing, and version tagging
- Conducted cost analyses and provided optimization recommendations, resulting
  in significant savings
- Instrumented microservices with StatsD for custom metrics and application
  performance insights
- Enhanced infrastructure stability through monitoring with DataDog and Grafana,
  implementing anomaly detection and service hotfixes
- Participated in EKS to AKS migration as the organization transitioned from AWS
  to Azure for business relationship reasons
- Migrated PostgreSQL on AWS RDS to Azure CosmosDB and from AWS SQS to Azure Queue
  Storage and utilized Redis for caching
- Implemented GitOps workflows using ArgoCD and Keptn for continuous delivery
- Managed secrets with HashiCorp Vault, AWS Secrets Manager, and AWS SSM
  Parameter Store

### Alkami - Site Reliability Engineer - 2017 to 2018

- Facilitated private cloud migrations from ARMOR Gen3 to ARMOR Gen4
- Developed a custom CLI tool utilizing the ARMOR API, implemented in Python
- Authored Ansible automation playbooks for Windows Server to deploy banking
  applications across multiple cloud platforms
- Regularly deployed custom .NET applications to Windows Server Core
- Designed and maintained Chocolatey deployment packages for internal use
- Established a continuous delivery pipeline using Team City and Ansible
- Set up an AWS Lambda deployment pipeline with an Amazon Linux Docker image and
  Terraform
- Implemented application performance monitoring using New Relic
- Integrated webhooks to notify Slack channels of changes in JIRA (prior to the
  official server plugin) and Datadog
- Managed MSSQL databases and Redis caching
- Used PagerDuty for on-call incident response

### ARMOR (Firehost) - Site Reliability Engineer - 2015 to 2017

- Provided guidance on best security practices for AWS services configuration,
  supporting ARMOR Anywhere infrastructure
- Reconstructed and migrated data for multiple internal application stacks,
  including Atlassian Jira, Jira Helpdesk, Confluence, and Grafana
- Authored security-focused software automation playbooks using Ansible and
  Infrastructure as Code with Terraform
- Enhanced infrastructure stability through monitoring with New Relic, DataDog,
  and Splunk, implementing anomaly detection and service hotfixes
- Recommended cost-reduction strategies, resulting in ~$15.7k+ monthly savings
  (ELK stack optimizations and Reserved Instances)
- Developed AWS Lambda functions for automated reporting, infrastructure
  monitoring, and alert generation using the Python boto3 library
- Managed MySQL, MSSQL, and MariaDB databases with RabbitMQ for message queuing
  and Redis for caching
- Utilized AWS SSM Parameter Store for secrets management
- Used PagerDuty for on-call incident response

## Skills

### Technical Skills:

**Core DevOps Skills**: Kubernetes, Helm, Ansible, Docker, Terraform, Packer, AWS CloudFormation, Security Scanning, Git</br>
**Cloud Platforms**: AWS, Azure, GCP</br>
**Programming & Scripting**: Python, Bash & Shell, PowerShell</br>
**CI/CD Tools**: Jenkins, GitHub Actions, GitLab CI, ArgoCD, Keptn, Bamboo</br>
**Databases**: PostgreSQL, MySQL, MariaDB, MSSQL, DynamoDB, CosmosDB</br>
**Message Queues & Caching**: RabbitMQ, AWS SQS, Azure Queue Storage, Redis</br>
**Secrets Management**: HashiCorp Vault, AWS Secrets Manager, AWS SSM Parameter Store</br>
**Observability**: DataDog, Grafana, New Relic, Sumo Logic, Splunk</br>
**Incident Management**: PagerDuty</br>
**Networking**: VPCs, Load Balancers, DNS, CDNs</br>
**Operating Systems**: Linux, Windows Server</br>
**Cross-functional Skills**: Containerization, Security & Compliance, API & Webhook Automation, Virtualization, Infrastructure Monitoring

### Soft Skills:

**Management & Team Building**: Servant Leadership, Communication, Collaboration, Conflict Resolution, Coaching</br>
**Problem-Solving**: Troubleshooting, Debugging, Observability</br>
**Time management**: Kanban, Sprints (prefer Scrumban framework), Pomodoro Timers, Prioritizing tasks & Backlog Refinement</br>
**SCRUM leadership**: Standup, Backlog Refinement, Deployment Retrospectives, Blameless Postmortems</br>
**Business Value**: Cost Optimizations</br>
