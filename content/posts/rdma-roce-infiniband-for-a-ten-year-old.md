---
title: "RDMA, RoCEv2 and InfiniBand, Explained to a Ten-Year-Old (and to the New Grad on My Team)"
date: 2026-09-12T09:00:00-07:00
draft: false
tags: ["RDMA", "RoCEv2", "InfiniBand", "OCI", "Networking", "GPU", "Multiplanar", "HPC", "Infrastructure", "GB200"]
categories: ["Technical Deep Dive", "Cloud Infrastructure"]
summary: "What RDMA is, why InfiniBand and RoCEv2 are two roads for the same traffic, which one OCI drives on, and why OCI now gives every GPU four roads instead of one. Short, with pictures, no prior networking needed."
images:
  - /posts/rdma-roce-infiniband-for-a-ten-year-old/lead.png
---

![A robot arm passing packages between two glass-walled offices, a private train on its own track, and a network card sending four glowing lanes of traffic to a row of switches](/posts/rdma-roce-infiniband-for-a-ten-year-old/lead.png)

*2,609 words · 14 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Lead image generated with Grok. Figures 1 to 5 are my own drawings from public NVIDIA, InfiniBand Trade Association and Oracle documents. References at the bottom.*

**Related readings from this blog:**

- [The Complete NCCL Reference Guide](/posts/nccl-complete-reference-guide/) - the software that rides on the network described here
- [GPU Burn-In at Scale](/posts/gpu-burn-in-at-scale-reference-guide/) - how I test this network before I trust it
- [From First Principles to Zettascale](/posts/summary-gpu-oci-first-principles-blog/) - the OCI First Principles series this post leans on

## Why I Wrote This

Every new hire who joins OCI GPU usually asks the same question during their technical orientation week: what is RDMA, and why does it go by two different names, IB (InfiniBand) and RoCE (and RoCEv2)? Most people bring a WhatsApp intuition, where half a second of delay is fine. In AI/ML training, that same delay can cause a workload to slow down rapidly, and a slow workload on a few thousand rented GPUs is an expensive workload. The way we usually teach RDMA is by whiteboarding the architecture or pointing people to YouTube videos on RDMA. This post is a simplified version of that explanation, with illustrations. As with my previous guides on GPUs and NCCL, each section ends with an explanation suitable for a younger, less experienced audience. I use my own version of Einstein's line for everything I write: "If you can't explain something to your nana, you don't understand it." Readers who are already familiar with queue pairs can skip straight to the multiplanar section.

## The Twin Problem: Two GPUs, Two Houses

Due to memory constraints, large AI models can't fit on a single computer. They are distributed and partitioned across thousands of GPUs, which exchange learned parameters with each other during computation. The speed of this exchange is essential; if it is slow, thousands of GPUs sit idle, wasting expensive resources. Idle GPUs are the most costly inefficiency in large-scale training compute.

The architectural challenge arises because GPUs are located on separate servers within a rack, in different racks in a building, or even in different buildings. Within a server, GPUs communicate via NVLink, NVIDIA's proprietary high-speed copper interconnect. However, between servers (or racks), we need a fast network. Conventional Ethernet networks are not optimized for such fast traffic; they were designed for web traffic at their inception.

## RDMA: The Robot Arm

Traditional networking is like the postal service - slow but reliable. An application hands its data to the OS (operating system), which copies it and segments it into packets before sending them to the NIC (network interface card). When the packets reach the receiving NIC, it delivers them to the OS, which copies them again before notifying the application. This multi-step process involves redundant copying and constant CPU interruption on both ends [1].

RDMA, Remote Direct Memory Access, is the fix. RDMA is, by definition, direct memory access from the memory of one computer to another without involving either computer's OS [1]. The NIC transfers data directly into the remote system's memory, bypassing the OS altogether, which removes the redundant memory copies and the CPU interruptions on both sides. Figure 1 shows the process before and after RDMA.

![Figure 1: normal networking versus RDMA](/posts/rdma-roce-infiniband-for-a-ten-year-old/fig-01-post-office-vs-rdma.png)

**Two words you will hear in your first week.** A **queue pair** is the pair of mailboxes, one send and one receive, that each program keeps at its network card. Paul Grun's 2010 primer for the InfiniBand Trade Association calls it "one end of a channel" [2], and the NVIDIA programming manual says it is "roughly equivalent to a socket" [3]. Another RDMA concept is a **registered memory region**, a memory zone a program designates for a device to use. It's safe because the device is not allowed to touch anything outside that boundary.

