---
title: "WorkSpaces Application Manager: Scaling Application Deployment"
date: 2015-04-15T09:00:00-07:00
draft: false
---

![Amazon WorkSpaces](/amazon_workspaces.jpg)

WorkSpaces Application Manager solved the problem we couldn't solve with GA: how to manage Microsoft Office updates across 1M+ workspaces without downtime.

## The Problem Every Enterprise Customer Hit

After a year of WorkSpaces deployments, customers had thousands of workspaces. Then:

**Scenario: Microsoft Office patch Tuesday**

Old way:
1. Download Office update
2. Test on isolated machine (1 day)
3. Rebuild golden image with new Office (4 hours)
4. Terminate 5,000 workspaces
5. Reprovision from new image (overnight)
6. Users lose all desktop customizations 😡

**Users lost a full day of productivity every month.**

## What WAM Did

WAM separated *base OS* from *applications.* Instead of golden images containing everything, we had:

- **Base Image**: Windows (versioned, rarely updated)
- **App Bundles**: Office, Adobe, Slack, etc. (versioned independently)
- **User Profile**: Desktop settings, installed fonts, preferences
- **Data**: User files (on EBS)

Now Office patch Tuesday:
1. Create new Office bundle version (15 minutes)
2. Test with 10 users (1 hour)
3. Deploy to all users in background (30 minutes, no downtime)
4. If broken, instant rollback

**Users: zero downtime. IT: one-hour lead time instead of 24 hours.**

## The Traction

WAM adoption was instant:
- **Deployment velocity**: 20x faster (from days to minutes)
- **Rollback safety**: Full version history; any bad patch could be reverted instantly
- **Compliance**: Every app version tracked with audit trail (critical for healthcare/finance)
- **Cost**: Reduced IT labor by 40% (less firefighting, fewer reprovisioning windows)

By end of 2015: 50K+ workspaces using WAM. Enterprises shifted from "WorkSpaces is for startup remote workers" to "WorkSpaces is our standard desktop."

## What We Learned

Three insights reshaped how I thought about infrastructure:

1. **Layering beats monoliths**: Monolithic images (OS + apps) break easily. Layered bundles iterate safely.

2. **Versioning + rollback > prevention**: You can't prevent all bugs. But you *can* rollback in seconds. This confidence makes users *want* updates.

3. **Operational simplicity wins deals**: WAM didn't have 10x the performance. It had 10x fewer update headaches. That was enough to convert skeptics.

## The Broader Pattern

WorkSpaces + WAM showed that cloud infrastructure doesn't just *replace* on-prem. It *reimagines* the operational model.

On-prem: golden images, batch updates, scheduled downtime.
Cloud: versioned bundles, instant rollback, zero-downtime deployments.

This pattern would repeat everywhere at AWS:
- **EC2**: versions and AMIs
- **Kubernetes**: versioned container images
- **Lambda**: versioned functions
- **Databases**: point-in-time recovery

The theme: *make versioning and rollback first-class concepts.* That's how cloud infrastructure scales to enterprise size without becoming operational hell.

