---
title: "Container With Most Water"
date: 2016-11-08T09:00:00-08:00
difficulty: "Medium. Two Sum's pointer shape with a different reason to move"
tags: ["Coding", "Arrays", "Two Pointers", "Greedy"]
summary: "Vertical walls of different heights. Pick two that hold the most water between them. Start with a finger at each end and always move the shorter wall inward. Same shape as sorted Two Sum, and the lesson is why the move is safe."
draft: false
---

## The question

You are given a list of heights. Each is a vertical wall standing on the x-axis. Pick two walls so the water held between them is as much as possible. Water is width times the shorter wall, because it spills over the short one.

## Explain it to a ten-year-old

You have a row of fence posts of different heights and a long plank. Rest the plank across two posts and pour water in. The water only rises as high as the shorter post, then spills. Start with the plank across the two posts at the far ends, the widest it can go. Now which post do you give up? The tall one is doing nothing, the short one is what stops the water. So move the short one in and try again. Keep going until the posts meet. You never need to try the other way.

<div class="cw" aria-label="Animation: two pointers at the ends of a row of bars step inward, always moving the shorter wall, while the water area between them updates">
  <div class="cw-plot">
    <div class="cw-water"></div>
    <div class="cw-bar" style="--i:0;--h:3">3</div>
    <div class="cw-bar" style="--i:1;--h:1">1</div>
    <div class="cw-bar" style="--i:2;--h:6">6</div>
    <div class="cw-bar" style="--i:3;--h:4">4</div>
    <div class="cw-bar" style="--i:4;--h:5">5</div>
    <div class="cw-bar" style="--i:5;--h:2">2</div>
    <div class="cw-lo">lo</div><div class="cw-hi">hi</div>
  </div>
  <div class="cw-steps">
    <span class="cw-s0">walls 3 and 2 · 5 × 2 = 10 · move the shorter, hi</span><span class="cw-s1">walls 3 and 5 · 4 × 3 = 12 · best so far · move lo</span><span class="cw-s2">walls 1 and 5 · 3 × 1 = 3 · move lo</span><span class="cw-s3">walls 6 and 5 · 2 × 5 = 10 · move hi</span><span class="cw-s4">walls 6 and 4 · 1 × 4 = 4 · pointers meet · answer 12</span>
  </div>
