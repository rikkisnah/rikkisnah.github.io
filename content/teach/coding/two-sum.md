---
title: "Two Sum"
date: 2016-06-14T09:00:00-07:00
difficulty: "Easy. Problem number one on LeetCode, and the door to two pointers"
tags: ["Coding", "Arrays", "Two Pointers", "Hash Map"]
summary: "Find two numbers in a list that add up to a target. Unsorted list: remember what you have seen in a hash map. Sorted list: one finger at each end, walk them towards each other. Two tricks, one problem, and half of the array questions you will ever be asked."
draft: false
---

## The question

You are given a list of numbers and a target. Return the positions of the two numbers that add up to the target. There is exactly one answer and you cannot use the same number twice.

## Explain it to a ten-year-old

You have a pile of coins and need two that make exactly ten pence. The slow way is to pick up every coin and try it against every other coin. The clever way is to pick up one coin, say a three, and ask "have I already seen a seven?" Keep a note of every coin you put down. Each new coin, you check your note once. One pass through the pile.

If the coins are already lined up smallest to biggest, there is a second clever way. Put one finger on the smallest and one on the biggest. Add them. Too big? The big finger moves left. Too small? The small finger moves right. The fingers walk towards each other and meet in the middle.

**Unsorted, hash map.** List 3, 8, 1, 6, 5, target 7. Each step: look at one number, ask the note for its partner, then write the number down.

<div class="ts" aria-label="Animation: a cursor walks the array while a seen map fills up, until the complement is found">
  <div class="ts-row">
    <span>3</span><span>8</span><span>1</span><span>6</span><span>5</span>
    <div class="ts-cur"></div>
  </div>
  <div class="ts-seen"><em>seen:</em> <span class="ts-k0">3</span><span class="ts-k1">8</span><span class="ts-k2">1</span></div>
  <div class="ts-steps">
    <span class="ts-s0">3 · need 4 · not seen · write 3</span><span class="ts-s1">8 · need −1 · not seen · write 8</span><span class="ts-s2">1 · need 6 · not seen · write 1</span><span class="ts-s3">6 · need 1 · seen at index 2 · answer (2, 3)</span>
  </div>
</div>

**Sorted, two pointers.** List 1, 3, 4, 6, 8, target 10. Too small moves the left finger. Too big moves the right one.

<div class="tp" aria-label="Animation: two pointers at the ends of a sorted array walk towards each other until the pair sums to the target">
  <div class="tp-row">
    <span>1</span><span>3</span><span>4</span><span>6</span><span>8</span>
    <div class="tp-lo">lo</div><div class="tp-hi">hi</div>
  </div>
  <div class="ts-steps">
    <span class="ts-s0">1 + 8 = 9 · too small · lo →</span><span class="ts-s1">3 + 8 = 11 · too big · ← hi</span><span class="ts-s2">3 + 6 = 9 · too small · lo →</span><span class="ts-s3">4 + 6 = 10 · found (2, 3)</span>
  </div>
