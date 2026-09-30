---
title: "Design an Analytics Dashboard for an AI Chat App"
date: 2026-02-24T09:00:00-08:00
difficulty: "Medium-hard. The data-infrastructure round in product clothing, with a privacy rule that decides the storage"
tags: ["Systems", "Analytics", "Data Infrastructure", "Kafka", "Streaming", "Privacy", "GDPR", "Alerting", "LLM"]
summary: "Three audiences want to watch one chat product: engineers want p99 and GPU utilisation in seconds, product wants retention and revenue by plan, support wants a user's timeline without ever seeing the chat. Design the event stream, the rollups, the three alert tiers, and the token that lets you erase a person without erasing the trends."
mermaid: true
draft: false
---

## The question

Design an analytics dashboard for an AI chat application at ChatGPT or Claude scale, so Product, Engineering and Support can monitor system health, user behaviour and business performance in near real time.

The product words hide a data-infrastructure question: ingest, process and serve large-scale data to stakeholders with different needs and different sensitivities. The pipeline is the same one you would build for fleet telemetry. What is specific here is three personas with three freshness targets, a rule that chat content is never stored, and a regulator who can ask you to forget a person.

## Clarify first

Three metrics per persona, and how fresh each must be: seconds for health, minutes for behaviour, daily for business. Scale in one line: daily active users and messages per user. May we store chat content? No, and say it before they ask. How long may we keep events? Warm for a year, cold beyond. Which regulations: erasure under GDPR with a deadline, and support views that must satisfy HIPAA.

Then the sentences. Engineering can see per-model p50 and p99 latency, error rate per minute, model usage, queue depth and GPU utilisation, and can define alerts. Product can see daily and weekly active users, session length, retention, thumbs up and down, and revenue and usage by plan. Support can open a per-user timeline of sessions and errors without seeing a word of chat.

The technical challenges are the sentences that decide the design. Analytics must never degrade the chat path, so every emit is fire-and-forget and analytics is shed before a request is. Dashboards refresh in one to five seconds; the sub-50 ms figure people quote belongs to the serving query on hot rollups, not the pipeline. Identity is a token that can be shredded, so erasure keeps the aggregates. And the numbers: thirty million daily users sending twenty messages with five events each is three billion events a day, about 35,000 a second on average and 150,000 at peak, a terabyte a day raw.

## Explain it to a ten-year-old

A stadium has thousands of turnstiles. Every time one clicks, it drops a ticket stub into a chute. The stubs slide onto one long conveyor, and three clerks stand beside it: one counts stubs per minute and shouts if the rate drops, one sorts them into boxes by gate and hour for the manager's weekly report, and one files them in a warehouse in case someone asks about last year. The stubs carry a locker number, never a name. If a fan asks to be forgotten, you throw away the card that says which locker was theirs. The stubs stay, the counts stay, but nobody can say which ones were that fan's.

## Entities, then the API

Write the event record in full; it is the answer to "how do event systems structure a record".

- **Event**: event id (time-ordered UUID), type, schema version, event time and ingest time, source service, session id, user token, request id, then the dimensions (model, region, plan, client version), the measures (latency, tokens in and out, status), a per-type attributes map, and a sensitivity tag per field. Immutable, the source of truth.
- **Session**: session id, user token, start, end, client, origin.
- **PrivacyToken**: user id to token, with a per-user key, created and revoked timestamps. Analytics never stores the user id.
- **Rollup**: metric, window (one second, one minute, one hour, one day), dimensions, count, sum, p50 and p99 sketches, watermark.
- **Dashboard** (audience, widgets) and **AlertRule** (metric, condition, window, group by, tier, channel, escalation).

Not entities: the chat message, which is never stored here, and the GPU, which is a dimension on an infrastructure event.

The API is one endpoint per need. Events in, as a batch, always accepted, idempotent on event id. Metrics out, by metric, dimensions and window, from a cache. A session timeline for support behind role checks and an audit log. Dashboards and alert rules as resources. And one endpoint that deletes a user's privacy token, which is the erasure mechanism.

## The answer

