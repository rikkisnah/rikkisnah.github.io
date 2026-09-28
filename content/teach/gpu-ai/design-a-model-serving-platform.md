---
title: "Design a Model Serving Platform with Versions and A/B Tests"
date: 2026-01-20T09:00:00-08:00
difficulty: "Hard. Two planes that must meet in one picture, and a clock that punishes slow set-up"
tags: ["GPU", "Inference", "Serving", "Versioning", "A/B Testing", "Rollouts", "Multi-Region", "Infrastructure"]
summary: "A hundred models from a hundred megabytes to a hundred gigabytes, clients on every continent, and product teams who want to ship version eight to ten percent of traffic tonight. Design the platform that stores the versions, gets them onto GPUs, splits the traffic, and never loads a model while a client is waiting."
mermaid: true
draft: false
---

## The question

Design a platform that stores and runs machine learning models of very different sizes, with versioning and A/B testing. Clients call it from around the world. Think of the models behind a maps product: one for routing, one for weather, one for arrival times.

It sounds like a product question. It is an infrastructure question with three parts that must fit on one page: a **control plane** that knows which versions exist and how traffic should split, a **deployment plane** that gets the bytes onto GPUs and says when a replica is ready, and a **data plane** that routes a request to a ready replica, batches it, and streams the answer back. Interviewers grade the fit between the three more than any one of them.

## Clarify first

Five minutes, no more. Ask, in this order:

- **Who calls, and what is one call?** Apps and services, request and response for small models, a stream for token models.
- **How many models and what sizes?** A hundred models, from 100 MB to 100 GB. The size spread is the whole design: a small model fits many times on one GPU, a large one needs several GPUs and minutes to load.
- **Latency per class, peak load, regions?** p99 of 100 ms for small models, 10,000 requests a second at peak, three regions, a request should stay in its region.
- **What does A/B mean here?** A percentage split between two versions, sticky per user or per customer, and a canary is just an arm with a small weight.
- **What does "rollout done" mean?** Serving capacity on the new version, not bytes on disk.

Then say the sentences. An engineer can register a model, upload a version, deploy it to a pool in a region, run an experiment between two versions, and roll out or roll back. A client calls one stable endpoint per model and gets a result from whichever version the rules choose. Operators see per-version and per-arm health.

And the technical challenges, which are the sentences the interviewer actually listens for: sizes differ a thousandfold; loading a large version takes minutes so it must never happen on the request path; one registry serves global clients, so routing rules may be seconds stale but a call must never fail because the registry is down; A/B assignment must be a cheap sticky hash on the hot path; the GPU is the expensive part, so batching and bin-packing decide the bill; availability wins on the inference path, consistency wins in the control plane.

## Core entities, then the API

Six records. Say them as a list first, fill in fields later.

- **Model**: id, name, owner, and an alias map such as `prod → v7`, `canary → v8`.
- **ModelVersion**: model, version, artifact location, checksum, size, GPU memory needed, status. Immutable once uploaded.
- **Deployment**: version, region, pool, replica count, GPU class, generation, status.
- **Experiment** and **Arm**: which model, the arms with their versions and weights, the assignment key (user or customer), pinned customers, stop criteria.
- **Replica**: node, GPUs, version, and a state machine: pulling, loaded, warm, ready (with the version and the generation it was reached under), serving, draining.

Not entities: the request, which is metered but not stored; the batch, which is a runtime grouping; the region, which is a partition key on everything else.

The API follows the requirements one to one. `POST /models` and `POST /models/{id}/versions` (returns a signed upload URL, then a validation step). `POST /deployments` with version, region, replicas, GPU class and a canary percentage. `POST /experiments` with the arms and the key. `POST /rollouts/{id}/pause`, `resume`, `rollback`. For clients, one endpoint: `POST /v1/models/{name}:predict` with the inputs, an optional version or alias, and an optional user key; the response carries `served_version` and `arm` so the experiment log can join later. Internally, replicas report `{generation, version, state}` and routers watch a per-model rules snapshot.

## The answer

