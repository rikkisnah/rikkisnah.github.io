---
title: "Design a URL Shortener"
date: 2016-05-17T09:00:00-07:00
difficulty: "Easy to start, and the first design question I give. Bitly, TinyURL, same thing"
tags: ["Systems", "Hashing", "Storage", "Caching"]
summary: "Turn a long web address into a short one and back again. One table, one counter, one cache, one redirect. The whole design is deciding how to make the short code so two people never get the same one, then making the read path fast because reads outnumber writes a thousand to one."
draft: false
---

## The question

Design Bitly. Give it a long URL, get a short one back. Anyone who visits the short one is sent to the long one. A billion links, a hundred million people a day. Under 100 ms per redirect. Never hand out the same code twice.

## Explain it to a ten-year-old

A library has thousands of books with long titles. Instead of writing the whole title on your reading list, the librarian gives each book a small sticker with a code, like B7K2. You write down B7K2. When you come back and say "B7K2", the librarian looks it up in the big register and hands you the right book. The register is the database. The sticker is the short code. The librarian's memory of the popular books is the cache. The only hard part is making sure no two books ever get the same sticker, and the librarian does that by numbering stickers in order from a roll.

The hot path, a visitor clicking a short link:

<div class="us" aria-label="Animation: a redirect request moves from the browser through the API, misses the cache, reads the database, fills the cache, and returns a 302">
  <div class="us-row">
    <span>Browser</span><span>API</span><span>Cache</span><span>Database</span><span>Long URL</span>
    <div class="us-cur"></div>
  </div>
  <div class="us-steps">
    <span class="us-s0">GET /abc123</span><span class="us-s1">look up abc123</span><span class="us-s2">cache miss</span><span class="us-s3">read row, check expiry, fill cache</span><span class="us-s4">302 → https://example.com/very/long/…</span>
  </div>
  <p class="us-cap">Next visitor: browser → API → cache hit → 302. The database never hears about it.</p>
