---
title: "Sliding Window, Fixed Length"
date: 2017-10-03T09:00:00-07:00
difficulty: "Easy. The first pattern that turns n squared into n"
tags: ["Coding", "Arrays", "Sliding Window"]
summary: "Find the best run of exactly k items in a row. Do not re-add the window every time it moves. Add the one coming in, subtract the one going out. One pass, and the same trick works for sums, counts and letters."
draft: false
---

## The question

You are given a list of numbers and a size `k`. Find the biggest sum of any `k` numbers that sit next to each other.

## Explain it to a ten-year-old

Ten children in a row, each holding some sweets. You want the three neighbours holding the most sweets between them. The slow way: count every group of three from scratch. The fast way: count the first three once. Then step right. One child leaves the group on the left, one joins on the right. Take away what the leaver had, add what the joiner has. You never count more than two children per step.

<div class="sw" aria-label="Animation: a window of three cells slides across an array, adding the new cell and subtracting the old one">
  <div class="sw-row">
    <span>2</span><span>1</span><span>5</span><span>1</span><span>3</span><span>2</span><span>8</span><span>1</span>
    <div class="sw-win"></div>
  </div>
  <div class="sw-sums">
    <span class="sw-s0">sum 8</span><span class="sw-s1">−2 +1 → 7</span><span class="sw-s2">−1 +3 → 9</span><span class="sw-s3">−5 +2 → 6</span><span class="sw-s4">−1 +8 → 13</span><span class="sw-s5">−3 +1 → 11</span>
  </div>
  <p class="sw-cap">k = 3. Best window is 3, 2, 8 with sum 13.</p>