**Explain it to a ten-year-old.** You and your friend live in different houses and share a box of Lego. The old way: you ask your mum, your mum walks next door, your friend's mum finds the piece, hands it over, your mum brings it back. RDMA: you both agree on one shelf, and a robot arm reaches through the window and puts the piece straight on it. The mums never get up.

## InfiniBand: Your Private Railway

RDMA is a conceptual approach that requires an underlying transport mechanism. InfiniBand was the first such implementation and has remained the leading solution for two decades.

InfiniBand was created in 1999 from the merger of two rival technologies, Next Generation I/O and Future I/O [2]. It is a networking architecture developed specifically to support RDMA with minimal transmission delay. IB uses dedicated cables, switches, and routing schemes, managed via a central subnet manager that configures routes through the network. The system is highly controlled and isolated from general-purpose networking.

IB link speeds have roughly doubled every three years: 200 Gb/s per link for HDR (High Data Rate) in 2018, 400 Gb/s for NDR (Next Data Rate) in 2022, and 800 Gb/s for XDR (eXtreme Data Rate) from 2024 [4]. Nearly all IB technology comes from Mellanox, which NVIDIA acquired in April 2020. Because of that acquisition, IB and NVIDIA Quantum switches are now practically synonymous.

**Explain it to a ten-year-old.** InfiniBand is a private railway built just for the Lego trains. One station master knows every track. No cars are allowed on it.

## RoCEv2: The Same Train on Public Roads

Because dedicated networks such as InfiniBand are costly and most data centers already utilize Ethernet, the InfiniBand community introduced RoCE (RDMA over Converged Ethernet) in 2010. This approach carries the InfiniBand transport header inside an Ethernet frame. The initial version of RoCE was limited to a single switch domain, as it could not traverse routers. In 2014, RoCEv2 addressed this shortcoming by encapsulating packets within standard UDP and IP protocols (using UDP port 4791), enabling routing across entire data centers [5]. Figure 2 compares the three encapsulation methods.

![Figure 2: InfiniBand, RoCE v1 and RoCE v2 packet stacks](/posts/rdma-roce-infiniband-for-a-ten-year-old/fig-02-three-envelopes.png)

There is one catch: RDMA assumes packets never get dropped because the card writes straight into memory and cannot afford to stop and ask. InfiniBand guarantees that by design. Ethernet does not. So a RoCEv2 network must be made lossless on purpose: a priority queue that pauses the sender rather than dropping (Priority Flow Control), and switches that mark packets when they start to queue up (Explicit Congestion Notification). The card slows down before anything is lost [5]. Get those knobs wrong, and the fabric is fine at 10 percent load and falls apart at 90.

**So how does InfiniBand actually guarantee no drops?** InfiniBand works on permission. Ethernet works on hope. On Ethernet, the sender just transmits. If the switch on the other end has no room, it drops the packet. PFC is a late fix: a pause message sent once the buffer is already almost full. On InfiniBand, the receiver tells the sender up front how much room it has, in units called **credits**, tracked separately per virtual lane so one slow traffic class can't starve the others. Each port advertises credits in 64-byte units; the sender counts them down as it sends and stops dead at zero, and as the receiver drains its buffer it hands more credits back [2]. A packet is only ever sent into space that is guaranteed to exist, so a buffer can never overflow, and no switch ever has a reason to drop it for congestion. This happens hop by hop across the whole fabric, so congestion turns into back-pressure that ripples toward the source instead of into dropped packets. Figure 5 puts the two side by side.

![Figure 5: InfiniBand credit-based flow control versus Ethernet send-and-drop](/posts/rdma-roce-infiniband-for-a-ten-year-old/fig-05-credit-based-flow-control.png)

| | InfiniBand | RoCEv2 (Ethernet) |
|---|---|---|
| Default behavior | Lossless | Lossy |
| How a sender knows it can transmit | Receiver hands out credits for free buffer space first | It doesn't; it just sends |
| What happens when a buffer fills | Can't happen; sender ran out of credits and stopped | Switch drops packets |
| Congestion signal | Built in: sender sees credits stop arriving | Bolt-on: PFC pause frames, ECN marks |
| Timing | Before the buffer is full, proactive | When the buffer is nearly full, reactive |
| Who configures it | Nobody, it's how the link works | You do, on every switch and NIC |
| Failure mode | Congestion spreads as back-pressure | Packets dropped, RDMA stalls or retransmits |

Two footnotes worth knowing. Bit errors can still corrupt a packet on the wire; InfiniBand's reliable transport (RC queue pairs) catches that with sequence numbers and retransmits, rare enough that the application never sees it. And lossless is not the same as congestion-free: back-pressure can still spread across the fabric, a pattern called tree saturation, which is why InfiniBand also carries its own congestion control, FECN and BECN marking, on top [2]. That is a performance mechanism, not a loss-prevention one.

