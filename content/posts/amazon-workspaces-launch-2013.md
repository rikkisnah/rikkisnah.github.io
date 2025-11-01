---
title: "Amazon WorkSpaces: The Birth of Desktop-as-a-Service"
date: 2013-11-15T09:00:00-07:00
draft: false
---

![Amazon WorkSpaces - Desktop as a Service](/posts/amazon-workspaces-launch-2013/workspaces_desktop_as_service.png)

Desktop-as-a-Service: rent a Windows desktop from AWS, get VPN-free remote work, no hardware to manage, pay per user per month.

## The Old Way vs. The New Way

**Traditional enterprise desktops:**
- Buy 10,000 PCs at $1,200 each = $12M upfront
- IT staff spends 60% of time maintaining them (disk space, updates, broken screens)
- Employee leaves? Reimage the machine, ship it to next employee
- Someone's laptop gets stolen in the airport—full data breach
- Employee works remote? Jittery VPN connection, laggy screen sharing, password resets

**WorkSpaces:**
- Employee gets a desktop in the cloud
- Connects via PCoIP (Teradici's remote display protocol)
- IT provisioning time: ~5 minutes (vs. 3 days for physical hardware)
- Employee leaves? Terminate the workspace in 1 click
- Stolen laptop? Nothing on it; data stays in the cloud

## What We Built

Two hardware SKUs:
- **Graphics Bundle**: Dual-core, 2GB RAM (office work: email, Word, Slack)
- **Standard Bundle**: Quad-core, 4GB RAM (dev, design, heavier apps)

Connected via **PCoIP** (Teradici's proprietary remote desktop protocol—way better compression than RDP). Each workspace lived as an EC2 instance in the customer's own VPC, synced with their Active Directory.

## The Challenges

We launched *limited preview* because we knew we'd shipped 20% of a complete product:

- **Printing didn't work** (corporate users *need* printers)
- **GPU apps failed** (no GPU in the bundle options)
- **Network latency sucked** for high-latency connections (PCoIP was optimized for <20ms RTT)
- **Application quirks** (some Windows apps misbehaved over remote display)
- **Compliance missing** (HIPAA, PCI-DSS frameworks not yet built)

But the core idea was proven: **you can rent a desktop from AWS.**

## Market Reaction

Enterprise IT was polarized:
- **The believers**: "We can fire half our hardware team and provision desktops in minutes."
- **The skeptics**: "Desktops over the internet? Latency nightmare. And what about compliance?"

Pilots landed with healthcare, finance, and remote-heavy startups. Average deployment: 50–500 workspaces per pilot customer.

## The Insight

By 2013, AWS had proven you could rent compute, storage, databases. WorkSpaces proved you could rent *human-facing infrastructure.* The cloud wasn't just for servers—it was for everything.

This planted a seed: WorkSpaces, WorkDocs (cloud storage for teams), and AppStream (stream any Windows app) eventually became a coherent strategy. Enterprises didn't just move their servers to AWS; they moved their entire end-user infrastructure.

Later, when COVID hit in 2020, every enterprise that had kicked WorkSpaces tires suddenly needed it urgently. We shipped more workspaces in Q1 2020 than in the previous 5 years combined.