</div>
<style>
.sw { --cell: 3.2rem; --gap: 0.45rem; --n: 6; --t: 9s; margin: 1.25rem 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.sw-row { position: relative; display: flex; gap: var(--gap); width: max-content; }
.sw-row > span { width: var(--cell); height: var(--cell); display: grid; place-items: center; border: 1px solid #94a3b8; border-radius: 0.35rem; font-size: 1.35rem; }
.sw-win { position: absolute; top: -0.25rem; left: -0.25rem; width: calc(3 * var(--cell) + 2 * var(--gap) + 0.5rem); height: calc(var(--cell) + 0.5rem); border: 3px solid #ea580c; border-radius: 0.5rem; background: rgba(254, 215, 170, 0.35); animation: sw-slide var(--t) steps(1, end) infinite; }
.sw-sums { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; margin-top: 0.9rem; font-size: 1.05rem; }
.sw-sums > span { opacity: 0.35; animation: sw-on var(--t) steps(1, end) infinite; }
.sw-sums .sw-s0 { animation-delay: 0s; }
.sw-sums .sw-s1 { animation-delay: -7.5s; }
.sw-sums .sw-s2 { animation-delay: -6s; }
.sw-sums .sw-s3 { animation-delay: -4.5s; }
.sw-sums .sw-s4 { animation-delay: -3s; }
.sw-sums .sw-s5 { animation-delay: -1.5s; }
.sw-cap { font-size: 0.85rem; opacity: 0.7; margin: 0.5rem 0 0; }
@keyframes sw-slide {
  0%      { transform: translateX(0); }
  16.66%  { transform: translateX(calc(1 * (var(--cell) + var(--gap)))); }
  33.33%  { transform: translateX(calc(2 * (var(--cell) + var(--gap)))); }
  50%     { transform: translateX(calc(3 * (var(--cell) + var(--gap)))); }
  66.66%  { transform: translateX(calc(4 * (var(--cell) + var(--gap)))); }
  83.33%  { transform: translateX(calc(5 * (var(--cell) + var(--gap)))); }
  100%    { transform: translateX(calc(5 * (var(--cell) + var(--gap)))); }
}
@keyframes sw-on {
  0%, 16.66% { opacity: 1; font-weight: 700; color: #ea580c; }
  16.67%, 100% { opacity: 0.35; font-weight: 400; color: inherit; }
}
@media (prefers-reduced-motion: reduce) {
  .sw-win, .sw-sums > span { animation: none; }
  .sw-win { transform: translateX(calc(4 * (var(--cell) + var(--gap)))); }
  .sw-sums .sw-s4 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

The window never changes size, so the only things that change when it moves are one element in and one element out. Keep a running total. Each step: add the newcomer, subtract the leaver, compare. Whatever you are tracking, a sum, a count of vowels, a map of letter frequencies, gets the same two updates.

The brute force recounts `k` items at each of `n` positions, so `n × k`. The window touches each item twice, once in and once out, so `n`.

## The steps

1. Sum the first `k` items. That is the window and the best so far.
2. For each index `i` from `k` to the end:
   - `window += a[i]`, the one coming in.
   - `window -= a[i - k]`, the one going out.
   - `best = max(best, window)`.
3. Return `best`.

```python
def max_sum_k(a, k):
    window = sum(a[:k])
    best = window
    for i in range(k, len(a)):
        window += a[i] - a[i - k]
        best = max(best, window)
    return best
```

Time O(n). Space O(1).

The same shape with a frequency map, for "does any window of `s` contain the same letters as `p`":

```python
from collections import Counter

def has_anagram(s, p):
    k = len(p)
    need, window = Counter(p), Counter(s[:k])
    if window == need:
        return True
    for i in range(k, len(s)):
        window[s[i]] += 1
        window[s[i - k]] -= 1
        if window[s[i - k]] == 0:
            del window[s[i - k]]
        if window == need:
            return True
    return False
```

## The template

This is the reason patterns are worth learning. Someone worked out the sliding window shape once, and every fixed-window problem since is the same eight lines with three small pieces swapped. Memorise the shape. Understand why each line is there. Then a problem you have not seen is one you have.

```python
state = INIT                       # STATE: a sum, a count, a Counter, a set. Add and remove in O(1)
start = 0
best = NONE
for end in range(len(a)):
    ADD(state, a[end])             # extend: the newcomer at the right edge
    if end - start + 1 == k:       # the window is exactly k wide
        best = EVALUATE(state, best)   # look at the window once
        REMOVE(state, a[start])    # contract: the leaver at the left edge
        start += 1
```

The capitals are the parts that change. For the max sum above, state is a number, add is `+=`, remove is `-=`, evaluate is `max`. For anagrams, state is a Counter, add and remove change one count, evaluate compares two Counters. For "any repeat within k", state is a set, evaluate is "was the newcomer already in it". The shape never moves.

The snippet in the steps above is the same template with `start` folded away as `i - k`. Use whichever you can write without thinking. The reason to understand the shape rather than just memorise it is the moment the interviewer says "longest" instead of "exactly k". The loop is the same, but the `if` becomes a `while` and the left edge moves only when the window breaks a rule. If you know why the fixed version works, that change is obvious. If you memorised it, it is a new problem.

## What I am listening for

- Whether you say "n times k" for the brute force and then see that the window overlaps. The overlap is the whole insight.
- Whether the out-going index is `i - k`. Off by one here is the most common bug in the room.
- Whether the state you keep supports add and remove in constant time. A sum does. A counter does. A sorted list does not, and that is when you need the [monotonic deque](/teach/coding/sliding-window-maximum/).
- Whether you can tell me when the window is fixed and when it is not. "Exactly k" is this lesson. "Longest" or "shortest" is a different pattern with two pointers that move independently.

## Where it leads

Fixed window, same trick with a different state:

- [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/). The problem above, divided by `k`.
- [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/). A set of the last `k` items.
- [Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/). A count instead of a sum.
- [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) and [Permutation in String](https://leetcode.com/problems/permutation-in-string/). A letter counter, as in the second snippet.
- [Maximum Points You Can Obtain from Cards](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/). Take from both ends, which is a fixed window over the middle, flipped.
- [Maximum Sum of Distinct Subarrays With Length K](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/). Sum plus a counter at the same time.
- [Sliding Window Maximum](/teach/coding/sliding-window-maximum/). When the state is "the biggest item", the running total is not enough.

Variable window, the next rung:

- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) and [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/). The right edge always moves, the left edge moves only when the window breaks a rule.

{{< remember >}}
- **Fixed k means one in, one out.** Never recount the window.
- **The leaver is at `i - k`.** Say it before you type it.
- **State must add and remove in O(1).** Sum, count, or counter.
- **"Exactly k" is fixed. "Longest" is not.** Different pattern.
{{< /remember >}}

## Go deeper

- [Fixed-length sliding window](https://www.hellointerview.com/learn/code/sliding-window/fixed-length) on Hello Interview. The template above is theirs, and the page has the variable-length version next to it.
- [Sliding window problems on LeetCode](https://leetcode.com/problem-list/sliding-window/), the tag page. Do the easy ones in one sitting.
- [NeetCode's roadmap](https://neetcode.io/roadmap) has a sliding window branch with a video per problem. The [NeetCode channel](https://www.youtube.com/@NeetCode) is where the videos live.
- [Sliding window on LeetCode's explore cards](https://leetcode.com/explore/) if you prefer the guided form.

**With AI on the table.** The assistant writes the sum version perfectly. I ask it to find the window with the most distinct values instead, then I ask you why the code it produced is now slower than it should be. Usually it rebuilt a set every step. Spotting that is the job.
