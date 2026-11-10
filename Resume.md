# Robert Jackson

## Contact

**Email**: [robert@aztek.io](mailto:robert@aztek.io)<br/>
**Phone**: [406 396 9048](tel:+14063969048)<br/>
**LinkedIn**: [linkedin.com/in/robert-jackson-ii](https://www.linkedin.com/in/robert-jackson-ii/)<br/>
**GitHub**: [github.com/unacceptable](https://github.com/unacceptable)

## Summary

Platform Engineering and SRE leader with 11+ years driving DevOps
transformations and application modernization across a Fortune 500 enterprise
(Dell), a unicorn startup (Calm), and smaller startups. Led SRE teams at Dell and Koupon, managing
Koupon's team through its acquisition by PDI Technologies. Took two companies
through their first SOC2 certification and delivered $1.8M+ in annualized cloud
savings across Kubernetes platforms on AWS, GCP, and Azure.

## Certifications

**Kubernetes**: [Certified Kubernetes Administrator (CKA)](https://cdn.aztek.io/certs/CKA_Certificate.pdf)<br/>
**AWS**: [Solutions Architect - Professional](https://cdn.aztek.io/certs/awsSolutionsArchitect_PE.pdf), [DevOps Engineer - Professional](https://cdn.aztek.io/certs/awsDevOpsEngineer_PE.pdf), [Solutions Architect - Associate](https://cdn.aztek.io/certs/awsSolutionsArchitect_AE.pdf), [Developer - Associate](https://cdn.aztek.io/certs/awsCertifiedDeveloper_AE.pdf), [SysOps Administrator - Associate](https://cdn.aztek.io/certs/awsSysOpsAdmin_AE.pdf)<br/>
**General**: [CompTIA Security+](https://cdn.aztek.io/certs/CompTIA_Security%2B.pdf)

<!--
## Education

**Software Engineering** | Montana Tech | 2025 | GPA: 3.60
-->

## Professional Experience

### Selector ([selector.ai](https://selector.ai))
**Senior Staff Engineer** | 2026 to present

- Own the reliability and lifecycle of a large fleet of Google Kubernetes Engine
  (GKE) and Rancher Kubernetes Engine (RKE) clusters; authored the fleet
  patching policy and GKE upgrade schedule
- Saved ~$170k per year through cloud cost optimizations (unused PVC cleanup,
  right-sizing, decommissioning clusters) and a custom PVC autoscaler
- Built Python AI agents using Gemini 4 Argon that detect configuration drift and
  submit Pull Requests to correct Kubernetes manifests, deployed with
  least-privilege principles
- Guide enterprise customers through deploying the Selector stack into their
  own Kubernetes environments
- Designed a strangler release pattern for incrementally migrating Kustomize
  deployments to Helm under ArgoCD GitOps, and implemented it in my own
  microservices
- Refactored Infrastructure as Code and led the team's upgrade to the latest
  OpenTofu
- On-call for production; coordinate with teams across US, Europe, South Asia,
  and East Asia

### BackBox ([backbox.com](https://backbox.com))
**Senior DevOps Solutions Architect** | 2023 to 2026

- Built BackBox's cloud platform from the ground up: the Infrastructure as Code
  strategy and modules, modular CI/CD pipelines, and the company's first
  Kubernetes clusters; led the Terraform to OpenTofu migration
- Led BackBox's first SOC2 certification and designed the AI security strategy
  (vendor terms of use, data security, and privacy review)
- Architected a Vulnerability Intelligence Relay (CVE data lake) and an AI
  Agent Swarm on AWS Bedrock with RAG that produces structured remediation
  guidance, plus a Grader agent (Sentinel) to score remediation quality
- Built automation and an API abstraction for isolated ephemeral sandboxes used
  for customer trials, QA, and SaaS offerings
- Containerized FastAPI microservices; implemented Grafana and DataDog
  observability, including LLMObs for AI services, and PagerDuty alerting

### Koupon, a PDI Technologies company ([koupon.com](https://koupon.com))
**Site Reliability Engineering Manager** | 2021 to 2023

- Managed an SRE team of 4 across the US and India using Servant Leadership
- Led the team through Koupon's acquisition by PDI Technologies and retained
  every team member through the transition by representing their concerns to
  leadership and securing the resources they needed
- Led Koupon's DevOps transformation: introduced Infrastructure as Code (custom
  Terraform modules, Terragrunt), Helm and Helmfile, and CI/CD tooling on
  Kubernetes, and replaced IAM access keys with IRSA and Cross-Account Roles
- Advised engineering teams across the organization on modernizing their app
  stacks, and won senior leadership support for tech debt and other
  Non-Functional Requirements
- Used Value Stream Mapping with Dev, QA, Security, and Data teams to find and
  remove workflow bottlenecks
- Consolidated 10 EKS clusters into 4 and cut cloud spending by ~$440k per year
  (Reserved Instances, Savings Plans, S3 optimizations, EC2 to EKS migrations);
  ran infrastructure supporting 25% of revenue on 5% of cloud spend
- Defined the 99.99% SLO and 99.9% SLA, led Koupon's first SOC2 certification,
  and launched a Status Page for internal and external stakeholders
- Migrated observability from Sumo Logic to DataDog, MySQL on EC2 to MariaDB on
  RDS, and in-house Twilio alerting to PagerDuty

### Dell ([dell.com](https://www.dell.com))
**DevOps Solutions Architect** | 2018 to 2021

- Team Lead for the SRE team managing infrastructure for 86 organizations;
  primary owner of the Dell Data Security Platform (DDSP), Insights Platform,
  and Remediation Platform
- Modernized those platforms from individual EC2 servers to containers on ECS
  and then to Kubernetes; managed dozens of EKS clusters and helped migrate
  them to AKS
- Saved ~$1M per year by right-sizing Elasticsearch clusters and databases,
  consolidating workloads, and setting Kubernetes resource requests and limits
- Converted manually provisioned infrastructure to CloudFormation, then
  migrated it to Terraform using a strangler release pattern
- Guided numerous development teams in adopting DevOps patterns: microservice
  CI/CD pipelines, GitOps with ArgoCD and Keptn, ChatOps, and container
  scanning with Trivy
- Built monitoring with DataDog, Prometheus, and Grafana, and secrets
  management with HashiCorp Vault
- Contributed upstream to open source projects, including Keptn, Helm charts,
  the NGINX Ingress Controller, and HashiCorp Terraform providers

### Calm ([calm.com](https://www.calm.com))
**DevOps Consultant (Contract)** | 2019 to 2020

- Managed multiple Kubernetes clusters and Infrastructure as Code with
  Terraform and Terragrunt
- Designed ephemeral development environments that gave each commit its own
  URL, letting developers test microservices against the core dev stack
- Onboarded new microservices and helped developers optimize builds, cutting a
  6-minute Docker build in half through layer caching and Dockerfile reordering
- Deployed Apache Airflow and Jupyter on Kubernetes with hand-written Helm
  charts

### Alkami ([alkami.com](https://www.alkami.com))
**Site Reliability Engineer** | 2017 to 2018

- Built a Python CLI on the ARMOR API, Ansible playbooks for Windows Server, and
  a TeamCity and Ansible delivery pipeline for .NET banking applications

### ARMOR, formerly Firehost ([armor.com](https://www.armor.com))
**Site Reliability Engineer** | 2015 to 2017

- Authored security-focused Ansible and Terraform automation, AWS Lambda
  (Python/boto3) reporting, and cost reductions of ~$188k per year

## Skills

**Leadership**: DevOps Transformation, Application Modernization, Servant Leadership, Coaching, Value Stream Mapping, SCRUM, Blameless Postmortems, Cloud Cost Optimization (FinOps), SOC2 Compliance<br/>
**Core DevOps Skills**: Kubernetes (GKE, EKS, AKS, RKE), AWS ECS, Helm, Kustomize, Ansible, Docker, OpenTofu, Terraform, Terragrunt, Packer, AWS CloudFormation, Istio, Open Policy Agent (OPA), Git<br/>
**Cloud Platforms**: AWS, Azure, GCP<br/>
**Programming & Scripting**: Python, C++, Bash & Shell, PowerShell<br/>
**CI/CD Tools**: Jenkins, GitHub Actions, GitLab CI, ArgoCD, Keptn, Bamboo<br/>
**Databases & Messaging**: PostgreSQL, MySQL, MariaDB, MSSQL, DynamoDB, CosmosDB, Elasticsearch, RabbitMQ, Redis<br/>
**Secrets Management**: HashiCorp Vault, OpenBao, AWS Secrets Manager, AWS SSM Parameter Store<br/>
**Observability**: SLO/SLI, DataDog, OpenTelemetry, Prometheus, Grafana, New Relic, Sumo Logic, Splunk, PagerDuty<br/>
**AI & LLM Platforms**: AWS Bedrock, Google Gemini 4 Argon, Retrieval-Augmented Generation (RAG), AI Agents