</div>
<style>
.ts, .tp { --cell: 3.2rem; --gap: 0.45rem; --step: calc(var(--cell) + var(--gap)); --t: 6s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.ts-row, .tp-row { position: relative; display: flex; gap: var(--gap); width: max-content; }
.ts-row > span, .tp-row > span { width: var(--cell); height: var(--cell); display: grid; place-items: center; border: 1px solid #94a3b8; border-radius: 0.35rem; font-size: 1.35rem; }
.ts-cur { position: absolute; top: -0.25rem; left: -0.25rem; width: calc(var(--cell) + 0.5rem); height: calc(var(--cell) + 0.5rem); border: 3px solid #ea580c; border-radius: 0.5rem; background: rgba(254, 215, 170, 0.35); animation: ts-walk var(--t) steps(1, end) infinite; }
.ts-seen { margin-top: 0.9rem; font-size: 1.05rem; display: flex; gap: 0.5rem; align-items: center; }
.ts-seen em { font-style: normal; opacity: 0.7; }
.ts-seen > span { padding: 0.1rem 0.6rem; border: 1px dashed #94a3b8; border-radius: 0.35rem; opacity: 0.15; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.ts-seen .ts-k0 { animation-name: ts-k0; } .ts-seen .ts-k1 { animation-name: ts-k1; } .ts-seen .ts-k2 { animation-name: ts-k2; }
.ts-steps { display: flex; flex-wrap: wrap; gap: 0.4rem 1.25rem; margin-top: 0.9rem; font-size: 1.05rem; }
.ts-steps > span { opacity: 0.35; animation: ts-on var(--t) steps(1, end) infinite; }
.ts-steps .ts-s0 { animation-delay: 0s; } .ts-steps .ts-s1 { animation-delay: -4.5s; } .ts-steps .ts-s2 { animation-delay: -3s; } .ts-steps .ts-s3 { animation-delay: -1.5s; }
.tp-lo, .tp-hi { position: absolute; top: -0.25rem; left: -0.25rem; width: calc(var(--cell) + 0.5rem); height: calc(var(--cell) + 0.5rem); border: 3px solid; border-radius: 0.5rem; font-size: 0.75rem; line-height: 1; padding-top: 0.15rem; text-align: center; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.tp-lo { border-color: #2563eb; color: #2563eb; animation-name: tp-lo; }
.tp-hi { border-color: #ea580c; color: #ea580c; animation-name: tp-hi; }
@keyframes ts-walk { 0% { transform: translateX(0); } 25% { transform: translateX(var(--step)); } 50% { transform: translateX(calc(2 * var(--step))); } 75%, 100% { transform: translateX(calc(3 * var(--step))); } }
@keyframes ts-k0 { 0%, 24.99% { opacity: 0.15; } 25%, 100% { opacity: 1; } }
@keyframes ts-k1 { 0%, 49.99% { opacity: 0.15; } 50%, 100% { opacity: 1; } }
@keyframes ts-k2 { 0%, 74.99% { opacity: 0.15; } 75%, 100% { opacity: 1; } }
@keyframes ts-on { 0%, 24.99% { opacity: 1; font-weight: 700; color: #ea580c; } 25%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
@keyframes tp-lo { 0% { transform: translateX(0); } 25%, 50% { transform: translateX(var(--step)); } 75%, 100% { transform: translateX(calc(2 * var(--step))); } }
@keyframes tp-hi { 0%, 25% { transform: translateX(calc(4 * var(--step))); } 50%, 100% { transform: translateX(calc(3 * var(--step))); } }
@media (prefers-reduced-motion: reduce) {
  .ts-cur, .ts-seen > span, .ts-steps > span, .tp-lo, .tp-hi { animation: none; }
  .ts-cur { transform: translateX(calc(3 * var(--step))); }
  .ts-seen > span { opacity: 1; }
  .ts-steps .ts-s3 { opacity: 1; font-weight: 700; color: #ea580c; }
  .tp-lo { transform: translateX(calc(2 * var(--step))); }
  .tp-hi { transform: translateX(calc(3 * var(--step))); }
}
</style>

## The trick

There are two tricks, and which one you use depends on one question: is the list sorted?

**Not sorted.** Trade space for time. As you walk the list, store each number and its position in a hash map. For each new number, look up `target - number`. If it is in the map, you are done. One pass, one lookup per element.

**Sorted.** Trade nothing. Two pointers, one at each end. The sum tells you which pointer to move. Because the list is sorted, moving `lo` right can only make the sum bigger and moving `hi` left can only make it smaller, so you never skip the answer.

Sorting an unsorted list first costs n log n, which is slower than the hash map. So the map is the answer to the classic question, and two pointers is the answer to its sorted cousin. Know both and say why.

## The steps

Unsorted, hash map:

1. `seen = {}`.
2. For each index `i` and value `x`:
   - `need = target - x`.
   - If `need` is in `seen`, return `(seen[need], i)`.
   - Otherwise `seen[x] = i`.

```python
def two_sum(a, target):
    seen = {}
    for i, x in enumerate(a):
        need = target - x
        if need in seen:
            return seen[need], i
        seen[x] = i
```

Time O(n). Space O(n).

Sorted, two pointers:

1. `lo = 0`, `hi = len(a) - 1`.
2. While `lo < hi`:
   - `s = a[lo] + a[hi]`.
   - If `s == target`, return `(lo, hi)`.
   - If `s < target`, `lo += 1`. Otherwise `hi -= 1`.

```python
def two_sum_sorted(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == target:
            return lo, hi
        if s < target:
            lo += 1
        else:
            hi -= 1
```

Time O(n). Space O(1).

## The template

Nobody invents this at the whiteboard. Someone worked it out years ago, and the reason it is worth memorising is that it is not a solution to one problem. It is a shape. The shape stays the same and three small pieces change. Learn the shape, understand why each line is there, and a problem you have never seen becomes a problem you have.

The lookup shape, for anything unsorted:

```python
seen = {}                          # STATE: what you remember. Map, or a set if you only need yes/no
for i, x in enumerate(a):
    need = TARGET - x              # KEY: what would complete this element
    if need in seen:
        return seen[need], i       # ON HIT: return, count, or collect and keep going
    seen[x] = i                    # remember this one, after the check, never before
```

The two-pointer shape, for anything sorted:

```python
lo, hi = 0, len(a) - 1
while lo < hi:
    s = a[lo] + a[hi]              # COMPARE: the thing you measure at the two ends
    if s == TARGET:
        return lo, hi              # ON HIT: return, count, or collect and move both
    if s < TARGET:
        lo += 1                    # too small: the only way up is the left finger
    else:
        hi -= 1                    # too big: the only way down is the right finger
```

What changes from problem to problem is written in capitals: the state you keep, the key you look up or the thing you compare, and what you do on a hit. Everything else is the same code. Two Sum returns on the first hit. 3Sum fixes one element and runs the sorted shape on the rest, collecting hits. Container With Most Water compares areas instead of sums and moves the shorter wall. The shape did not change.

The part you must understand, not memorise, is why the pointer shape is safe. It works only because the list is sorted, so moving `lo` cannot make the sum smaller and moving `hi` cannot make it bigger. If an interviewer changes the problem so that promise is gone, the template is gone with it, and you need to notice.

## In GPU infrastructure

Placing a job that needs exactly sixteen GPUs across two partly used hosts is Two Sum over free-GPU counts. Walk the hosts once with a map from free count to hostname and you find the pair in one pass. Sort the hosts by free GPUs and walk from both ends and you have the pointer version, which is how a simple bin packer pairs a big fragment with a small one so the rack does not end up with unusable slivers.

## What I am listening for

- Whether you say the brute force first, two loops and n squared, and then improve it. Skipping straight to the map is fine. Not being able to explain what it beats is not.
- Whether you check the map before you insert. Insert first and `[3, 3]` with target 6 finds itself.
- Whether you ask if the list is sorted. That one question tells me you know there are two tools, not one.
- Whether you can explain why the two-pointer walk never misses the answer. It is the sorted order. If you cannot say that, you have memorised the code.

## Where it leads

Two Sum is the first rung on a ladder. Once the two ideas are in your head, these are the same problem in a different costume.

- [Two Sum II, sorted input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/). The two-pointer version, on its own.
- [3Sum](https://leetcode.com/problems/3sum/). Sort, fix one number, run Two Sum II on the rest. The hard part is skipping duplicates.
- [Container With Most Water](/teach/coding/container-with-most-water/). Two pointers from the ends, always move the shorter wall. Its own lesson, because the reason to move is the whole point.
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/). Two pointers from the ends, compare and walk in.
- [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) and [Move Zeroes](/teach/coding/move-zeroes/). Two pointers moving the same direction at different speeds.
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/). Two pointers from the ends, hard. Do it last.
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/). The hash map idea again, with running sums instead of single numbers.

{{< remember >}}
- **Unsorted: hash map.** Look up `target - x` before you insert `x`.
- **Sorted: two pointers.** Too small, move `lo`. Too big, move `hi`.
- **Ask if it is sorted.** That decides the tool.
- **Say the brute force first.** Then say what you are beating.
{{< /remember >}}

## Go deeper

- The problem statement: [Two Sum on LeetCode](https://leetcode.com/problems/two-sum/). Then [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) for the sorted version.
- [Two Pointers overview](https://www.hellointerview.com/learn/code/two-pointers/overview) on Hello Interview covers the pattern, both directions, and the problems that use it.
- [Two Sum walked through by NeetCode](https://www.youtube.com/watch?v=KLlXCFG5TnA) is eight minutes and the drawing is exactly the one above. The rest of the [NeetCode channel](https://www.youtube.com/@NeetCode) has every problem in the list.

**With AI on the table.** The assistant will hand you the hash map version instantly. I ask it to handle a list with a million numbers where memory is tight and the list is already sorted, and I watch whether you notice the tool should switch tricks. Then I ask what breaks if the same number appears twice.
