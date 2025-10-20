---
title: "Three Weeks in Batam: Bringing NVIDIA GB200 to Life on the Data Plane"
date: 2025-03-15T10:00:00-07:00
draft: false
tags: ["gb200", "batam", "data-plane", "infrastructure", "nvidia", "oci", "2025", "indonesia"]
---

Three weeks in Batam, Indonesia in March 2025. Not a vacation - something far more meaningful. I was there to help bring the NVIDIA GB200 data plane to life, working alongside some of the brightest minds at OCI and NVIDIA. This was the moment where cutting-edge technology meets real-world infrastructure, and I got to be part of making it happen.

**Related readings:**
- [Behind the Scenes: NVIDIA GB200 NVL72 on OCI APIs](https://blogs.oracle.com/cloud-infrastructure/post/behind-the-scenes-nvidia-gb200-nvl72-oci-apis) - Technical deep dive on the NVIDIA GB200 and OCI integration
- [Supercluster: NVIDIA Blackwell Dedicated Alloy](https://blogs.oracle.com/cloud-infrastructure/post/supercluster-nvidia-blackwell-dedicated-alloy) - OCI's Supercluster offering with Blackwell GPUs
- [Nvidia GB200 NVL72 Now Available via Oracle Cloud](https://www.datacenterdynamics.com/en/news/nvidia-gb200-nvl72-now-available-via-oracle-cloud/) - Data Center Dynamics coverage of the launch

## The Mission: Time to Market

When I arrived in Batam, the pressure was real. GB200 was new. NVIDIA's latest breakthrough in GPU technology. OCI was committed to being first to market with it. And the data plane - the critical infrastructure layer that handles every packet, every connection, every byte moving through these machines - needed to be battle-ready.

This wasn't about perfection on day one. It was about **learning, shipping, and adapting**. Three weeks to validate, test, troubleshoot, and deploy infrastructure that would handle the most demanding workloads in Asia-Pacific.

## The Reality of New Technology

Working with GB200 felt like frontier work. The technology was cutting-edge, but that meant we were often in uncharted territory:

- **Documentation was incomplete** - We were sometimes writing the playbook as we went
- **Edge cases appeared constantly** - New hardware reveals new problems
- **Collaboration was critical** - Every issue required bringing NVIDIA engineers, OCI architects, and our data plane team together
- **Real-time problem-solving** - We couldn't wait for release cycles; we needed answers in hours

There's something electric about that kind of work. You're not maintaining a system; you're building it. You're not following a checklist; you're writing the checklist.

## The Data Plane Perspective

My focus was on the data plane - the networking and compute substrate that sits between the hardware and the applications. This is where microseconds matter. This is where efficiency directly translates to customer performance and cost.

We faced questions that only real deployment could answer:
- How does GB200's architecture affect packet flow and latency?
- Where are the bottlenecks in our current stack?
- What optimizations unlock the performance these GPUs promise?
- How do we scale this reliably across multiple machines?

Each day brought new insights. Some came from elegant solutions. Others came from failures that taught us more than successes ever could.

![NVIDIA GB200 NVL72 Rack System](/posts/gb200-batam-data-plane-rollout/gb200_hero.png)
*The NVIDIA GB200 NVL72 - 36 Grace CPUs and 72 Blackwell GPUs in a single liquid-cooled rack*

## Working with the Best

The team in Batam represented the pinnacle of expertise. NVIDIA engineers who designed the architecture we were deploying. OCI architects with years of experience running hyperscale infrastructure. Each person brought a deep specialization, but the magic happened when those specializations intersected.

Conversations that started with "Why is this latency spike happening?" would pull in network engineers, GPU specialists, and systems architects. Within hours, we'd have root cause analysis and be testing fixes. The knowledge transfer was constant - I learned as much from watching others problem-solve as I did from solving problems myself.

## Three Weeks That Mattered

By the end of three weeks, we had:
- Validated the data plane against real workloads
- Identified and fixed critical bottlenecks
- Established monitoring and alerting that would catch future issues
- Built confidence that this infrastructure was ready for customers

Not every deployment challenge was solved, but we had momentum. We had patterns. And we had a team that understood the system deeply enough to adapt when new problems emerged.

![OCI Supercluster with NVIDIA Blackwell](/posts/gb200-batam-data-plane-rollout/oci_supercluster.png)
*OCI's state-of-the-art infrastructure combining NVIDIA Quantum-2 InfiniBand networking with GB200 systems*

## The Lesson

This experience reinforced something I've learned throughout my career: **breakthrough infrastructure comes from diverse expertise executing under pressure with clear purpose**. We weren't perfect. But we were focused. We learned fast. We shipped.

Batam became more than just a data center location for me - it became a reminder that real technology work means getting into the details, working with exceptional people, and being willing to learn something new every single day.

The GB200 is now deployed in OCI's Batam region. Every deployment, every AI workload, every inference that runs there benefits from the three weeks we invested in getting the data plane right.

That's infrastructure that matters.

