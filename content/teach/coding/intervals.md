---
title: "Intervals"
date: 2018-03-27T09:00:00-07:00
difficulty: "Medium. One sort and one question, and half of all scheduling problems fall over"
tags: ["Coding", "Intervals", "Sorting", "Greedy"]
summary: "Start and end pairs: meetings, bookings, ranges. Sort them and the mess becomes a line you walk once. Sort by start to merge. Sort by end to pick the most that fit. The only question at each step is whether the next one starts before the current one ends."
draft: false
---

## The question

You are given a list of pairs, each a start and an end. Merge the ones that overlap. Or: pick the most that do not overlap. Or: slot a new one in. Or: how many are running at once. Different words, one pattern.

## Explain it to a ten-year-old

Your friends each tell you when they are at the park, like "two till six" and "one till three". Written down in the order they told you, it is a mess. Line them up by when each one arrives and it becomes easy. Walk along the day. If the next friend arrives before the current group has left, they join the group and the group stays until the last of them leaves. If the next friend arrives after everyone has gone, that is a new group. At the end you know exactly when the park had someone in it.

<div class="iv" aria-label="Animation: four intervals sorted by start are walked once; overlapping ones stretch the current merged interval, a gap starts a new one">
  <div class="iv-axis"><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>10</span><span>11</span><span>12</span></div>
  <div class="iv-lane"><div class="iv-bar iv-in iv-i0" style="--s:1;--e:3">1–3</div></div>
  <div class="iv-lane"><div class="iv-bar iv-in iv-i1" style="--s:2;--e:6">2–6</div></div>
  <div class="iv-lane"><div class="iv-bar iv-in iv-i2" style="--s:8;--e:10">8–10</div></div>
  <div class="iv-lane"><div class="iv-bar iv-in iv-i3" style="--s:9;--e:12">9–12</div></div>
  <p class="iv-label">merged, so far</p>
  <div class="iv-lane iv-out"><div class="iv-bar iv-m0"></div><div class="iv-bar iv-m1"></div></div>
  <div class="iv-steps">
    <span class="iv-s0">1–3 · first one · start a group</span><span class="iv-s1">2–6 · 2 &lt; 3 · overlaps · stretch to 1–6</span><span class="iv-s2">8–10 · 8 ≥ 6 · gap · new group</span><span class="iv-s3">9–12 · 9 &lt; 10 · overlaps · stretch to 8–12</span>
  </div>