</div>
<style>
.cw { --u: 4rem; --z: 1.4rem; --t: 7.5s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.cw-plot { position: relative; width: calc(6 * var(--u)); height: calc(6 * var(--z) + 2.2rem); border-bottom: 2px solid #64748b; }
.cw-bar { position: absolute; bottom: 0; left: calc(var(--i) * var(--u) + 0.45rem); width: calc(var(--u) - 0.9rem); height: calc(var(--h) * var(--z)); background: #cbd5e1; border: 1px solid #64748b; border-bottom: none; border-radius: 0.25rem 0.25rem 0 0; display: grid; align-items: end; justify-items: center; font-size: 1.1rem; padding-bottom: 0.15rem; z-index: 2; }
.cw-water { position: absolute; bottom: 0; background: rgba(59, 130, 246, 0.35); border-top: 2px solid #2563eb; z-index: 1; animation: cw-water var(--t) steps(1, end) infinite; left: calc(0.5 * var(--u)); width: calc(5 * var(--u)); height: calc(2 * var(--z)); }
.cw-lo, .cw-hi { position: absolute; top: 0; width: var(--u); text-align: center; font-size: 0.95rem; font-weight: 700; z-index: 3; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.cw-lo { color: #2563eb; left: 0; animation-name: cw-lo; }
.cw-hi { color: #ea580c; left: calc(5 * var(--u)); animation-name: cw-hi; }
.cw-lo::after, .cw-hi::after { content: "▼"; display: block; font-size: 0.7rem; }
.cw-steps { display: flex; flex-wrap: wrap; gap: 0.4rem 1.25rem; margin-top: 0.9rem; font-size: 1.05rem; }
.cw-steps > span { opacity: 0.35; animation: cw-on var(--t) steps(1, end) infinite; }
.cw-steps .cw-s0 { animation-delay: 0s; } .cw-steps .cw-s1 { animation-delay: -6s; } .cw-steps .cw-s2 { animation-delay: -4.5s; } .cw-steps .cw-s3 { animation-delay: -3s; } .cw-steps .cw-s4 { animation-delay: -1.5s; }
@keyframes cw-water {
  0%   { left: calc(0.5 * var(--u)); width: calc(5 * var(--u)); height: calc(2 * var(--z)); }
  20%  { left: calc(0.5 * var(--u)); width: calc(4 * var(--u)); height: calc(3 * var(--z)); }
  40%  { left: calc(1.5 * var(--u)); width: calc(3 * var(--u)); height: calc(1 * var(--z)); }
  60%  { left: calc(2.5 * var(--u)); width: calc(2 * var(--u)); height: calc(5 * var(--z)); }
  80%, 100% { left: calc(2.5 * var(--u)); width: calc(1 * var(--u)); height: calc(4 * var(--z)); }
}
@keyframes cw-lo { 0%, 39.99% { left: 0; } 40%, 59.99% { left: var(--u); } 60%, 100% { left: calc(2 * var(--u)); } }
@keyframes cw-hi { 0%, 19.99% { left: calc(5 * var(--u)); } 20%, 79.99% { left: calc(4 * var(--u)); } 80%, 100% { left: calc(3 * var(--u)); } }
@keyframes cw-on { 0%, 19.99% { opacity: 1; font-weight: 700; color: #ea580c; } 20%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
@media (prefers-reduced-motion: reduce) {
  .cw-water, .cw-lo, .cw-hi, .cw-steps > span { animation: none; }
  .cw-water { left: calc(0.5 * var(--u)); width: calc(4 * var(--u)); height: calc(3 * var(--z)); }
  .cw-lo { left: 0; } .cw-hi { left: calc(4 * var(--u)); }
  .cw-steps .cw-s1 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

This is the sorted [Two Sum](/teach/coding/two-sum/) shape. Two pointers at the ends, one step inward per turn, done when they meet. The only thing that changed is the reason to move.

In Two Sum the list was sorted, so "too small, move lo" was obviously safe. Here nothing is sorted. The rule is **move the shorter wall**, and it is safe for a reason you must be able to say: the area is width times the shorter wall. If you keep the shorter wall and move the taller one, the width shrinks and the height is still capped by the same short wall, so every container you would try is worse. Moving the short wall is the only move that could possibly find a taller one. So you never skip the answer.

## The steps

1. `lo = 0`, `hi = len(h) - 1`, `best = 0`.
2. While `lo < hi`:
   - `area = (hi - lo) * min(h[lo], h[hi])`. Keep the max.
   - If `h[lo] < h[hi]`, `lo += 1`. Otherwise `hi -= 1`.
3. Return `best`.

```python
def max_area(h):
    lo, hi = 0, len(h) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(h[lo], h[hi]))
        if h[lo] < h[hi]:
            lo += 1
        else:
            hi -= 1
    return best
```

Time O(n), each wall is given up at most once. Space O(1). The brute force tries every pair, n squared, and is what you say first.

## The template

This is the Two Sum pointer template with one line changed. Memorise the shape once and this problem costs you nothing new.

```python
lo, hi = 0, len(a) - 1
while lo < hi:
    MEASURE(a[lo], a[hi])          # Two Sum: the sum. Here: width × shorter wall
    if SHOULD_MOVE_LO:             # Two Sum: sum too small. Here: lo is the shorter wall
        lo += 1
    else:
        hi -= 1
```

What changes is written in capitals. MEASURE is what you compute at the two ends. SHOULD_MOVE_LO is the rule that decides which finger gives up. Everything else is the same code you already know.

The part to understand is what makes a move rule legal. The shape only works when the pointer you move can never have been part of a better answer with anything still inside. Sorted order gives you that in Two Sum. The "shorter wall caps the area" argument gives you it here. When a new problem hands you two pointers from the ends, your job is to find that sentence. If you cannot find it, the pattern does not apply and you should say so.

## In GPU infrastructure

The move rule is the lesson. When a measure is the minimum of two sides, only the smaller side is worth touching. A ring all-reduce runs at the speed of its slowest link, so upgrading the fast NIC changes nothing. A pair of GPUs negotiate NVLink at the lower of their two link widths. A rack's usable power is the smaller of the feed and the cooling. Every time you see min of two things, ask which side is the short wall before you spend money on the tall one.

## What I am listening for

- Whether you say n squared first and then look for a way to throw pairs away without checking them. That is the whole idea of two pointers.
- Whether you move the shorter wall, and whether you can say why in one sentence. Moving the taller wall is the classic wrong answer, and I let it run until you notice.
- Whether you handle equal heights. Either pointer is fine, but you should know that and not freeze on it.
- Whether you connect it to Two Sum without me pointing it out. The same shape, a different move rule. Seeing that is the difference between knowing patterns and knowing problems.

## Where it leads

- [Two Sum II, sorted input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/). The same shape with the sorted-order move rule. Do it before this one.
- [3Sum](https://leetcode.com/problems/3sum/). Fix one, run the pointer shape on the rest.
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/). The same walls, but now you count the water on top of every bar, not between two chosen ones. Two pointers from the ends again, tracking the tallest wall seen from each side. The hard cousin. Do it last.
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/). The pointer shape where the move rule is "both, every time".

{{< remember >}}
- **Two fingers at the ends.** Area is width times the shorter wall.
- **Move the shorter wall.** The taller one cannot help.
- **Why it is safe:** keeping the short wall and shrinking the width can only make it worse.
- **Same shape as Two Sum.** Different reason to move. Find the reason before you trust the shape.
{{< /remember >}}

## Go deeper

- The problem statement: [Container With Most Water on LeetCode](https://leetcode.com/problems/container-with-most-water/), number 11.
- [Container With Most Water](https://www.hellointerview.com/learn/code/two-pointers/container-with-most-water) on Hello Interview has the proof written out, and sits next to their [two pointers overview](https://www.hellointerview.com/learn/code/two-pointers/overview).
- [NeetCode's walk-through](https://www.youtube.com/watch?v=UuiTKBwPgAo) draws the water and shows the wrong move first, which is the best way to remember the right one.
- The pattern page this belongs to: [Two Sum](/teach/coding/two-sum/), where the two-pointer template lives.

**With AI on the table.** The assistant writes this correctly and moves the shorter wall. I ask it to explain why, then I ask you whether its explanation is a proof or a hunch. Usually it says "the shorter wall limits the area" and stops. The missing half is "so every container that keeps it is no better". I want you to notice the sentence is unfinished.
