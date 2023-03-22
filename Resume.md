Robert Jackson
==============

Social  |Contact                                                            |Code                                                                   |Link
-----:  |:---                                                               |---:                                                                   |:---
Email   |[robert@aztek.io](mailto:robert@aztek.io)                          |GitHub                                                                 |[unacceptable](https://github.com/unacceptable)
LinkedIn|[robert-jackson-ii](https://www.linkedin.com/in/robert-jackson-ii/)|GitLab                                                                 |[aztek-io](https://gitlab.com/aztek-io)

Certifications
--------------
Advanced                                                                                                    | Intermediate
---                                                                                                         |--------------
[Certified Kubernetes Administrator (CKA)](https://cdn.aztek.io/certs/CKA_Certificate.pdf)                  |[AWS Certified Solutions Architect - Associate](https://cdn.aztek.io/certs/awsSolutionsArchitect_AE.pdf)
[AWS Certified Solutions Architect - Professional](https://cdn.aztek.io/certs/awsSolutionsArchitect_PE.pdf) |[AWS Certified Developer - Associate](https://cdn.aztek.io/certs/awsCertifiedDeveloper_AE.pdf)
[AWS Certified DevOps Engineer - Professional](https://cdn.aztek.io/certs/awsDevOpsEngineer_PE.pdf)         |[AWS Certified SysOps Administrator - Associate](https://cdn.aztek.io/certs/awsSysOpsAdmin_AE.pdf)
                                                                                                            |[Security+](https://cdn.aztek.io/certs/CompTIA_Security%2B.pdf)

Job History
-----------
### PDI Technologies - 2022 to present
#### Site Reliability Engineering Manager
* Leading a team during an acquisition (Koupon was acquired by PDI)
* Working to ensure that team members have the resources that they need
* Focusing on ensuring that team members and their concerns are being represented
* Finding ways to implement Servant Leadership principles
* Championing quality of life improvements for my team
* Aiming to improve team morale through proper work allocation (e.g. finding the right balance between easy wins and skill development), pair programming, and listening to the needs of individuals
* Led regular SCRUM meetings like Morning Standups, Backlog Refinements, and Retrospective meetings while hiring a proper SCRUM Leader
* Setting up 1-on-1 conversations with team members and with other leaders in the organization to ensure that we are providing the service and features that align best with our customer's needs
* Selling senior leadership on work initiatives that are important to the team and organization like addressing tech debt items and patching clusters
* Ensuring that our team is following through on delivering items critical to the needs of the business (e.g. making releases easier for developers, application uptime, and overall stability)
* Advising the engineering teams on ways we can modernize our app stack
* Reduced cloud spending by ~$36.7k per month (achieved via purchasing RIs, costs savings plans, optimizing S3 API operations and storage lifecycles, and migrating services from EC2 to EKS)
* Oversaw infrastructure that accounted for 25% of the total revenue @ 5% of the total cloud spending
* Purchased tooling for my team's needs (DataDog, misc. software licenses, Udemy, etc.)

### Koupon - 2021 to 2022
#### Site Reliability Engineering Manager
* Created a Status Page: https://status.koupon.com for internal and external stakeholders
* Worked with Dev, QA, Security, and Data teams to identify duplications of effort and bottlenecks in existing workflows using Value Stream Mapping and other patterns to help make work visible
* Containerized legacy monitoring scripts
* Implemented security scanning initiatives to scan Docker containers, Kubernetes, and our cloud provider to identify potential misconfigurations.
* Stood up CI and CD tooling in Kubernetes
* Wrote helm charts for specific business needs https://charts.devops.koupon.com/ (deploying Microservices and CronJob tasks)
* Introduced the team to Infrastructure as Code orchrestration with custom Terraform modules (modules that we wrote ourselves not forked from public repos) and Terragrunt
* Introduced the team to Helm orchestration with Helmfile
* Moved the team away from IAM access keys towards IAM role authentication using KIAM (for microservices) and Cross-Account Roles (for users)

### Dell - 2018 to 2021
#### DevOps Solutions Architect
* Team Lead for Dell's Insights Platform SRE team
* Developing Cloud-Agnostic Solutions for Microservices via the use of Kubernetes and Helm
* Writing Infrastructure as Code (mostly using Terraform with a bit of CloudFormation)
* Implementing SecOps patterns like Container Scanning (via Trivy) into CI Pipelines
* Deploying monolithic applications like Jenkins in Kubernetes (this was before the community helm chart)
* Helped a myriad of teams addopt DevOps Patterns via methods outlined in DevOps literature and industry leading technologies
* Projects contributed to:
    - CNCF projects (Keptn, Helm Charts, NGINX Ingress Controller, etc.)
    - Hashicorp Terraform Providers (kubernetes-alpha, azurerm, aws, etc.)
    - Other OSS projects (shellcheck, robin_stocks, etc.)

#### Principal Site Reliability Engineer
* Developed Cloud-Agnostic solutions using Kubernetes and Helm/Helmfile and Terraform modules
* Built Monitoring from the ground up (using CloudWatch -> DataDog -> Promethues/Grafana/Alert Manager)
* Built out the ChatOps Integrations for Development Teams (e.g. CVE Bot, CloudWatch Bot, etc.)
* Built out automation around Blue-Green Deployments using CloudFormation (later switched to in place deployment strategies)
* Wrote CI pipelines for microservices which compiled code, pushed artifacts, and tagged versions
    - We started out using bamboo specs, but switched to Jenkinsfiles and shared libraries in Jenkins
* Performed costing analyses and recommended courses of actions that cumulatively saved ~$84.6k per month
    - This was achieved via the use of Spot Instances, IaC use, RDS and Redshift cluster consolidation/resizing, etc.

### Alkami - 2017 to 2018
#### Site Reliability Engineer
* Assisted with private cloud migrations from ARMOR Gen3 to ARMOR Gen4
* Created a private CLI tool that leverages the ARMOR API written in python
* Wrote Ansible automation Playbooks for Windows Server to deploy our banking application in multiple clouds
* Deployed custom .NET Applications to Windows Servers Core on a near daily basis
* Created and maintained Chocolatey deployment packages for internal usage
* Created Continuous Delivery Pipeline using TeamCity and Ansible
* Created an AWS Lambda Deployment pipeline using an Amazon Linux Docker Image and Terraform
* Used webhooks to notify Slack Channels of changes in JIRA (before official server plugin), Datadog, etc.

### ARMOR | Firehost - 2015 to 2017
#### Site Reliability Engineer
* Advised teams on best security practices for configuring AWS Services, supporting ARMOR Anywhere Infrastructure
* Rebuilt and migrated data for several application stacks for internal use (Atlassian Jira, Jira Helpdesk, Confluence, Grafana)
* Wrote various security-minded software automation playbooks for Ansible and Infrastructure as Code automation with Terraform
* Added stability to infrastructure with monitoring, anomaly detection, and service hotfixes
* Made recommendations on cost reduction changes totaling ~$15.7k+ savings per month (ELK stack infrastructure optimizations & RIs)
* Wrote AWS Lambda Functions to automate reports, monitor infrastructure, and generate alerts via the Python boto3 library

Skills
------
DevOps Tooling      | Programming & Scripting   | CI/CD          | Generic
-------------       | -------------             | ---            | ------
Kubernetes          | Bash & Shell              | Jenkins        | Webhooks & APIs
Helm                | Python                    | Github Actions | Troubleshooting
Ansible             | Go                        | Gitlab         | Virtualization
Docker              | Powershell                | Keptn          | Containers
Terraform           |                           | Bamboo         | Security Scanning
Packer              |                           |                | templating engines