</div>
<style>
.iv { --u: 2.7rem; --t: 6s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; width: max-content; max-width: 100%; }
.iv-axis { display: flex; margin-left: 0; }
.iv-axis > span { width: var(--u); font-size: 0.75rem; opacity: 0.6; text-align: left; border-left: 1px solid #cbd5e1; padding-left: 0.15rem; }
.iv-lane { position: relative; height: 1.9rem; margin-top: 0.3rem; width: calc(12 * var(--u)); }
.iv-label { margin: 0.6rem 0 0; font-size: 0.8rem; opacity: 0.7; }
.iv-bar { position: absolute; top: 0.15rem; height: 1.6rem; left: calc((var(--s) - 1) * var(--u)); width: calc((var(--e) - var(--s)) * var(--u)); border-radius: 0.35rem; display: grid; place-items: center; font-size: 0.95rem; }
.iv-in { background: #e2e8f0; border: 1px solid #94a3b8; opacity: 0.45; animation: iv-on var(--t) steps(1, end) infinite; }
.iv-i0 { animation-delay: 0s; } .iv-i1 { animation-delay: -4.5s; } .iv-i2 { animation-delay: -3s; } .iv-i3 { animation-delay: -1.5s; }
.iv-out { border-top: 1px dashed #cbd5e1; padding-top: 0.2rem; height: 2.2rem; margin-top: 0.15rem; }
.iv-m0, .iv-m1 { top: 0.35rem; background: rgba(254, 215, 170, 0.6); border: 2px solid #ea580c; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.iv-m0 { --s: 1; --e: 3; animation-name: iv-m0; }
.iv-m1 { --s: 8; --e: 10; opacity: 0; animation-name: iv-m1; }
.iv-steps { display: flex; flex-wrap: wrap; gap: 0.4rem 1.25rem; margin-top: 0.9rem; font-size: 1.05rem; }
.iv-steps > span { opacity: 0.35; animation: iv-step var(--t) steps(1, end) infinite; }
.iv-steps .iv-s0 { animation-delay: 0s; } .iv-steps .iv-s1 { animation-delay: -4.5s; } .iv-steps .iv-s2 { animation-delay: -3s; } .iv-steps .iv-s3 { animation-delay: -1.5s; }
@keyframes iv-on { 0%, 24.99% { opacity: 1; background: #fed7aa; border-color: #ea580c; } 25%, 100% { opacity: 0.45; background: #e2e8f0; border-color: #94a3b8; } }
@keyframes iv-step { 0%, 24.99% { opacity: 1; font-weight: 700; color: #ea580c; } 25%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
@keyframes iv-m0 { 0%, 24.99% { width: calc(2 * var(--u)); } 25%, 100% { width: calc(5 * var(--u)); } }
@keyframes iv-m1 { 0%, 49.99% { opacity: 0; width: calc(2 * var(--u)); } 50%, 74.99% { opacity: 1; width: calc(2 * var(--u)); } 75%, 100% { opacity: 1; width: calc(4 * var(--u)); } }
@media (prefers-reduced-motion: reduce) {
  .iv-in, .iv-m0, .iv-m1, .iv-steps > span { animation: none; }
  .iv-in { opacity: 1; }
  .iv-m0 { width: calc(5 * var(--u)); } .iv-m1 { opacity: 1; width: calc(4 * var(--u)); }
  .iv-steps .iv-s3 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

Sort. Unsorted intervals can overlap anything, so every check is against everything, n squared. Sorted by start, an interval can only overlap the one you are currently holding, so one pass does it. The check is one comparison: does the next one start before the current one ends?

The second trick is knowing which end to sort by. **Sort by start when you are merging or inserting**, because you build the answer left to right. **Sort by end when you are choosing the most that fit**, because taking the one that finishes earliest leaves the most room for the rest. Getting the sort wrong is the most common mistake in the whole family.

## The steps

Merge, sorted by start:

1. Sort by start.
2. `out = [first]`.
3. For each interval after that: if its start is less than the end of `out[-1]`, stretch `out[-1].end` to the max of the two ends. Otherwise append it.

```python
def merge(intervals):
    intervals.sort()
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s < out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

Pick the most that do not overlap, sorted by end:

1. Sort by end.
2. `last_end = -infinity`, `kept = 0`.
3. For each interval: if its start is at or after `last_end`, keep it and set `last_end` to its end. Otherwise skip it.

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])
    last_end, kept = float("-inf"), 0
    for s, e in intervals:
        if s >= last_end:
            kept += 1
            last_end = e
    return kept          # removals needed = len(intervals) - kept
```

Both are O(n log n) for the sort and O(n) for the walk. Touching ends: decide whether `[1, 3]` and `[3, 5]` overlap before you write the comparison. The problem statement tells you. Most say they do not, so the check is a strict less-than.

## The template

Somebody worked this out long ago, and the reason to memorise it is that every interval problem is the same eight lines with two decisions swapped. Learn the shape and the decisions, and Insert Interval, Non-overlapping Intervals and Burst Balloons stop being new problems.

```python
intervals.sort(key=SORT_KEY)           # DECISION 1: by start to build, by end to choose
current = None
for s, e in intervals:
    if current is not None and s < current[1]:   # DECISION 2: overlap test, < or <=
        MERGE_OR_SKIP(current, s, e)   # build: stretch current.end = max(...). choose: skip
    else:
        EMIT(current); current = [s, e]  # a gap: close the old one, open a new one
EMIT(current)
```

The two decisions:

- **Sort key.** Start when the answer is a set of ranges you build left to right: merge, insert, free time. End when the answer is a count of ranges you choose: most meetings you can attend, fewest to remove, fewest arrows.
- **On overlap.** Build problems stretch the current interval. Choose problems throw the newcomer away, because the one you already hold ends sooner.

When the question is "how many at once", the shape changes: split every interval into a start event and an end event, sort the events, and count up and down as you walk. That is the [meeting rooms](/teach/coding/meeting-rooms/) lesson, and the heap there is doing the same walk.

The part to understand rather than memorise is why sorting by end is safe for choosing. Among all the intervals that could be first, the one that ends earliest can never block more of the rest than any other choice would. Say that sentence to yourself until it is obvious. Then you can defend the greedy answer instead of just producing it.

## What I am listening for

- Whether you sort before you do anything else. If you start comparing every pair, I wait a minute and then ask what sorting would buy you.
- Which key you sort by, and whether you can say why. "By start" without a reason is a memorised answer. "By end because it frees up the most room" is understanding.
- The overlap test on touching ends. I ask whether `[1, 3]` and `[3, 5]` merge. I want you to ask me back.
- Whether you notice that `out[-1]` changes as you go. The stretch must use the max of both ends, not just the newcomer's end. `[1, 10]` then `[2, 3]` is the trap.

## Where it leads

All of these are the template with the two decisions made:

- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/). Sort by start, return false on the first overlap. The warm-up.
- [Merge Intervals](/teach/coding/merge-intervals/). The build shape, exactly as above. [On LeetCode](https://leetcode.com/problems/merge-intervals/).
- [Insert Interval](https://leetcode.com/problems/insert-interval/). Already sorted. Copy the ones that end before it, merge the ones that overlap it, copy the rest.
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/). The choose shape, sorted by end. Answer is total minus kept.
- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/). The choose shape again, wearing a costume.
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/). Two sorted lists, two pointers, the overlap of each pair is max of starts to min of ends.
- [Meeting Rooms II](/teach/coding/meeting-rooms/). How many at once. The event walk or the heap. [On LeetCode](https://leetcode.com/problems/meeting-rooms-ii/).
- [Employee Free Time](https://leetcode.com/problems/employee-free-time/). Merge everyone's busy time, then the gaps between merged intervals are the answer.

{{< remember >}}
- **Sort first.** Then one pass.
- **Overlap: next start before current end.** Decide about touching ends before you type it.
- **Build by start, choose by end.** The sort key is the whole problem.
- **Stretch with max of both ends.** `[1, 10]` then `[2, 3]` catches people.
- **"How many at once" is events**, not merging.
{{< /remember >}}

## Go deeper

- [Intervals overview](https://www.hellointerview.com/learn/code/intervals/overview) on Hello Interview is the source for the two-sort idea and the problem list.
- [Merge Intervals walked through by NeetCode](https://www.youtube.com/watch?v=44H3cEC2fFM), and the interval branch of the [NeetCode roadmap](https://neetcode.io/roadmap) for the rest.
- [Interval problems on LeetCode](https://leetcode.com/problem-list/intervals/), the tag page. Do Merge, Insert and Non-overlapping in one sitting and you will see the template.
- [Interval scheduling on Wikipedia](https://en.wikipedia.org/wiki/Interval_scheduling) has the proof that earliest-end-first is optimal, for the day an interviewer asks you to justify it.

**With AI on the table.** The assistant merges perfectly. I change the problem to "fewest to remove" and watch whether you notice the sort key must change. Then I hand it `[1, 10], [2, 3], [4, 5]` and ask what its merge returns. If it wrote `out[-1][1] = e` instead of the max, the answer is wrong, and the job is to see that in the code it gave you, not to run it.