1. **One event, end to end.** A service emits an event carrying the user's token. The collector buffers five to ten milliseconds, batches, validates lightly and writes to an ingest topic, partitioned by session, with a single acknowledgement. A stream processor checks the schema, dedupes on event id, computes one-second and one-minute rollups with percentile sketches, handles late events with watermarks, and publishes rollups and enriched events to one output topic. Three consumers read that topic independently: a real-time consumer holds the latest values in memory and feeds the dashboard API, which pushes over a socket; a database writer lands rollups in a hot store that serves filter, sort and history; a cold writer lands raw events (from the ingest topic) and rollups in the lake, warm for a year and cold beyond. One alert evaluator per tier reads the real-time consumer, the hot store or the lake. The point of the topic between processor and sinks: one seam, each sink at its own pace and replayable, and a slow lake write can never back up the processor.
2. **Isolation.** The emit is asynchronous with a local buffer. Under pressure the collector drops analytics, never a chat request. The dashboard's availability is its own: if the OLAP store is down, chat does not notice.
3. **Real time, honestly.** Ingest: client batching with a short flush, gRPC to a collector in the same region, an in-memory ring buffer, Kafka with one acknowledgement, no synchronous validation on the hot path. Serve: rollups held in memory, incremental streaming windows, materialised views, push instead of polling. End-to-end freshness is one to five seconds. Under 50 ms is the serving query.
4. **Privacy that survives erasure.** The options and why they lose: scrubbing personal data with patterns at write time is brittle; hashing the user id with one global salt is reversible and cannot be erased; deleting rows on request destroys the aggregates. The answer is a per-user token derived from a per-user key. Analytics stores only the token. To erase a person, delete the key: every row becomes unattributable within the deadline, and the counts and trends stay. The goal is non-attributability, not protection from an insider who holds the vault. Chat content is never emitted, fields carry sensitivity tags, retention is tiered, and a compliance job scans the lake for anything that slipped through, raises tickets and drives deletions.
5. **Alerts.** Rules over rollups, evaluated on a schedule that matches the tier; grouped by dimension; thresholds and baseline anomalies; dedupe and grouping so one incident is one page; silences; severity and escalation; routed to pager, chat, email or ticket.
6. **Three tiers, three evaluators.** Under ten seconds: streaming evaluation on one-second rollups straight from the stream processor, to a pager, for p99 latency and error rate per model. Under sixty seconds: one-minute rollups in the hot store, evaluated every fifteen seconds, to chat and on-call, for GPU utilisation and queue depth. Under a day: batch jobs on the lake, to email and tickets, for retention, revenue drift and cost. Separate evaluators, so a slow lake query can never delay a page.
7. **What Anthropic adds.** Sensitivity classes with row and column policies at the serving layer and an audit trail on every support lookup. Workload isolation so an ad-hoc scan does not stall the on-call dashboard. Bad-data blast radius handled by quarantine, versioned mappings and a re-run over the lake. A cardinality budget per metric that pages someone when crossed.

## The board

The pipeline runs across the top; the output topic and its three consumers sit in the middle, with the dashboards on the left; the hot store, the lake, the evaluators and the compliance module sit below. Solid arrows are the event and query path; dashed are control, schemas, history and the raw feed into the lake.

{{< excalidraw id="NwUIiRIJH89tGbNIXzte" png="/teach/systems/chat-analytics-answer-board.png" title="Analytics dashboard for an AI chat app, the answer" src="/teach/systems/chat-analytics-answer-board.excalidraw" >}}

[Download the one-page cheat sheet](/teach/systems/chat-analytics-cheat-sheet.pdf) (A4, two sides: front is what to ask and what to design in order, back is this board).

## What goes wrong in the room

- **Entities and storage, but no path.** A board with Event, Session and a warm/cold sketch, and nothing between the services and the dashboard. Draw the collector, the log, the stream processor and the rollup store before anything else.
- **Alerts as a table with tiers and no machinery.** Say who evaluates, how often, against what, and where it routes.
- **Numbers left as adjectives.** "Tens of millions of users" has to become events per second and bytes per day within the first five minutes.
- **Promising 50 ms end to end.** Scope it to the serving query and say the pipeline is seconds.
- **Erasure by deleting rows.** It answers the regulator and destroys the trends. Shred the key.

{{< remember >}}
- **Three personas, three freshness targets**: seconds, minutes, daily.
- **Fire-and-forget emit; shed analytics before chat.** Isolation is a requirement, not a nicety.
- **The event envelope**: ids, both timestamps, source, schema version, correlation ids, then dims, measures, attributes, sensitivity tags.
- **Roll up early, then one output topic and three consumers**: real-time push, the queryable store, the lake.
- **Per-user token, crypto-shredding.** Erasure deletes the key; aggregates survive.
- **One evaluator per alert tier**: under 10 s from the stream, under 60 s from the hot store, under a day from the lake.
- **3B events a day is 35k a second, 150k at peak, a terabyte a day raw.**
{{< /remember >}}

## Go deeper

- [Design a Telemetry Platform](/teach/systems/design-a-telemetry-platform/) is the same pipeline with the metric-name follow-up; the schema registry is shared.
- [Design a Metrics Pipeline](/teach/systems/design-a-metrics-pipeline/) for the rollup and sketch mechanics.
- [Design a Token Usage and Limits Service](/teach/systems/design-a-token-usage-and-limits-service/) produces the usage event that feeds revenue by plan.
- The [CloudEvents specification](https://cloudevents.io/) and [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) for the event envelope; the [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) docs for grouping, silencing and routing.

**With AI on the table.** The assistant will produce Kafka, Flink, ClickHouse and a lake in one breath. I ask it to erase one user and show me what happens to last quarter's retention chart, then ask you why the token beats the hash. The tool knows the components. You have to know the key.