</div>
<style>
.us { --cell: 5.6rem; --gap: 0.45rem; --step: calc(var(--cell) + var(--gap)); --t: 7.5s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.us-row { position: relative; display: flex; gap: var(--gap); width: max-content; }
.us-row > span { width: var(--cell); height: 3rem; display: grid; place-items: center; border: 1px solid #94a3b8; border-radius: 0.35rem; font-size: 0.95rem; }
.us-cur { position: absolute; top: -0.25rem; left: -0.25rem; width: calc(var(--cell) + 0.5rem); height: 3.5rem; border: 3px solid #ea580c; border-radius: 0.5rem; background: rgba(254, 215, 170, 0.35); animation: us-walk var(--t) steps(1, end) infinite; }
.us-steps { display: flex; flex-wrap: wrap; gap: 0.4rem 1.25rem; margin-top: 0.9rem; font-size: 1.05rem; }
.us-steps > span { opacity: 0.35; animation: us-on var(--t) steps(1, end) infinite; }
.us-steps .us-s0 { animation-delay: 0s; } .us-steps .us-s1 { animation-delay: -6s; } .us-steps .us-s2 { animation-delay: -4.5s; } .us-steps .us-s3 { animation-delay: -3s; } .us-steps .us-s4 { animation-delay: -1.5s; }
.us-cap { font-size: 0.85rem; opacity: 0.7; margin: 0.6rem 0 0; }
@keyframes us-walk { 0% { transform: translateX(0); } 20% { transform: translateX(var(--step)); } 40% { transform: translateX(calc(2 * var(--step))); } 60% { transform: translateX(calc(3 * var(--step))); } 80%, 100% { transform: translateX(calc(4 * var(--step))); } }
@keyframes us-on { 0%, 19.99% { opacity: 1; font-weight: 700; color: #ea580c; } 20%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
@media (prefers-reduced-motion: reduce) {
  .us-cur, .us-steps > span { animation: none; }
  .us-cur { transform: translateX(calc(4 * var(--step))); }
  .us-steps .us-s4 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

Do not hash the URL and hope. Take a number from a counter and write it in base 62, the ten digits plus upper and lower case letters. Six characters gives you 62 to the power 6, about 56 billion codes. Seven gives 3.5 trillion. A counter never collides. The only thing left to worry about is handing out counter ranges to many servers so they do not fight over one number, and that is a batch of a thousand from Redis, not one call per link.

Then notice the shape of the load. A thousand clicks for every link created. Design the read path first and the write path barely at all.

## The steps

Follow the [45-minute plan](/teach/system-design-in-a-hurry/). This problem is the best place to practise it, because every step is short.

1. **Requirements, five minutes.** A user can shorten a URL, optionally with a custom alias and an expiry. A visitor is redirected. Out of scope: accounts, click analytics. Qualities: codes are unique, redirect under 100 ms, available over consistent, a billion links, a hundred million daily users. Say "read heavy, about a thousand to one" out loud. That sentence drives everything after it.
2. **Entities, two minutes.** Original URL, short URL, user. That is the list.
3. **API, five minutes.** `POST /urls` with the long URL, alias and expiry, returns the short URL. `GET /{code}` returns a redirect. Two endpoints. Do not add a third.
4. **High level, ten minutes.** Create: API validates the URL, gets a code, writes one row, returns the short link. Redirect: API reads the row, checks expiry, answers 410 if expired, else redirects. One table, code as the primary key, long URL, owner, created, expires.
5. **Deep dive, the code.** Hash of the URL gives you deduplication but collisions, so you need a unique constraint and a retry loop. Counter in Redis gives you uniqueness for free, and `INCR` is atomic because Redis is single threaded. Counter codes are guessable, so if that matters, mix in a few random bits or skip in the sequence. Pure random is not enough entropy at a billion. Pick the counter and say why.
6. **Deep dive, the reads.** A hundred million users at five clicks a day is about six thousand redirects a second, tens of thousands at peak. Primary key index first. Then a cache in front of the database, memory is a thousand times faster than SSD. Then, if the interviewer pushes, run the redirect at the CDN edge so most clicks never reach your servers at all.
7. **Deep dive, the redirect code.** 301 is permanent and browsers cache it, so you never see the second click. 302 sends every visit through you, so you can count, expire and change links. Say 302 and say why.
8. **Deep dive, the writes and the counter.** Writes are about one a second. A single Postgres with a replica is plenty. Storage is 500 bytes times a billion, half a terabyte. For the counter, each write server takes a block of a thousand from Redis and burns through it locally. If Redis dies and loses a few values, nothing breaks, you only needed uniqueness, not continuity, and the unique constraint on the table is the safety net. Multi-region: give each region its own disjoint range.

## The template

This problem is the simplest example of a shape you will use for half the design round: **a read-heavy key-value service**. Memorise the shape, then understand each box well enough to remove it when the problem does not need it.

```text
WRITE PATH (rare, ~1/s)
  client ──► API ──► ID GENERATOR ──► DATABASE (one table, key = ID)

READ PATH (constant, ~1000/s)
  client ──► API ──► CACHE ──hit───► RESPONSE (here: a 302)
                       │
                      miss
                       ▼
                    DATABASE ──► fill cache ──► RESPONSE
```

The parts that change from problem to problem:

- **ID GENERATOR.** Counter plus base 62 here. A [unique ID generator](/teach/systems/design-a-unique-id-generator/) when you need time ordering. A hash when you need the same input to give the same key.
- **DATABASE.** Any store with a primary key lookup. It only becomes interesting when the data outgrows one box, and then you shard by the key with [consistent hashing](/teach/systems/consistent-hashing/).
- **CACHE.** Always the same answer: cache-aside, LRU eviction, and a plan for invalidation. Here the plan is a TTL plus explicit delete on expiry.
- **RESPONSE.** A redirect here. A JSON object for a profile service. A file for an object store.

Pastebin, a profile service, a feature-flag service and a DNS resolver are this same drawing with different words in the boxes. When you recognise the shape, you get the first fifteen minutes for free and can spend the round on the box that is actually hard.

## In GPU infrastructure

The fleet inventory service is this drawing with the words changed. Hostname to node record, read by every health check and scheduler tick, written when a node is racked or drained, a thousand reads per write. One table, a cache in front, and a unique ID for every node and job. The counter-batching trick is exactly how you hand out unique job IDs across regions without the regions talking: each takes a block, and a lost block costs nothing.

## What I am listening for

- Whether you say "read heavy" in the first five minutes without being asked. Mid-level candidates get there when I nudge. Senior candidates open with it.
- Whether you reach for a hash of the URL. I ask what you do on a collision and the counter answer usually appears within a minute. Staff candidates also mention that counters are guessable.
- Whether you say 302 and know why. It is a small thing that tells me you have shipped a web service.
- Whether you ask if links expire. It changes the cache story and the storage story.
- Whether, unprompted, you can say what happens when Redis holding the counter dies. The best answer is "we lose a few numbers and nobody notices".

{{< remember >}}
- **Counter plus base 62.** No collisions, six or seven characters, billions of codes.
- **Hand out counter blocks**, not single numbers. Losing a block is fine.
- **A thousand reads per write.** Index, then cache, then edge.
- **302, not 301.** Cached redirects cannot be counted or changed.
- **Read-heavy key-value service.** Learn the shape, reuse it everywhere.
{{< /remember >}}

## Go deeper

- [Design Bitly](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly) on Hello Interview is the walk-through the steps above follow, including what they expect at mid, senior and staff level. Read it after you have tried it yourself.
- [Design a URL Shortener](https://www.youtube.com/watch?v=JQDHz72OA3c) by ByteByteGo is the twelve-minute video version. The [ByteByteGo book](https://bytebytego.com/) has it as chapter 8.
- [interviewing.io's system design guide](https://interviewing.io/guides/system-design-interview) is honest about how the round is actually graded.
- [Encode and Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) on LeetCode is the coding-round version. Twenty lines, and you should be able to write the base 62 encoder from memory.
- [NeetCode's system design course](https://neetcode.io/courses/system-design-for-beginners/0) covers this as its first problem if you want it taught slowly.

**With AI on the table.** The assistant gets this right in one go, with the counter, the cache and the 302. So I ask what happens when the Redis that hands out counter blocks is down for an hour. Can you still create links? Should you? The template has no opinion, and you must.
