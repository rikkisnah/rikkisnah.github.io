---
title: "Stacks"
date: 2017-02-21T09:00:00-08:00
difficulty: "Easy to start. One data structure, three shapes, and a lot of medium problems fall over"
tags: ["Coding", "Stack", "Monotonic", "Parsing"]
summary: "A pile of plates. You only ever touch the top one. That is enough to match brackets, undo edits, unwind nested things, and find the next bigger number for every item in one pass. Learn the three shapes and you have the whole family."
draft: false
---

## The question

Is this string of brackets valid? `([]{})` is. `([)]` is not. Every opener must be closed by the matching closer, in the right order. That is the warm-up. The same tool then answers "for each day, how long until a warmer one", and "what does `3[a2[c]]` expand to".

## Explain it to a ten-year-old

A pile of plates. You can put a plate on top or take the top one off. You cannot pull one out of the middle. Now read the brackets left to right. Every time you see an opener, put a plate on the pile with that shape drawn on it. Every time you see a closer, look at the top plate. If it is the matching opener, take it off. If it is the wrong shape, or there is no plate, the string is broken. When you reach the end, the pile must be empty.

<div class="st" aria-label="Animation: a cursor walks a bracket string; openers are pushed onto a stack, closers pop the matching opener, and the stack ends empty">
  <div class="st-wrap">
    <div class="st-in">
      <div class="st-row">
        <span>(</span><span>[</span><span>]</span><span>{</span><span>}</span><span>)</span>
        <div class="st-cur"></div>
      </div>
    </div>
    <div class="st-stack">
      <div class="st-slot"><span class="st-p1a">[</span><span class="st-p1b">{</span></div>
      <div class="st-slot"><span class="st-p0">(</span></div>
      <div class="st-base">stack</div>
    </div>
  </div>
  <div class="st-steps">
    <span class="st-s0">( · opener · push</span><span class="st-s1">[ · opener · push</span><span class="st-s2">] · top is [ · match · pop</span><span class="st-s3">{ · opener · push</span><span class="st-s4">} · top is { · match · pop</span><span class="st-s5">) · top is ( · match · pop · empty · valid</span>
  </div>
</div>
<style>
.st { --cell: 3.2rem; --gap: 0.45rem; --step: calc(var(--cell) + var(--gap)); --t: 9s; margin: 1.25rem 0 1.75rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.st-wrap { display: flex; gap: 2.5rem; align-items: flex-end; flex-wrap: wrap; }
.st-row { position: relative; display: flex; gap: var(--gap); width: max-content; }
.st-row > span { width: var(--cell); height: var(--cell); display: grid; place-items: center; border: 1px solid #94a3b8; border-radius: 0.35rem; font-size: 1.5rem; }
.st-cur { position: absolute; top: -0.25rem; left: -0.25rem; width: calc(var(--cell) + 0.5rem); height: calc(var(--cell) + 0.5rem); border: 3px solid #ea580c; border-radius: 0.5rem; background: rgba(254, 215, 170, 0.35); animation: st-walk var(--t) steps(1, end) infinite; }
.st-stack { display: flex; flex-direction: column; gap: 0.25rem; }
.st-slot { position: relative; width: var(--cell); height: var(--cell); }
.st-slot > span { position: absolute; inset: 0; display: grid; place-items: center; border: 2px solid #ea580c; background: #fed7aa; border-radius: 0.35rem; font-size: 1.5rem; opacity: 0; animation-duration: var(--t); animation-timing-function: steps(1, end); animation-iteration-count: infinite; }
.st-p0 { animation-name: st-p0; } .st-p1a { animation-name: st-p1a; } .st-p1b { animation-name: st-p1b; }
.st-base { width: var(--cell); border-top: 3px solid #64748b; font-size: 0.8rem; text-align: center; opacity: 0.7; padding-top: 0.15rem; }
.st-steps { display: flex; flex-wrap: wrap; gap: 0.4rem 1.25rem; margin-top: 0.9rem; font-size: 1.05rem; }
.st-steps > span { opacity: 0.35; animation: st-on var(--t) steps(1, end) infinite; }
.st-steps .st-s0 { animation-delay: 0s; } .st-steps .st-s1 { animation-delay: -7.5s; } .st-steps .st-s2 { animation-delay: -6s; } .st-steps .st-s3 { animation-delay: -4.5s; } .st-steps .st-s4 { animation-delay: -3s; } .st-steps .st-s5 { animation-delay: -1.5s; }
@keyframes st-walk { 0% { transform: translateX(0); } 16.66% { transform: translateX(var(--step)); } 33.33% { transform: translateX(calc(2 * var(--step))); } 50% { transform: translateX(calc(3 * var(--step))); } 66.66% { transform: translateX(calc(4 * var(--step))); } 83.33%, 100% { transform: translateX(calc(5 * var(--step))); } }
@keyframes st-p0  { 0%, 83.32% { opacity: 1; } 83.33%, 100% { opacity: 0; } }
@keyframes st-p1a { 0%, 16.65% { opacity: 0; } 16.66%, 33.32% { opacity: 1; } 33.33%, 100% { opacity: 0; } }
@keyframes st-p1b { 0%, 49.99% { opacity: 0; } 50%, 66.65% { opacity: 1; } 66.66%, 100% { opacity: 0; } }
@keyframes st-on { 0%, 16.65% { opacity: 1; font-weight: 700; color: #ea580c; } 16.66%, 100% { opacity: 0.35; font-weight: 400; color: inherit; } }
@media (prefers-reduced-motion: reduce) {
  .st-cur, .st-slot > span, .st-steps > span { animation: none; }
  .st-cur { transform: translateX(var(--step)); }
  .st-p0, .st-p1a { opacity: 1; }
  .st-steps .st-s1 { opacity: 1; font-weight: 700; color: #ea580c; }
}
</style>

## The trick

A stack is the answer whenever **the thing you need next is the most recent thing you have not dealt with yet**. Brackets: the closer must match the most recent unclosed opener. Undo: the most recent edit. Nested strings: the most recent unfinished group. "Next warmer day": the most recent day still waiting for an answer.

Three shapes cover nearly every stack problem:

1. **Match.** Push openers. On a closer, pop and compare. Empty at the end means valid.
2. **Unwind.** Push partial work as you go into nesting. On the way out, pop and combine. Decode String, expression evaluation, folder paths.
3. **Monotonic.** Keep the stack sorted, say decreasing. When a newcomer is bigger than the top, pop, and the newcomer is the answer for everything you popped. Next greater element, daily temperatures, largest rectangle.

## The steps

Valid Parentheses:

1. `pairs = {")": "(", "]": "[", "}": "{"}`, `stack = []`.
2. For each character: if it is an opener, push it. If it is a closer, the stack must be non-empty and its top must be `pairs[c]`. Otherwise return false. Pop.
3. Return `not stack`.

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack
```

Time O(n). Space O(n) in the worst case, a string of all openers.

Daily Temperatures, the monotonic shape:

```python
def daily_temperatures(t):
    ans = [0] * len(t)
    stack = []                        # indices, temperatures decreasing from bottom to top
    for i, x in enumerate(t):
        while stack and t[stack[-1]] < x:
            j = stack.pop()
            ans[j] = i - j            # x is the first warmer day after j
        stack.append(i)
    return ans
```

Each index is pushed once and popped at most once, so O(n) even with the inner `while`.

## The template

Someone worked out the three shapes years ago. Memorise them as one loop with the capitals filled in differently, and understand what the stack is holding in each. That last part is what lets you use it on a problem you have not seen.

```python
stack = []
for x in INPUT:
    while stack and SHOULD_POP(stack[-1], x):   # match: closer meets its opener. monotonic: x beats the top
        top = stack.pop()
        RESOLVE(top, x)                         # match: nothing. monotonic: x is top's answer. unwind: combine
    if SHOULD_PUSH(x):                          # match: openers only. monotonic: always. unwind: on the way in
        stack.append(x)
FINISH(stack)                                   # match: must be empty. monotonic: leftovers have no answer
```

The question to ask before writing any of it is **what does each item on the stack mean**. In matching, an opener waiting for its closer. In unwinding, work paused while you go one level deeper. In a monotonic stack, an item still waiting for its answer, and the stack stays sorted because anything that would have broken the order has already been answered and removed. If you can say what a stack item means, the pops write themselves. If you cannot, you are guessing.

## What I am listening for

- Whether you check the stack is non-empty before you look at the top. Every stack bug I have ever seen in an interview is this one.
- Whether you match the type, not just the count. `([)]` has balanced counts and is wrong.
- For the monotonic shape, whether you can say why the inner `while` does not make it n squared. Each item is popped once. If you cannot say that, you cannot defend the complexity.
- Whether you know what is on the stack. I ask "what does the top of your stack mean right now" halfway through. The good candidates answer in one sentence.

## Where it leads

Match:

- [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/). The one above.
- [Min Stack](/teach/coding/min-stack/). A stack that also answers "smallest right now". A second stack does it.

Unwind:

- [Decode String](https://leetcode.com/problems/decode-string/). Push the count and the string so far on `[`, pop and repeat on `]`.
- [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/). Push numbers, an operator pops two.
- [Simplify Path](https://leetcode.com/problems/simplify-path/). `..` pops a folder.

Monotonic:

- [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/). The snippet above.
- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/). The same, with a map at the end.
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/). Increasing stack of bar indices. Popping a bar tells you how far its height extends. The hard one.
- [Sliding Window Maximum](/teach/coding/sliding-window-maximum/). The monotonic idea in a deque, because items also leave from the front.

{{< remember >}}
- **A stack is for "the most recent unfinished thing".**
- **Three shapes: match, unwind, monotonic.** One loop, different pops.
- **Check non-empty before you peek.** Every time.
- **Say what a stack item means.** Then the code writes itself.
- **Monotonic is O(n).** Each item pushed once, popped once.
{{< /remember >}}

## Go deeper

- [Stack overview](https://www.hellointerview.com/learn/code/stack/overview) on Hello Interview, and their [monotonic stack](https://www.hellointerview.com/learn/code/stack/monotonic-stack) page for the third shape.
- [Valid Parentheses](https://www.youtube.com/watch?v=WTzjTskDFMg) and [Daily Temperatures](https://www.youtube.com/watch?v=cTBiBSnjO3c) walked through by NeetCode. The second one is where the monotonic idea clicks for most people.
- [Stack problems on LeetCode](https://leetcode.com/problem-list/stack/) and the [monotonic stack list](https://leetcode.com/problem-list/monotonic-stack/). Do Valid Parentheses, Daily Temperatures and Decode String in one sitting and you have seen all three shapes.
- [Stack on Wikipedia](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) for the two minutes of history, including why it is called push and pop.

**With AI on the table.** The assistant writes Valid Parentheses in one go. I hand it `Daily Temperatures` and ask it for the complexity. It says O(n). I ask you whether that is right, and why, with a `while` loop inside a `for`. The answer is "each index is popped once". If you cannot say it, the tool's answer is a rumour.