1. **Deploy path first, because it explains why the request path is simple.** An engineer registers version eight. The weights land in an object store with a checksum, mirrored to every region before anything else happens. The deployment controller picks nodes: bin-pack by GPU memory with headroom for activations, topology-aware so a multi-GPU model sits on GPUs that share NVLink. It assigns a generation number to the rollout. On each node an agent pulls the weights in chunks, verifies every hash, caches on NVMe, loads into GPU memory, runs warm-up prompts, and reports ready with the version and the generation. Only then does the controller add the replica to the ready set and publish routing rules: canary ten percent to version eight. Routers pick up the new snapshot within seconds.
2. **Request path.** A client hits the nearest region through anycast. The gateway authenticates, checks quota, and meters usage. The inference router resolves the alias to a version, then the experiment arm with a sticky hash of the user or customer key and the experiment id, then a ready replica for that version in this region. The request goes to a per-version queue; the batcher flushes on size or time and never mixes versions in one batch; the GPU runs the batch; the result streams back the same way with the served version stamped on it. Metrics and the experiment log are emitted asynchronously. If this region has no ready replica for the chosen version, the router fails over to the next region and pays the latency rather than cold-loading a model or returning an error.
3. **The sum, out loud.** Small model, batch of 32 every 10 ms: 3,200 requests a second per GPU, so 10,000 a second needs four GPUs; run six for headroom and a canary. Large model, 100 GB of weights: 80 seconds to pull at 10 Gbit/s, about 20 seconds from NVMe into GPU memory, plus warm-up. A version switch is minutes, which is why it lives entirely in the control plane and why the pools keep ten percent warm spare capacity.
4. **Where the GPU optimisations live on the board.** Do not list them; place them. Bin-packing and topology-aware placement live in the deployment controller. Quantisation to FP8 or INT8 is a property of the ModelVersion and halves the GPUs for the models that tolerate it. Tiered GPU classes are a Deployment field. Dynamic batching with a latency budget lives in the batcher, and the queue depth in front of it is the utilisation dial: aim for seventy percent so bursts do not blow the tail. Autoscaling reads queue depth and GPU utilisation and scales to warm, never to zero, for anything large. The trade-off in one sentence: latency against utilisation, and queueing is the lever.
5. **A/B correctness.** The assignment hash is stable across requests and regions. Arm weights change only through the control plane. Analysis reads the experiment log, which joins request id to arm and version, never the router's memory. Canary stop signals are per arm: error rate, p99, and a quality metric. When one trips, the controller pauses or rolls back, and a rollback is a new generation: rules revert, version eight replicas drain, and a late "ready" from the old generation is ignored.
6. **Multi-tenancy.** One version per replica, so tenants never share weights or memory. Per-model queues, so a slow large model cannot starve a fast small one. Per-customer quotas at the gateway. Load shedding by tier when a queue exceeds its latency budget. No GPU memory oversubscription.
7. **Multi-region.** The registry is single-writer with asynchronous read replicas. Routers cache the rules snapshot with a last-known-good fallback, so a registry outage stops changes but not inference. Artifacts are mirrored before a deployment starts. This is the answer to "consistency or availability": consistent in the control plane, available on the request path, and say it in exactly those words.

## The board

The request path is numbered and comes back to the client. The deployment plane sits above it and meets it at the router. Every data-plane box feeds observability, and the canary stop signals go back to the controller.

{{< excalidraw id="ow54pKycwLbNzjpCb0QE" png="/teach/systems/model-serving-platform-answer-board.png" title="Model serving platform with versions and A/B, the answer" src="/teach/systems/model-serving-platform-answer-board.excalidraw" >}}

[Download the one-page cheat sheet](/teach/systems/model-serving-platform-cheat-sheet.pdf) (A4, two sides: front is what to ask and what to design in order, back is this board).

## What goes wrong in the room

- **The high-level design lands at minute thirty.** Requirements took eleven minutes, entities another ten, and the follow-ups never happened. Target: the board complete by minute fifteen. Practise the set-up on standard problems until it is automatic, then spend the saved minutes on scale, observability and isolation.
- **Three sketches instead of one.** A request-flow drawing, a control-plane-versus-data-plane drawing, and a deployment-pipeline drawing are all correct and all useless separately. The interviewer needs the picture where the planes meet.
- **Naming optimisations without applying them.** "Bin-pack by GPU memory, topology-aware, quantise, warm pool" is a list. The answer is "bin-packing lives in the controller and is why the large model fits on four GPUs instead of five".
- **Answering a follow-up before stating its goal.** Condense "how would you optimise GPU resources" into "latency against utilisation, and I will use the queue to trade one for the other" before touching the board.
- **Life of a request that stops at the router.** Draw the way back. The result has to reach the client, and the served version has to reach the experiment log.

{{< remember >}}
- **Three planes, one page.** Control plane decides, deployment plane makes replicas ready, data plane routes and batches. They meet at the router.
- **Never load on the request path.** Warm pool, NVMe pre-placement, fail over to another region instead of cold-starting.
- **Ready means the exact version under the current generation.** Rollback is a new generation.
- **Sticky hash for arms, experiment log for analysis.** The router's memory is not a record.
- **Consistent control plane, available data plane.** Rules seconds stale are fine; a failed call is not.
- **Batch 32 every 10 ms is 3,200 requests a second per GPU.** 100 GB at 10 Gbit/s is 80 seconds, plus 20 to reach GPU memory.
{{< /remember >}}

## Go deeper

- [Design an Inference API](/teach/gpu-ai/design-an-inference-api/) is the data plane of this platform with the batching maths worked through.
- [Design Model Weight Distribution](/teach/gpu-ai/design-model-weight-distribution/) is the deployment plane: how 100 GB reaches a thousand nodes and how readiness is gated.
- [Design a Distributed Job Scheduler](/teach/systems/design-a-distributed-job-scheduler/) is the drill for getting from prompt to board in fifteen minutes; its two-layer pattern (durable store plus in-memory queue) is the same shape as the rollout controller here.
- NVIDIA's [Triton model repository and versioning](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html) and KServe's [canary rollouts](https://kserve.github.io/website/latest/modelserving/v1beta1/rollout/canary/) are the production versions of the version and arm records.

**With AI on the table.** The assistant will produce the three planes as three tidy diagrams in a minute. I ask it to put them on one page with the request path numbered and the result returning, then ask you where the queue depth should sit and why seventy percent. The tool draws the boxes. You have to know which one the trade-off lives in.
