---
title: "Resume"
draft: false
---

## Rik Kisnah

**Lead Principal Systems Software Engineer, AI/ML Infrastructure, Oracle Cloud Infrastructure (OCI)**  
Seattle, Washington, United States

> In God we Trust, all others bring data

**[Download PDF resume](/resume.pdf)** · [LinkedIn](https://www.linkedin.com/in/rikkisnah) · [GitHub](https://github.com/rikkisnah) · [Publications](/publications/)

---

## Summary

Infrastructure engineer with 20+ years building and operating production platforms, the last seven on GPU/HPC compute at fleet scale. Leads the OCI GPU Infrastructure team, owning rack-scale cluster design, the data plane, validation, fleet health, and repair automation for a fleet spanning NVIDIA H100, GB200/GB300 NVL72, and AMD accelerators across dozens of production regions.

Co-authored the engineering behind OCI's dedicated GB200 NVL72 rack-scale APIs. Works across the stack, from bare-metal and rack bring-up and RDMA/NCCL performance validation to the telemetry and fault classification that keep usable compute high across accelerator generations. Hands-on in Go and Python; comfortable across C/C++ systems code. Technical advisor to senior executives, public speaker, and author of a widely read body of writing on GPU infrastructure, NCCL, AI data centers, and AI-assisted engineering. Two pieces in particular, [The Complete NCCL Reference Guide](/posts/nccl-complete-reference-guide/) and [Attention Is All You Need: An Infrastructure Engineer's Guide](/posts/attention-is-all-you-need-and-all-you-need-to-know/), were well received across the industry and are used as working references by GPU infrastructure teams.

**Products delivered, chronologically:** Motorola phones, Aeroflex PXI, Amazon Kindle, AWS EC2 Windows, AWS WorkSpaces, AWS Load Balancers, Oracle Cloud Bare Metal, Oracle HPC/GPU.

---

## Core Skills

- **GPU / HPC infrastructure:** rack-scale cluster design and bring-up (NVL72), NVLink/NVSwitch fabric, PCIe, GPU hardware behavior
- **Networking:** RDMA / InfiniBand / RoCE, NCCL and collective performance, OSU and NCCL benchmarking
- **Fleet operations:** validation and acceptance criteria (multi-vendor, topology-aware), fault classification and repair orchestration, fleet telemetry and observability
- **NVIDIA / AMD / OEM technical interface:** firmware and driver interoperability, new-generation bring-up
- **Engineering:** Go, Python, C/C++, Terraform / infrastructure-as-code, CI/CD, DevOps/SRE
- **Leadership:** cross-org technical leadership, executive advising, public speaking, technical writing

---

## Experience

### Oracle Cloud Infrastructure

**Seattle, WA · Full-time · January 2019 – Present**

#### Lead Principal Systems Software Engineer
**June 2026 – Present**

- Leads the OCI GPU Infrastructure team, owning rack-scale cluster design, bring-up, validation, and fleet health for a heterogeneous NVIDIA H100, GB200/GB300 NVL72, and AMD fleet across dozens of production regions.
- Technical interface with NVIDIA and OEM hardware partners for new GPU generations: firmware and driver interoperability, NVLink/NVSwitch provisioning, and RDMA fabric validation for GB200/GB300 bring-up.
- Owns the validation and acceptance-criteria framework that gates every host before release: ~190 test definitions across three silicon vendors, topology-aware from single host through pair, full rack (18 trays / 72 GPUs), and multi-rack collectives, with performance thresholds set per shape and per fabric.
- Built rack-level dynamic completion criteria and partial-rack collective grouping, so one bad tray does not stall a rack of healthy ones.
- Owns the fault-classification and remediation path that routes production hardware failures to the right recipe automatically (rerun, soft reset, deep power cycle, repair script, ticket), cutting manual triage on a fleet where GPU failure rates materially exceed CPU rates.
- Delivered fleet-wide telemetry and observability for hosts and NVLink/NVSwitch fabric (health, port state, error counters, thermals, power), surfaced from single device up to region level.
- Built the diagnostics and repair-orchestration path that drains and repairs an individual host while jobs keep running on the rest of the NVL72 rack.
- Added an LLM-assisted triage tier behind deterministic rules: telemetry-grounded remediation suggestions with confidence-gated escalation to humans.
- Serves as technical advisor to senior executives on architecture and roadmap; drove the organization's AI-assisted engineering adoption program through executive review. Multiple patent and invention disclosures in GPU fault management and topology-aware AI systems.
- Delivers brown bag sessions and public presentations; high-volume Bar Raiser interviewer.