**Explain it to a ten-year-old.** A credit is a receiver's promise of free space, handed out before anything moves, the way a restaurant only seats you when a table is free instead of letting everyone in and turning people away at the door. RoCEv2 runs the same Lego trains on the normal roads. To make it work, you paint a bus lane nobody else may use, and you put up traffic lights that turn amber early so the trains never have to crash.

## Which One, and Which One OCI Picked

| | InfiniBand | RoCEv2 |
|---|---|---|
| Runs on | Its own cables and switches | Ordinary Ethernet and IP |
| Who plans the routes | One subnet manager | Normal IP routing, or the NIC |
| Lossless | Built in | You configure it |
| Scale | Large, one subnet | As large as your IP network |
| Who sells it | NVIDIA | Everyone |

OCI chose RoCEv2 for its first cluster network, on NVIDIA ConnectX cards, and has stuck with it. Pradeep Vincent and Jag Brar wrote it up in the 2023 First Principles post: RoCE on ConnectX, a three-tier Clos fabric, lossless queues set aside for GPU traffic, and placement hints so a job lands on physically close GPUs [6]. The zettascale version of that fabric gives every GPU its own 400 Gb/s link and grows to 131,072 GPUs [7]. For GB200 NVL72 racks, OCI offers both NVIDIA Quantum InfiniBand and Spectrum-X Ethernet with RoCE as the scale-out network between racks, with NVLink doing scale-up inside the rack [8].

Why choose Ethernet when InfiniBand offers lower latency? At the scale of 100,000 GPUs, network design becomes primarily a supply chain and operational challenge rather than a latency issue. Ethernet provides a diverse vendor ecosystem, multiple switch chip options, and a large pool of experienced operators. Additionally, Ethernet carries both storage and management traffic. The marginal latency increase is offset by eliminating single-vendor dependencies.

## Multiplanar: Four Roads Instead of One

This section is especially significant because it introduces the first network design I have encountered that treats intermittent optical link failures as routine variability rather than critical outages.

In traditional network fabrics, each GPU's network card connects via a single high-bandwidth link to a leaf switch in a large three-tier Clos topology comprising thousands of switches operating under a unified routing protocol. This monolithic structure means that a single faulty switch, cable, congestion event, or software issue can impact all GPUs. Meta's research clusters demonstrated the cost of this approach: jobs running on 1,000 GPUs experienced interruptions approximately every eight hours [13].

OCI's Acceleron multiplanar design, presented by Pradeep Vincent, Jag Brar and David Becker in October 2025 and written up in March 2026, cuts the fabric into planes. In their words: "Each plane is an independent Clos fabric. Each fabric plane has independent data and control planes; there is no physical or logical 'fate sharing' between them" [9]. The GPU's 800G card does not send one 800G link to one switch. It sends four 200G links to four different switches, each on its own plane [9]. Figure 3 is the picture.

![Figure 3: a single-plane three-tier fabric versus four two-tier planes](/posts/rdma-roce-infiniband-for-a-ten-year-old/fig-03-one-plane-vs-four.png)

The gains of this approach are straightforward:

- **A fault stays in its plane.** If a plane "suffers a hardware fault, software issue, or congestion event, none of these issues impact the other planes" [9]. The card stops using the sick plane, and the job continues at three-quarters bandwidth instead of stopping. Figure 4 shows the same broken switch in both designs.
- **Fewer tiers.** Each plane carries only a quarter of the endpoints, so it fits in two tiers instead of three. Fewer hops mean lower, steadier latency. OCI's arithmetic: a 64-port 800G switch broken out four ways serves 256 endpoints at 200G each [9].
- **Maintenance without a window.** You can upgrade the switch software on plane 1 while planes 2, 3, and 4 carry the job, and even run different software versions on different planes [9].
- **The NIC drives.** Switches in one plane cannot see the other planes, so the routing brain moves to the edge. The card, with the host software, probes the paths and picks the plane for each packet [9].

![Figure 4: one switch fails in a single-plane fabric and in a multiplanar fabric](/posts/rdma-roce-infiniband-for-a-ten-year-old/fig-04-when-a-switch-dies.png)

The May 2026 follow-up explains how the NIC drives. OCI uses source routing over IPv6 segment routing: a central controller calculates many paths between every pair of cards and hands the lists to the hosts, and the card fails over to another list on its own, with no switch reconvergence [10]. On top of that sits Multipath Reliable Connection, MRC, which "extends the RDMA Reliable Connection model with multipath behavior" by spraying the packets of a single queue pair across all the paths and letting the card place them in memory out of order [10]. MRC itself was developed by OpenAI together with AMD, Broadcom, Intel, Microsoft, and NVIDIA; OCI is one of the places running it in production, under Stargate in Abilene [10].

