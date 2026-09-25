---
title: "Scale From Zero to Millions of Users"
date: 2020-09-15T09:00:00-07:00
difficulty: "The lesson before the first lesson. Every other design question is one rung of this ladder"
tags: ["Systems", "Scaling", "Caching", "Databases", "Availability"]
summary: "Start with one machine. Add users until it hurts, fix the one thing that hurts, repeat. Ten rungs from a single box to a sharded, cached, multi-region system, and the reason each rung exists. Learn the ladder once and half the design round becomes recognising which rung you are standing on."
draft: false
---

## The question

You have a web app on one machine. It works. Now it needs to serve millions of people. Walk me through how the system grows, one change at a time, and tell me at each step what broke and why the change fixes it.

This is chapter one of Alex Xu's [System Design Interview](https://bytebytego.com/courses/system-design-interview/scale-from-zero-to-millions-of-users) book, and it is the question I secretly ask inside every other question. Nobody says "scale from zero to millions" out loud any more. They say "design Instagram" and then watch whether you climb this ladder in the right order.

## Explain it to a ten-year-old

You open a lemonade stand in your front garden. One table, one jug, one notebook to write down who paid. On day one, three neighbours come and it is easy.

Then the whole street comes. The queue is long, so you ask a friend to run a second table, and your mum stands at the gate pointing people to whichever table is free. That is the load balancer. The notebook is now the slow part, because both tables keep reaching for it, so you give the notebook its own helper who does nothing but write things down. That is the database. People keep asking the same question, "how much is a cup?", so you write it on a sign so nobody has to ask. That is the cache. Kids from the next town want lemonade too, so you open a stand there with a photocopy of the price list. That is the CDN and the second data centre. And when the notebook itself gets too fat to flip through, you split it into two notebooks, A to M and N to Z. That is sharding.

Nobody plans a lemonade empire on day one. You add the next helper when the queue tells you to. Watch the ladder grow:

<div class="zm" aria-label="Animation: a system grows from one machine to a sharded, cached, multi-region design, one rung at a time">
  <div class="zm-grid">
    <div class="zm-row"><span class="zm-b zm-k0">Users</span><span class="zm-b zm-k8">geoDNS</span><span class="zm-b zm-k5">CDN<br><small>static files</small></span></div>
    <div class="zm-row"><span class="zm-b zm-k2">Load balancer</span><span class="zm-b zm-k8">Data centre 2<br><small>whole stack again</small></span></div>
    <div class="zm-row"><span class="zm-b zm-k0">Web 1</span><span class="zm-b zm-k2">Web 2</span><span class="zm-b zm-k6">Web n<br><small>autoscaled</small></span><span class="zm-b zm-k6">Session store</span></div>
    <div class="zm-row"><span class="zm-b zm-k4">Cache<br><small>Redis, LRU</small></span><span class="zm-b zm-k7">Queue</span><span class="zm-b zm-k7">Workers</span></div>
    <div class="zm-row"><span class="zm-b zm-k1">Database<br><small>primary, writes</small></span><span class="zm-b zm-k3">Replica<br><small>reads</small></span><span class="zm-b zm-k9">Shard 2</span><span class="zm-b zm-k9">Shard 3</span></div>
  </div>
  <div class="zm-steps">
    <span class="zm-s0">1 · one machine, first hundred users</span>
    <span class="zm-s1">2 · database on its own machine</span>
    <span class="zm-s2">3 · load balancer, second web server</span>
    <span class="zm-s3">4 · read replica, writes to primary only</span>
    <span class="zm-s4">5 · cache in front of the database</span>
    <span class="zm-s5">6 · CDN for images, CSS, JS</span>
    <span class="zm-s6">7 · stateless web tier, sessions in a shared store, autoscale</span>
    <span class="zm-s7">8 · queue and workers for slow jobs</span>
    <span class="zm-s8">9 · second data centre, geoDNS</span>
    <span class="zm-s9">10 · shard the database by user_id</span>
  </div>
  <p class="zm-cap">Faded boxes do not exist yet. Each rung is added because the previous system hurt somewhere, and only there.</p>