#### Consulting Member of Technical Staff
**August 2024 – June 2026**

- Tech lead for AI/ML infrastructure across OCI's HPC/GPU product line: control-plane APIs, host software, data-plane validation.
- Co-authored the engineering behind OCI's dedicated GB200 NVL72 rack-scale APIs, which launch, resize, monitor, and repair a full 72-GPU rack as a single unit, including firmware-version consistency enforcement across hosts, GPUs, and NVLink switches.
- Built a Go diagnostics CLI for GPU hosts (XID, clocks, ECC, NVLink, PCIe, RDMA checks against per-shape thresholds), packaged as RPM/DEB.
- Benchmarked H100 clusters at scale with OSU and NCCL collectives and published the methodology; maintains a public NCCL tuning and error-pattern reference for GB200, H100/H200, A100, and MI300X.

#### Principal Engineer
**January 2021 – August 2024**

- Tech lead for the OCI Compute HPC/GPU organization.
- Shipped the OCI HPC/GPU host plugins that run across all OCI GPU instances: RDMA configuration, GPU metrics collection, and fault detection, integrated with cluster networking up to 400 Gbps.
- Established the CI/CD practice the HPC/GPU organization uses to move host software from staging into production.

#### Principal Engineer (DevOps/SRE)
**January 2019 – December 2020**

