# Demo: one machine-sounding paragraph, five voices, same prompt

Date: 2026-09-19. Rewrites produced by Claude Code (Claude Fable 5.1) applying `prompts/humanize-prompt-<voice>.md` once each. No facts were added; the input has none to keep beyond its one claim, that documentation matters.

## Input (58 words, written to sound like a model)

> In today's fast-paced world, documentation is not just a nice-to-have, it's the cornerstone of engineering excellence. It is important to note that clear, concise, and comprehensive docs foster collaboration, drive innovation, and ensure long-term success. Isn't it time we asked why writing things down matters? In conclusion, great documentation is a testament to a team's commitment.

Tells in the input: "In today's fast-paced world", "not just X, it's Y", "It is important to note", two lists of exactly three, a rhetorical question, "In conclusion", "testament", "cornerstone".

## Rik Kisnah (56 words)

> Every team I have joined had the same gap: the code was there and the doc was not. Documentation is part of the engineering, and the cheap part. A clear doc lets two engineers work on one system without a meeting, and it lets the next hire start without someone standing behind them. Write it down while you still remember why.

## Barack Obama (62 words)

> Let me be clear. Documentation matters. It matters to the engineer who joins next month, and it matters to the one who leaves next year. When we write down what we know, we hand our work to the people who come after us, and that is how a team outlasts any one of us. So write it down. We owe each other that much.

## Ernest Hemingway (50 words)

> Write the docs. Write them clear and write them short and write them before you forget. The team reads them and the team works and no one asks twice. The engineer who comes after you reads them too. He does not know you. He knows the docs. That is enough.

## William Faulkner (93 words, over the 10 percent limit because the voice block asks for it)

> Because the code was there, had always been there, the way the house had been there before any of them were born and would be there after, but the reason for it was gone, gone with the man who wrote it and never wrote it down, so that the ones who came after (the new ones, the ones who had not watched it built) stood before it as before a locked door, and the doc, the plain small doc that would have been the key, had never been made, and would not be

## Dario Amodei (64 words)

> I think the case for documentation is simpler than people make it. To be clear, writing things down is not free, and I could be wrong about how much it pays back on a small team. My guess is that the return comes from a mechanism: a written doc lets a second engineer act without asking the first, which removes the bottleneck of one person's memory.

## What to notice

- The same prompt produced five different rhythms because only the voice line changed.
- Every version dropped the same tells: the opener, the "not just" flip, the note-that phrase, the question, the closing summary.
- Obama kept his groups of three and Faulkner kept his length and his mid-sentence corrections, because the base prompt lets a voice block override rules 7, 9, and 11 when it asks for them explicitly.
- None of the five added a fact. The input had one claim and each output still has one claim.