OCI is not alone in reaching for planes. DeepSeek trained V3 on an eight-plane InfiniBand fabric, with one 400G card per GPU and one plane per card, and reported that it let them reach 16,384 GPUs on a two-layer fat tree, at the cost of extra latency whenever traffic had to cross planes inside the node [11]. NVIDIA showed its own Spectrum-X multiplane design at Hot Chips 2026, with eight 200G links from each card to eight different switches [12]. The difference at OCI is that the card does the cross-plane work, so the application never sees the planes.

**Explain it to a ten-year-old.** Instead of one big road to school, there are four small ones, and your bike can use all four at once. If one road is closed, you still get there, a bit slower. Every road has its own traffic lights, so a jam on one never blocks the others.

## What This Means When You Are Holding the Cable

From a burn-in perspective, multiplanar architecture redefines system-readiness criteria. Previously, readiness was determined by the network interface card being operational and passing a bandwidth test. Now, each of the four links must connect to its designated plane, each plane must be routable, and the bandwidth test must achieve full throughput with all four planes active, as well as three-quarters throughput with one plane disabled. Incorrectly connected cables may not cause immediate failures, leaving nodes that appear functional at reduced capacity until a workload requiring full bandwidth is assigned. A complete checklist for this process is in the [burn-in guide](/posts/gpu-burn-in-at-scale-reference-guide/).

## The Whole Post in Five Lines

**For the ten-year-old.** Computers used to pass notes through their parents. RDMA lets them pass notes straight to each other's shelf. InfiniBand is a private railway for the notes. RoCEv2 sends the same notes on normal roads with a bus lane. OCI gives every computer four roads so one closed road never stops the class.

## References

1. Wikipedia, Remote direct memory access: https://en.wikipedia.org/wiki/Remote_direct_memory_access
2. Paul Grun, Introduction to InfiniBand for End Users, InfiniBand Trade Association, 2010: https://network.nvidia.com/pdf/whitepapers/Intro_to_IB_for_End_Users.pdf
3. NVIDIA, RDMA Aware Networks Programming User Manual: https://docs.nvidia.com/networking/display/rdmaawareprogrammingv17
4. Wikipedia, InfiniBand (speed table and history): https://en.wikipedia.org/wiki/InfiniBand
5. Wikipedia, RDMA over Converged Ethernet (v1 versus v2, UDP 4791, PFC and ECN): https://en.wikipedia.org/wiki/RDMA_over_Converged_Ethernet
6. Pradeep Vincent and Jag Brar, First Principles: Superclusters with RDMA, Oracle, February 2023: https://blogs.oracle.com/cloud-infrastructure/superclusters-rdma-high-performance
7. Oracle, First Principles: Inside Zettascale OCI Superclusters, March 2025: https://blogs.oracle.com/cloud-infrastructure/first-principles-zettascale-oci-superclusters
8. Oracle, Behind the Scenes: Scale your NVIDIA GB200 NVL72 deployments with dedicated OCI APIs: https://blogs.oracle.com/cloud-infrastructure/behind-the-scenes-nvidia-gb200-nvl72-oci-apis
9. Pradeep Vincent, Jag Brar and David Becker, First Principles: Oracle Acceleron Multiplanar Networking Architecture, Oracle, March 2026, and the video: https://blogs.oracle.com/cloud-infrastructure/first-principles-acceleron-multiplanar-networking and https://www.youtube.com/watch?v=7Tqovn_5-DU
10. Pradeep Vincent, Andrew Dickinson, David Becker and Diptanshu Singh, First Principles: Unlocking Oracle Acceleron Multiplanar Fabric with Multipath Reliable Connection, Oracle, May 2026: https://blogs.oracle.com/cloud-infrastructure/first-principles-multipath-reliable-connection
11. DeepSeek, Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures, May 2025, section on the Multi-Plane Fat-Tree: https://arxiv.org/abs/2505.09343
12. ServeTheHome, NVIDIA Spectrum-X Ethernet Multiplane Network Architecture at Hot Chips 2026 (secondary): https://www.servethehome.com/nvidia-spectrum-x-ethernet-multiplane-network-architecture-at-hot-chips-2026/
13. Kokolis et al. (Meta), Revisiting Reliability in Large-Scale Machine Learning Research Clusters, HPCA 2025 (mean time to failure by job size): https://arxiv.org/abs/2410.21680
