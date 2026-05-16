<div align="center">

# StrawHat-Enterprise

**Cloud platform engineering, Azure infrastructure, and developer experience — open-sourced.**

[![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Helm](https://img.shields.io/badge/Packaging-Helm-0F1689?logo=helm&logoColor=white)](https://helm.sh)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Backstage](https://img.shields.io/badge/IDP-Backstage-9BF0E1?logo=backstage&logoColor=black)](https://backstage.io)

</div>

---

## About

StrawHat-Enterprise builds and maintains a portfolio of **production-grade platform components** for teams running on Microsoft Azure and Kubernetes. Our focus areas are:

- **Self-hosted CI/CD runner platforms** on AKS (ARC, GitOps, image baking)
- **Reusable Infrastructure-as-Code** modules and catalogs (Terraform / Bicep)
- **Internal Developer Platform** tooling powered by Backstage
- **Operational automation** — certificate lifecycles, fleet observability, and runner orchestration

Every public repository here is designed to be modular, opinionated, and ready to drop into a real environment.

---

## Featured Projects

### Self-Hosted Runner Platform

| Repository | Description | Stack |
| --- | --- | --- |
| [`actions-runner-helm`](https://github.com/StrawHat-Enterprise/actions-runner-helm) | Helm charts for GitHub Actions self-hosted runners on Kubernetes — integrates **ARC**, **External Secrets Operator**, and **cert-manager**. | Go · Helm · K8s |
| [`actions-runner-gitops`](https://github.com/StrawHat-Enterprise/actions-runner-gitops) | GitOps source-of-truth for runner fleets deployed to AKS. | Argo CD · Helm |

### Infrastructure as Code

| Repository | Description | Stack |
| --- | --- | --- |
| [`Azure-Catalog`](https://github.com/StrawHat-Enterprise/Azure-Catalog) | Curated catalog of reusable Terraform modules for common Azure landing-zone and workload patterns. | Terraform · Azure |
| [`InfraCreator`](https://github.com/StrawHat-Enterprise/InfraCreator) | Composable infrastructure scaffolding to bootstrap new Azure environments quickly. | Terraform |

### Developer Platform (Backstage)

| Repository | Description | Stack |
| --- | --- | --- |
| [`backstage-app`](https://github.com/StrawHat-Enterprise/backstage-app) | Backstage portal — software catalog, TechDocs, and golden-path templates. | TypeScript · Backstage |
| [`Backstage-helm`](https://github.com/StrawHat-Enterprise/Backstage-helm) | Helm chart to deploy Backstage on Kubernetes with sane defaults. | Helm |

### Automation

| Repository | Description | Stack |
| --- | --- | --- |
| [`cert-automation`](https://github.com/StrawHat-Enterprise/cert-automation) | Automated certificate issuance, renewal, and distribution workflows. | Python |

---

## Engineering Principles

- **Modular by default** — small, composable units over monoliths.
- **GitOps everywhere** — declarative state, reviewed via pull requests.
- **Secure supply chain** — pinned versions, signed artifacts, secrets via ESO / Key Vault.
- **Operate what you ship** — every component ships with observability and runbooks.
- **Documentation as a feature** — if it isn't documented, it isn't done.

---

## Getting Started

1. Explore the [repository list](https://github.com/orgs/StrawHat-Enterprise/repositories) to find a project that fits your use case.
2. Each repo includes its own `README.md` with prerequisites, deployment steps, and configuration reference.
3. Open an issue or discussion if you hit a snag — feedback shapes the roadmap.

---

## Contributing

Contributions are welcome across all public repositories.

- Fork the repository and create a feature branch (`feat/<scope>`).
- Keep PRs focused and include tests or validation where applicable.
- Follow the repository's `CONTRIBUTING.md` and code of conduct.
- Sign your commits where required.

---

## License

Unless otherwise specified within a repository, projects are released under the **MIT License**.

---

<div align="center">

<sub>Maintained by the StrawHat-Enterprise platform crew.</sub>

</div>
