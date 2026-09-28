---
title: "Design a Prompt Playground"
date: 2025-12-09T09:00:00-08:00
difficulty: "Medium. Tiny traffic, one big blob, and an interviewer who will not let you draw"
tags: ["Product Design", "Versioning", "Object Storage", "Sharing", "Frontend", "LLM", "Infrastructure"]
summary: "A million users, ten thousand a day, under one request a second, and prompts that can reach ten megabytes. The interviewer opens a Google Doc, sketches client, server and database, and says: no architecture diagram. The whole design is the blob path and the sharing semantics, and the whole test is whether you can keep the scope small."
mermaid: true
draft: false
---

## The question

Design a prompt playground: a browser product where a user writes a prompt to an AI, runs it, looks at the output, and tweaks the prompt until the output is what they wanted. The interviewer walks you through sections and asks one question at a time: what can the user do, what are the data models, what happens when a prompt is over 10 MB, how do you keep the server out of the upload path, how do you make the frontend fast, how do you shrink uploads, and how does sharing work.

This is a product-design question wearing an infrastructure coat. The traffic is deliberately small so that sharding talk wastes your minutes. The two things that matter are a **10 MB prompt** that must never pass through the application server, and **sharing** with scopes, revocation and a possible viral spike. Everything else is a sentence.

## Clarify first

Five minutes. Browser product or API? One user or teams? One model or many? What is a prompt: a single message, or system plus user plus few-shot examples? How big can it get? Do outputs need to be kept? Is sharing in scope, and shared with whom?

Then the six things a user can do: create a prompt, edit it, **run it and see the output**, save versions with history and diffs, rename and organise, share by link. Delete is a seventh if they ask. The one people forget is "run and see the output", and it is the point of the product.

Then defer in one sentence, out loud: model and parameter picker, variables and templates, tags, ratings, datasets and evaluations, batch runs, team roles. Naming them shows you know the space; building them costs the round.

The technical challenges, which are the sentences the interviewer writes down: traffic is tiny, a million users, ten thousand a day, under one request a second, eighty percent reads, so there is nothing to shard; prompts average a kilobyte but can reach 10 MB, which is about 2.5 million tokens and beyond any context window, so the blob path is the design; versions must be immutable so history, diffs, sharing and caching are cheap; sharing needs scopes and revocation, and a shared prompt can go viral.

## Entities, with fields

Three core records and two for sharing. Write the fields; names alone score nothing.

- **Prompt**: id, owner, name, latest version id, updated at.
- **PromptVersion**: id, prompt id, parent version id, body or a body reference, hash, size. Immutable. Inline under about 64 KB, a reference into object storage above that.
- **Output**: id, version id, model, content reference, tokens in and out, latency.
- **ShareLink**: token, prompt id, optional version id, scope (public, link-only, account), role (viewer, editor), expires at, revoked at.
- **AclEntry**: prompt id, principal, role. Only when teams are in scope.

Indexes: owner and updated-at for the list view, prompt and created-at for history, a unique index on the token. Not entities: the run (it is an Output row), the thread (a name on the prompt), the model (a field), and anything from the deferred list.

The API follows one to one. Create, rename and delete a prompt. Create a version with a parent, list versions, diff two versions. Run a version and stream the output back. Ask for an upload slot and get a presigned multipart URL. Create a share link with scope and role, revoke it, and render a shared view by token.

## The answer

