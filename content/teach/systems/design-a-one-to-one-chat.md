---
title: "Design a One-to-One Chat"
date: 2026-04-21T09:00:00-07:00
difficulty: "Medium. The prompt is three words long; the round is about what you ask next"
tags: ["Systems", "Chat", "WebSockets", "Presence", "Kafka", "Redis", "Real-Time"]
summary: "One-to-one, text only, web only. That is all the interviewer gives you. Ask for the rest, then design the gateway that finds the recipient, the inbox that survives them being offline, the presence key that expires on its own, and defend Redis Pub/Sub against Kafka out loud."
mermaid: true
draft: false
---

## The question

Design a messaging app. Requirements: one-to-one, text only, web app only. Anything else you want to know, ask.

That is a real opener and it is a test of requirement gathering before it is a test of architecture. The numbers you should extract, or propose if the interviewer shrugs: 100 million daily users, ten messages each per day, delivery under half a second, 99.9 percent available, single device to start, history kept.

## Explain it to a ten-year-old

A school has thirty classrooms and one post room. Every child sits in a classroom with a walkie-talkie. To send a note to a friend, you hand it to your teacher. The teacher writes it in the school ledger, drops a copy in the friend's pigeon hole, and calls the friend's classroom on the radio. If the friend is in class, their teacher reads it out straight away and the pigeon-hole copy is thrown away. If the friend is off sick, the note waits in the pigeon hole until they are back. The trick is knowing which classroom the friend is in without asking every teacher: each child's name maps to one classroom by a fixed rule.

```mermaid
sequenceDiagram
  participant A as Client A
  participant G1 as Gateway 1
  participant S as Stores (Messages, Inbox)
  participant P as Redis Pub/Sub
  participant Gk as Gateway k (owns B)
  participant B as Client B
  A->>G1: send(msg, client_msg_id)
  G1->>S: persist message, write Inbox row for B
  G1->>P: publish on channel:B
  P->>Gk: deliver (Gk subscribed for B)
  Gk->>B: push over WebSocket
  B-->>Gk: ACK
  Gk->>S: delete Inbox row
```

## The trick

Two ideas carry the design. First, a **consistent hash from user id to gateway**, so the sender's gateway knows which gateway holds the recipient's socket without broadcasting. Second, an **Inbox table as the durability backstop**: write the message and the recipient's inbox row before publishing, delete the row on acknowledgement. Because the inbox exists, the fan-out bus can be at-most-once and fast. That single decision is what lets you defend Redis Pub/Sub against Kafka.

## The steps

1. **Ask.** Load, peak, latency, delivery guarantee, ordering, offline behaviour, retention, devices. Write the numbers on the board: 1 billion messages a day is about 11,600 a second average and 35,000 at peak; 10 million concurrent sockets at about a million per gateway is ten gateways; 200 bytes a message is 200 GB a day.
2. **Connection layer.** WebSocket over TLS, because both sides push. A layer-4 balancer is enough. Each gateway keeps an in-memory map from user id to socket.
3. **Finding the recipient.** Consistent hash on user id to pick the owning gateway; a coordination store (etcd or ZooKeeper) holds the ring so all gateways agree. When a gateway dies, only its slice of users reconnects elsewhere.
4. **Send path.** Persist the message in a wide-row store keyed by conversation id, write an inbox row for the recipient, publish on the recipient's channel. The owning gateway is subscribed and pushes to the socket. The client acknowledges; the gateway deletes the inbox row.
5. **Presence.** A Redis key per user with a TTL of twice the heartbeat interval, refreshed by the gateway on every ping (10 to 30 seconds, 5 second pong deadline). Offline is the key expiring. Do not write "last seen" per heartbeat: at scale that is 20 million writes a second.
6. **Offline delivery.** The recipient reconnects, reads their inbox, fetches the bodies, acknowledges, rows are deleted. Exactly-once from the client's point of view comes from deduplicating on the client message id.
7. **Ordering.** Per conversation, with server-issued monotonic ids. Global ordering is a trap; say so.
8. **The bus.** Redis Pub/Sub: a channel is a pointer to sockets, single-digit milliseconds, no per-channel metadata. Kafka: durable and replayable, tens of milliseconds with all acks, and roughly 50 KB of metadata per topic, so topic-per-user at a billion users is 50 TB of metadata. Choose Redis for fan-out and keep Kafka only if hours of replay is a hard requirement. Be ready for the Kafka internals follow-up anyway: partition as an ordered log, consumer groups and rebalance, replication and in-sync replicas, leader election, log compaction.
9. **Sharding.** Many small conversations per user: shard by user id. Few huge conversations: shard by conversation id. Hybrid above a participant threshold.
10. **Second device.** Scope the inbox by recipient and client id so each device acknowledges separately; cap devices per account.

## The board

{{< excalidraw id="IUUDFoX6KzAS1HryeN3n" png="/teach/systems/one-to-one-chat-board.png" title="One-to-one chat" src="/teach/systems/one-to-one-chat-board.excalidraw" >}}

[Download the one-page cheat sheet](/teach/systems/messaging-cheat-sheet.pdf) (A4, two sides: front is the five-question pack, the entities, the endpoints and the ordering policy; back is the full WhatsApp-shape board below).

### The same design with groups and several devices