- DevOps/SRE lead for OCI Compute: provisioning, deployment, monitoring, and operational tooling for [HPC](https://www.oracle.com/cloud/hpc/) and [Bare Metal](https://www.oracle.com/cloud/compute/bare-metal.html).

---

### Amazon Web Services

**Senior System Development Engineer**  
**Seattle, WA · December 2012 – December 2018**

- [Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/): built and operated automation for one of AWS's highest-traffic distributed services, where every change ships to a large, globally distributed, always-on fleet.
- Previously delivered [AWS WorkSpaces](https://aws.amazon.com/workspaces/), AWS EC2 Windows, and Amazon Kindle under strict regression and release-safety requirements.

---

### Aeroflex

**Principal Staff Development Engineer**  
**June 2010 – December 2012**

- Developed PXI application solutions for RF test of Qualcomm chipsets.
- Architected test solutions and provided pre-sales support for APAC customers.

---

### Motorola

**Senior Staff Software Engineer**  
**January 2002 – June 2009**

- Mobile device development and innovation (RAZR V3, ROKR E1, V70).

---

## Speaking & Thought Leadership

- **OCI Supercomputer Simplifies GPU Management for NVIDIA GB200 NVL72** — Oracle video feature, January 2026. [Watch](https://www.youtube.com/watch?v=opcct2z8SR0)
- **GB200 for OCI and AI Workloads** — Talk and demo to the National University of Singapore HPC community, August 2025. [Slides (PDF)](/HPC%20and%20AI%20Cloud%20on%20OCI.pdf) · [LinkedIn](https://www.linkedin.com/posts/activity-7363369400361443328-vTuJ)
- **HPC Cloud Builders: DevOps and Cloud Infrastructure** — Presentation to the Europe HPC community, September 2021. [Watch](https://www.youtube.com/watch?v=-OE_0cKbj40) · [Slides (PDF)](/Cloud_Builders_Devops_HPC.pdf)
- Regular brown bag sessions and internal talks on GPU infrastructure, NCCL, and AI-assisted engineering.

---

## Selected Publications

### GPU and AI infrastructure

- **[The Complete NCCL Reference Guide: Commands, Errors, and Troubleshooting for OCI GPU Infrastructure](/posts/nccl-complete-reference-guide/)** — rik-kisnah.ai, November 2025. NCCL commands, environment variables, error patterns, and per-shape tuning for GB200, H100/H200, A100, and MI300X. Well received across the industry and widely shared as a working reference.
- **[Attention Is All You Need: An Infrastructure Engineer's Guide](/posts/attention-is-all-you-need-and-all-you-need-to-know/)** — rik-kisnah.ai, February 2026. How the Transformer's quadratic attention cost drives KV-cache sizing, memory allocation, and interconnect design. Well received across the industry.
- **[GPU Burn-In at Scale: Commands, Gates, and Troubleshooting for NVIDIA and AMD Clusters](/posts/gpu-burn-in-at-scale-reference-guide/)** — rik-kisnah.ai, September 2026. Diagnostics, network validation, and acceptance gates for cluster commissioning across GB200, GB300, and MI355X.
- **[Zettascale Performance: OSU and NCCL Benchmarks on H100 AI Workloads](https://blogs.oracle.com/cloud-infrastructure/zettascale-osu-nccl-benchmark-h100-ai-workloads)** — Oracle Cloud Infrastructure Blog, November 2025.
- **[Behind the Scenes: Scale Your NVIDIA GB200 NVL72 Deployments with Dedicated OCI APIs](https://blogs.oracle.com/cloud-infrastructure/behind-the-scenes-scale-nvidia-gb200-nvl72-deployments)** — Oracle Cloud Infrastructure Blog, September 2025 (updated January 2026). Co-authored.
- **[From First Principles to Zettascale: How OCI's GPU/RDMA Architecture Redefines AI Infrastructure](/posts/summary-gpu-oci-first-principles-blog/)** — rik-kisnah.ai, October 2025.
- **[Three Weeks in Batam: Bringing NVIDIA GB200 to Life on the Data Plane](/posts/gb200-batam-data-plane-rollout/)** — rik-kisnah.ai, March 2025.
- **[Build the Data Centers](/posts/build-the-data-centers/)** — rik-kisnah.ai, July 2026. The economic case for AI data centers.
- **[The AI Pyramid: Five Layers Between Hardware and AGI](/posts/ai-pyramid-five-layers-between-hardware-and-agi/)** — rik-kisnah.ai, March 2026.

### AI-assisted engineering

- **[How to Make Agentic Coding Actually Work](/posts/how-to-make-agentic-coding-actually-work/)** — rik-kisnah.ai, March 2026.
- **[Content Engineering for AI Agents: Why Your Repository Isn't Ready](/posts/repos-not-built-for-ai-agents/)** — rik-kisnah.ai, January 2026.
- **[Your AI Strategy Is Read-Only](/posts/your-ai-strategy-is-read-only/)** — rik-kisnah.ai, June 2026.

### AI policy and society (Le Mauricien, Forum section)

- **[Mauritius Doesn't Need to Build Fable. It Needs an AI Pass.](https://www.lemauricien.com/opinions/mauritius-doesnt-need-to-build-fable-it-needs-an-ai-pass/)** — September 2026. [Blog post](/posts/mauritius-does-not-need-to-build-fable/)
- **[Will AI Eclipse Human Roles? A Mauritius Lens on Job Shifts and Societal Waves](https://www.lemauricien.com/le-mauricien/will-ai-eclipse-human-roles/693045/)** — December 2025.
- **[Mauritius at the Digital Crossroads: From Sugar Fields to Silicon Dreams](/posts/le-mauricien-article-2025/)** — November 2025.

Full list: [Publications](/publications/) · All posts: [Posts](/posts/)

---

## Education

- **Massachusetts Institute of Technology** — Postgraduate Certification, AI/ML, 2026
- **The University of Texas at Austin** — Postgraduate Certificate, AI/ML, 2019
- **University of Wales, Aberystwyth** — MSc, Computer Science (Neural Networks), 2007
- **Nanyang Technological University, Singapore** — BASc, Computer Engineering (Machine Learning), 2001

---

## Certifications

- AWS Solutions Architect
- Project Management Professional (PMP)
- Microsoft Certified Professional Developer (MCPD)
- Java Developer

---

## Languages

- **Native / bilingual:** English, French, French-based Creole
- **Conversational:** Mandarin, Bahasa Melayu
- **Elementary:** Hindi
- **Klingon** (just for fun)

---

*Last updated: September 2026*