</div>
<style>
.zm { --t: 15s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.zm-grid { display: flex; flex-direction: column; gap: 0.45rem; width: max-content; max-width: 100%; }
.zm-row { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.zm-b { min-width: 6.4rem; padding: 0.45rem 0.6rem; text-align: center; border: 1px solid #94a3b8; border-radius: 0.35rem; font-size: 0.9rem; line-height: 1.2; opacity: 0.14; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.zm-b small { font-size: 0.72rem; opacity: 0.8; }
.zm-k0 { animation-name: zm-a0; } .zm-k1 { animation-name: zm-a1; } .zm-k2 { animation-name: zm-a2; } .zm-k3 { animation-name: zm-a3; } .zm-k4 { animation-name: zm-a4; }
.zm-k5 { animation-name: zm-a5; } .zm-k6 { animation-name: zm-a6; } .zm-k7 { animation-name: zm-a7; } .zm-k8 { animation-name: zm-a8; } .zm-k9 { animation-name: zm-a9; }
@keyframes zm-a0 { 0% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 9.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 10%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a1 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 9.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 10% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 19.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 20%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a2 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 19.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 20% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 29.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 30%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a3 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 29.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 30% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 39.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 40%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a4 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 39.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 40% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 49.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 50%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a5 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 49.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 50% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 59.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 60%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a6 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 59.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 60% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 69.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 70%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a7 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 69.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 70% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 79.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 80%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a8 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 79.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 80% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 89.99% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } 90%, 100% { opacity: 1; border-color: #94a3b8; background: transparent; } }
@keyframes zm-a9 { 0% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 89.99% { opacity: 0.14; border-color: #94a3b8; background: transparent; } 90%, 100% { opacity: 1; border-color: #ea580c; background: rgba(254, 215, 170, 0.35); } }
.zm-steps { display: flex; flex-direction: column; gap: 0.15rem; margin-top: 0.9rem; font-size: 0.95rem; }
.zm-steps > span { opacity: 0.35; animation: zm-on var(--t) steps(1, end) infinite; }
.zm-steps .zm-s0 { animation-delay: 0s; } .zm-steps .zm-s1 { animation-delay: -13.5s; } .zm-steps .zm-s2 { animation-delay: -12s; } .zm-steps .zm-s3 { animation-delay: -10.5s; } .zm-steps .zm-s4 { animation-delay: -9s; }
.zm-steps .zm-s5 { animation-delay: -7.5s; } .zm-steps .zm-s6 { animation-delay: -6s; } .zm-steps .zm-s7 { animation-delay: -4.5s; } .zm-steps .zm-s8 { animation-delay: -3s; } .zm-steps .zm-s9 { animation-delay: -1.5s; }
@keyframes zm-on { 0%, 9.99% { opacity: 1; font-weight: 700; color: #ea580c; } 10%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
.zm-cap { font-size: 0.85rem; opacity: 0.7; margin: 0.6rem 0 0; }
@media (prefers-reduced-motion: reduce) {
  .zm-b, .zm-steps > span { animation: none; }
  .zm-b { opacity: 1; }
  .zm-steps .zm-s9 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

Never add a box because the book has it. Add a box because you can name the thing that broke. The order is not arbitrary either. Each rung fixes the bottleneck the previous rung exposed:

- One machine breaks because web and database fight over the same CPU and disk. So split them.
- One web server breaks because it is a single point of failure and has a ceiling. So add a load balancer and a second one. That is horizontal scaling, and it beats vertical scaling because a bigger machine still dies alone and there is always a biggest machine.
- The database breaks next, on reads first, because reads outnumber writes. So add replicas, then a cache, then a CDN. Three flavours of the same idea: answer the question closer to the person asking.
- Then you cannot add web servers freely because sessions live on them. So make the web tier stateless and put sessions in a shared store.
- Slow work, image resizing, emails, clogs the request path. So put it on a queue with workers.
- One building breaks when the building breaks. So run a second data centre and route with geoDNS.
- Finally the database breaks on writes and on size, and no replica helps with that. So shard.

If you can say the "because" for each rung, you understand the ladder. If you can only recite the rungs, an interviewer will find out in one follow-up.

## The steps

Run it as the [45-minute plan](/teach/system-design-in-a-hurry/). This question is unusual because the interviewer usually wants the whole ladder, not one deep dive, so keep each rung to two or three sentences and save the depth for whichever rung they poke.

1. **Requirements.** Ask what "millions" means: total accounts or daily active users, and reads versus writes. Ten million accounts with a hundred thousand daily readers is a small system. A million people writing at once is not. Ask whether it is global. That decides whether rungs six and nine matter.
2. **One machine.** DNS gives the browser an IP, the browser asks the web server, the server reads its own database and returns HTML or JSON. Say it in one breath. It shows you know what a request is.
3. **Split the database out.** Web tier and data tier on separate machines so each scales on its own. Pick relational unless you have a reason: unstructured data, very low latency, or a data volume one relational box cannot hold. "NoSQL because it scales" is not a reason. Say which one and why.
4. **Load balancer plus more web servers.** Users hit the balancer's public IP. Web servers sit on private IPs behind it. If one dies, traffic moves. If load grows, add a server. This is the [load balancer lesson](/teach/systems/design-a-load-balancer/) in one paragraph.
5. **Replicate the database.** One primary takes writes. Replicas take reads. If a replica dies, reads go to the others. If the primary dies, a replica is promoted, and be honest that promotion is the messy bit: data still in flight on the old primary may be lost, and something has to pick the new primary.
6. **Add a cache.** Cache-aside, sometimes called read-through: check the cache, on a miss read the database and fill the cache. Use it for data read often and changed rarely. Set an expiry that is neither seconds nor days. Evict with LRU unless you can say why not. Spread cache nodes across machines so one dying does not stampede the database.
7. **Add a CDN.** Static files, images, CSS, JavaScript, served from a node near the user. The book's numbers are 30 ms from the CDN against 120 ms from the origin. You pay per byte, so set the TTL with care, version files to invalidate them, and have a fallback when the CDN is down.
8. **Make the web tier stateless.** Sessions go into a shared store, Redis or a database. Now any server can take any request, sticky sessions go away, and autoscaling is just adding a server to the pool. This is the rung candidates most often skip and the one that makes everything after it possible.
9. **Queue the slow work.** Producers put messages on a queue, workers take them off. The web server answers "got it" in milliseconds and the resize happens later. Producers and workers scale independently, and if the workers are down the queue simply gets longer.
10. **Second data centre.** geoDNS sends each user to the nearest one. If one goes dark, everyone goes to the other. The hard problems are data: replicate asynchronously between sites, decide what happens to writes made in the dead site, and deploy the same thing to both.
11. **Shard the database.** Split rows across databases by a key, `user_id % 4` in the book. Choose a key that spreads evenly and matches the queries. Then name the three problems before the interviewer does: resharding when a shard fills or gets hot, the celebrity problem when one key gets all the traffic, and joins across shards, which you solve by denormalising.
12. **Logging, metrics, automation.** Not a rung, a floor under every rung. Host metrics, aggregated metrics, business metrics. Errors in one place. Deploys by a machine, not a person.

## The template

Memorise the ladder as a picture, and memorise the one word that pushes you up each rung.

```text
  WHAT HURTS                 WHAT YOU ADD
  ─────────────────────      ─────────────────────────────────────
  CPU shared by web+db  ──►  separate DATABASE machine
  one web box           ──►  LOAD BALANCER + N web servers
  db reads              ──►  READ REPLICAS
  hot reads, still slow ──►  CACHE (cache-aside, TTL, LRU)
  static files, far away──►  CDN
  cannot add servers    ──►  STATELESS web tier, SESSION STORE
  slow work in request  ──►  QUEUE + WORKERS
  one building          ──►  SECOND DATA CENTRE + geoDNS
  db writes, db size    ──►  SHARDS by KEY
  cannot see anything   ──►  LOGS, METRICS, AUTOMATION
```

What changes from problem to problem is where the pain shows up first and how far up the ladder you need to go. Design Pastebin and you stop at the cache. Design a chat app and you climb to the second data centre on the first day, because the requirement says global. Design a payments ledger and you fight to stay off the sharding rung as long as you can, because sharded transactions are misery.

What must be understood, not memorised, is the left column. In an interview I will give you a number and ask where it hurts. The candidates who have only learned the right column reach for a box. The ones who learned the left column reach for a bottleneck, and then the box follows.

## In GPU infrastructure

An inference service climbs exactly this ladder, with a GPU box where the web server was. One node with the model on it, then a load balancer across replicas whose health check is a tiny forward pass rather than a TCP ping, then a cache that is a prefix cache of already-computed KV blocks instead of Redis rows. The CDN rung becomes a regional mirror of model weights so a new node pulls a hundred gigabytes from next door rather than across the country. The queue rung is the batch scheduler in front of the GPUs, and the second data centre is a second region with its own copy of the fleet. Sharding is the odd one out: on the web the database outgrows one machine, and in AI the model outgrows one GPU, so the shard key becomes a tensor dimension and the join problem becomes an all-reduce. The floor under all of it, logs, metrics and automation, is the health-check pipeline that tells me a rack is sick before a customer does.

## What I am listening for

- Whether you name the bottleneck before you name the box. "The database is getting hammered by reads, so replicas" beats "then we add replicas".
- Whether you ask what "millions" means before you draw anything.
- Whether you put stateless before autoscaling. If you autoscale a stateful web tier, I ask where the sessions went.
- Whether you know that replicas fix reads and sharding fixes writes, and never mix them up.
- The follow-ups, which is where the round is actually decided:
  - **Ten times more users overnight.** What breaks first? The answer depends on your design and you should know it.
  - **The primary dies.** Who promotes the replica, how long does it take, and what happened to the last second of writes?
  - **One user has fifty million followers.** The celebrity problem. Their shard and their cache key are on fire. What now?
  - **The cache cluster restarts cold.** Every request is a miss at once. Does the database survive? Say "warm it up gradually" and "request coalescing" and you are fine.
  - **A whole data centre goes dark.** Reads are easy. What about the writes made there in the last minute?
  - **Shard three is full and shard one is empty.** How do you reshard without downtime? [Consistent hashing](/teach/systems/consistent-hashing/) is the answer, and it is its own lesson.

## Where this question shows up

You will rarely be asked it by name. You will be asked one of its costumes:

- **Design Instagram, Twitter, or a news feed.** The ladder plus a fan-out decision. [Hello Interview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) and [Design Gurus](https://www.designgurus.io/blog/complete-guide-sys-design) both frame it this way.
- **Design Pastebin or a URL shortener.** The bottom half of the ladder. My [URL shortener lesson](/teach/systems/design-a-url-shortener/) stops at the cache on purpose.
- **"How would you handle a million concurrent users?"** Usually a bare version of rungs three to eight, common in screening rounds. [EZ Tech Learn's walkthrough](https://www.eztechlearn.com/2026/02/system-design-101-how-to-scale.html) is a typical example of the expected answer.
- **"Your app just went viral, what do you do this weekend?"** The same question, with the added constraint that you cannot rewrite anything. Cache, CDN and read replicas, in that order, because they need no code changes.
- **The scaling follow-up inside any other design.** "Now make it ten times bigger." [Design Gurus' piece on follow-ups](https://designgurus.substack.com/p/system-design-interview-survival-220) and a [DEV Community post on pre-empting them](https://dev.to/numb_code_07/the-follow-up-questions-that-decide-system-design-interviews-and-how-to-pre-empt-them-32n3) are both honest about this being where the grade is set.

{{< remember >}}
- **Name the bottleneck, then the box.** Every rung has a "because".
- **Stateless web tier first.** It unlocks autoscaling and failover.
- **Replicas fix reads. Sharding fixes writes and size.** Cache and CDN are reads too, closer to the user.
- **Redundancy at every tier.** Two of everything, in two buildings.
- **Sharding costs you joins, even spread, and celebrities.** Delay it as long as you can.
- **Logs, metrics, automation are the floor, not a rung.**
{{< /remember >}}

## Go deeper

- [Scale From Zero to Millions of Users](https://bytebytego.com/courses/system-design-interview/scale-from-zero-to-millions-of-users) on ByteByteGo is the chapter these notes follow. Read it once, then try to redraw the final diagram from memory.
- [Noah Tigner's chapter notes](https://noahtigner.com/articles/system-design-interview-volume-1-chapter-1/) and [CodeJeet's summary](https://codejeet.com/system-design/scale-from-zero-to-millions-of-users) are two shorter retellings if you want to compare against mine.
- [The Excited Engineer on scaling to a million users](https://theexcitedengineer.substack.com/p/scaling-to-million-users-system-design) adds the numbers at each rung.
- [Amazon Builders' Library](https://aws.amazon.com/builders-library/) for what each rung looks like when it is real and on fire, especially the pieces on caching and avoiding fallback.
- The follow-ups above each have a lesson here: [load balancer](/teach/systems/design-a-load-balancer/), [distributed cache](/teach/systems/design-a-distributed-cache/), [message queue](/teach/systems/design-a-message-queue/), [multi-region service](/teach/systems/design-a-multi-region-service/), [consistent hashing](/teach/systems/consistent-hashing/).

**With AI on the table.** An assistant draws the final diagram, all ten rungs, in a second, and it draws them for every problem whether they are needed or not. So I hand it a Pastebin clone with a thousand users and the assistant's full diagram, and ask you to delete boxes until it is the right size. Knowing what to remove is the whole skill now.