The follow-ups the card leads to: group conversations, a phone and a tablet at once, and delivery status per message. Two rules survive the growth. Write the endpoints before the boxes, because the list of endpoints is what shows the hot paths (send, read, receipt, heartbeat) and the cold paths (create, rename, add, leave), and which services each flow must touch (leaving a group must detach that member's push targets). And treat ordering as a product policy, not a guarantee: the server issues a monotonic id per conversation for storage, the client renders by the sender's timestamp and marks a late arrival, retransmits are deduplicated on the client's message id, and nobody promises a global order. Multi-device means the inbox and the receipts are keyed by device, so each device catches up since its own last id. Groups run the same path N times, and above about a hundred members a worker pool does the N off the send path.

{{< excalidraw id="qBmnNjFYeH5VaJy0kyQ5" png="/teach/systems/messaging-answer-board.png" title="Real-time messaging with groups and multi-device, the answer" src="/teach/systems/messaging-answer-board.excalidraw" >}}

### The wide form: media, a hundred-thousand-member group, read state, and a crash

The third time this question came round it arrived as a platform, not a card: 500 million daily users, fifty billion messages a day, 200 milliseconds to deliver, availability over consistency. The design is the one above with the same six boxes, and the interviewer spent the second half on four follow-ups that every wide form of this question eventually reaches.

1. **Photos and videos.** The chat path carries references, never bytes. The client asks for a presigned multipart upload, sends straight to object storage, and the message holds a media id; recipients fetch through a CDN; a transcoder behind the store makes the variants the client could not.
2. **A group of a hundred thousand.** One send must not become a hundred thousand synchronous writes on the sending server. The send lands in the log and a fan-out service partitions the member list into batches, delivers each batch to the chat server that owns those users, and staggers the batches so the spike is a slope. Cold members pull on open instead of being pushed.
3. **Who has read it.** Not a per-message, per-member matrix. Each member keeps one monotonic watermark per conversation, the highest message id they have read, and it only moves forward. "Read by" for message N is the set of members whose watermark is at or past N; in a big group that becomes a count. One row per member per conversation, not one per message.
4. **The gateway crashes right after a send.** Two cases, one rule. If the durable write and the acknowledgement already happened, nothing is lost: the inbox delivers when the recipient's server or the push service picks it up. If the crash came before the acknowledgement, the client still holds the message as pending and retries with the same client message id, and the server deduplicates. The rule is that the acknowledgement comes only after the durable write, never before.

The lesson that outlived the design was about delivery. Say the whole design in four to six sentences before any box: clients hold a WebSocket to a stateful chat server behind an L4 balancer, a registry maps each user to a server and doubles as presence, a message is written to the log and the recipient's inbox before anyone is told and then pushed, groups fan out through a batch service, media goes straight to object storage, read state is a watermark, and retries are safe because the acknowledgement follows the write. Then draw. Restate the problem as the north star before the numbers. Never ask "is this okay?"; state the assumption and check alignment. When stuck, ask for focus, not the answer.

{{< excalidraw id="OLQUjzaoNEAKE3XByOe0" png="/teach/systems/messaging-platform-answer-board.png" title="Messaging platform, the wide form with four follow-ups" src="/teach/systems/messaging-platform-answer-board.excalidraw" >}}

[Download the wide-form cheat sheet](/teach/systems/messaging-platform-cheat-sheet.pdf) (A4, two sides: front is the six-sentence opener, the numbers, the endpoints and the four follow-ups; back is the board above).

## In GPU infrastructure

The same shape runs the control plane of a GPU fleet. Agents on ten thousand hosts hold long-lived connections to a handful of gateways; a command for one host has to find the gateway that owns it (consistent hash on host id); a host that is rebooting must not lose the command (an inbox row with a TTL); and "is the host alive" is a heartbeat key that expires on its own, never a table you write on every ping. Presence for chat and liveness for a fleet are the same Redis key.

## What I am listening for

- Whether the first five minutes are questions, not boxes.
- How the sender finds the recipient's gateway.
- Where the message is safe when the recipient is offline, and therefore why the bus can be lossy.
- Whether "last seen" is written per heartbeat.
- Whether ordering is promised per conversation or, fatally, globally.

{{< remember >}}
- **Ask first.** The opener is deliberately thin.
- **Consistent hash user → gateway**, ring in etcd.
- **Write message + inbox row, then publish.** Delete on ACK.
- **Presence is a TTL key**, offline is expiry.
- **Redis Pub/Sub for fan-out**, and say why not Kafka: metadata per topic.
- **Order per conversation** with server ids.
{{< /remember >}}

## Go deeper

- Hello Interview's [WhatsApp breakdown](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp) and the [design a chat system](https://www.hellointerview.com/community/questions/messenger-chat-system/cm4szunov00303g2e2gomqo2j) question page, which lists the deep dives interviewers actually ask.
- [Kafka's design document](https://kafka.apache.org/documentation/#design), the sections on partitions, replication and consumer groups. Read once; the follow-up will find you.
- Alex Xu, *System Design Interview*, chapter 12, the chat system.
- [Consistent Hashing](/teach/systems/consistent-hashing/), [Design a Message Queue](/teach/systems/design-a-message-queue/) and [Design a Notification System](/teach/systems/design-a-notification-system/) are the lessons this one leans on.

**With AI on the table.** The assistant will produce gateways, Kafka and Cassandra in one answer. I ask it why Kafka, then ask you what a topic costs and what the inbox table changes about the answer. The tool knows the boxes. You have to know which one is doing the durability.