1. **Small prompt, the normal day.** The editor autosaves a draft locally. Save creates an immutable version with the body inline. Run sends the version id to the prompt service, a model gateway streams tokens back over server-sent events, and the output is stored against the version. History shows versions and diffs because every version has a parent.
2. **The 10 MB prompt, hop by hop.** Walk the path and name the failure at each hop. The client times out and the editor chokes on the text. The gateway rejects the body with a 413 by default. The application server buffers the body and runs out of memory or request slots. Postgres stores it but the row and TOAST limits, bloat and replication lag make it a bad home. The model rejects it because it exceeds the context window, and it costs a fortune if it did not. Then the fixes, in the same order: cap at the edge with a clear message; a presigned multipart upload straight to object storage; a body reference and hash in the database; compression, since text shrinks three to five times; chunked, resumable transfer; range reads into a virtualised editor. Say plainly that running a 10 MB prompt is not possible as one call, and that chunk-and-summarise would be a separate feature.
3. **Keeping the server out of the upload.** The service hands the client a presigned URL. The bytes go from the browser to object storage directly. The service sees the metadata and a completion callback, verifies the hash, and creates the version. Multipart with per-part hashes makes it resumable; hashing the content deduplicates repeated uploads.
4. **Frontend.** A virtualised editor renders only the visible lines. History and outputs load lazily. A local cache holds recent versions and prefetches the likely next one. Drafts autosave. The client gates the size and shows a token count before anything is sent. Shared views come from a CDN. HTTP/2 multiplexing for the browser; gRPC belongs between services, not in the browser.
5. **Smaller uploads.** Send a diff against the parent version rather than the whole body, and write a full checkpoint every twenty versions so a read never replays a long chain. Compress, chunk, deduplicate repeated blocks.
6. **Renames and divergence.** Users rename; the system can auto-name from the first line or a short model summary and suggest names. Because a version has a parent, editing an old version creates a branch. Show a branch-or-merge choice; never overwrite silently. The latest pointer is per branch.
7. **Sharing.** Audience first: private, team through ACL rows, link-only through an unguessable token, public. Generate a random 128-bit token with a unique index and an optional expiry. Revocation is a `revoked_at` on the link checked through a short-lived permission cache, and the blob URLs are signed separately with a five to fifteen minute expiry; say the two-layer trade-off out loud. A viral share is cheap because versions are immutable: cache the rendered view and the blob on the CDN, and denormalise the public flag onto the link row so those reads skip the ACL lookup.
8. **Many tabs.** A shared in-browser cache, optimistic local writes, and a conflict on save turns into the same branch-or-merge choice.

## The board

The interviewer may not want a diagram. If they do, this is the one page: the request path across the top, the red 10 MB path down the left into object storage, and the sharing path along the bottom with the permission cache in front of the database.

{{< excalidraw id="S94xnwt9jN1ZfnxwXu4Z" png="/teach/systems/prompt-playground-answer-board.png" title="Prompt playground: versions, the 10 MB path, sharing" src="/teach/systems/prompt-playground-answer-board.excalidraw" >}}

[Download the one-page cheat sheet](/teach/systems/prompt-playground-cheat-sheet.pdf) (A4, two sides: front is what to ask and what to type in the Google-Doc order, back is this board).

## What goes wrong in the room

- **A fourteen-item feature list.** The interviewer asked what the user needs. Six things. Everything else, deferred in one sentence.
- **Entities the requirements never asked for.** Members, runs, datasets, evaluations. If you did not agree on evaluations in the requirements, there is no Eval table.
- **Names without fields.** "Prompt, version, output" is a start. The fields are the answer.
- **The upload through the server.** Object storage is half the answer; the presigned URL that keeps the server out of the byte path is the other half.
- **Ten minutes on sharding.** Under one request a second. Say it in minute one and move on to the blob path.
- **Diffs without checkpoints.** A chain of a thousand diffs is a slow read. Snapshot every so often.

{{< remember >}}
- **Six user needs, and "run and see the output" is one of them.** Defer the rest in one sentence.
- **Three entities with fields**: Prompt, PromptVersion (immutable), Output. Sharing adds ShareLink and, for teams, AclEntry.
- **Under one request a second: do not shard.** The design is the 10 MB path and the sharing semantics.
- **10 MB never touches the app server**: cap at the edge, presigned multipart upload, body reference, range reads.
- **Diffs plus checkpoints, compression, chunking, dedupe** shrink uploads.
- **Revocation through a short-TTL cache, blob URLs signed separately.** Immutable versions make the viral case a CDN problem.
{{< /remember >}}

## Go deeper

- [Design a URL Shortener](/teach/systems/design-a-url-shortener/) has the token generation and the viral-read pattern that sharing borrows.
- [Design an Object Store](/teach/systems/design-an-object-store/) for what a presigned URL and a multipart upload actually do.
- [Design a Token Usage and Limits Service](/teach/systems/design-a-token-usage-and-limits-service/) is what sits in the gateway when this product grows quotas.
- Anthropic's post on [AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) explains why the guided, no-diagram format exists.

**With AI on the table.** The assistant will produce a five-table schema and a Kubernetes diagram in thirty seconds. I ask it for the failure at each hop for a 10 MB prompt, then ask you which one you would fix first and why the presigned URL fixes two of them at once. The tool knows the components. You have to know the path.
