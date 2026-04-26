---
title: "A Short History of AI: From Greek Myths to Large Language Models"
date: 2026-03-28T12:00:00-07:00
draft: false
tags: ["AI", "history", "machine learning", "LLM"]
---

![A Short History of AI: From Greek Myths to Large Language Models](/posts/a-short-history-of-ai-from-greek-myths-to-large-language-models/history-of-ai.png)

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

# A Short History of AI: From Greek Myths to Large Language Models

Humans have been dreaming up artificial beings for millennia. For example, in Greek myths, Hephaestus was at a forge, creating metal servants. Similarly, Jewish folklore offered the golem, a clay figure infused with life. Meanwhile, in China and the Islamic world, engineers designed automata: devices that moved, poured drinks, and played music. For decades, philosophers debated whether thought could obey rules and whether anything other than a person could reason. Clearly, the dream of artificial intelligence is ancient. The science is not [10].

## The Science Begins (1940s-1950s)

In the 1940s, engineering replaced imagination. In 1943, Warren McCulloch and Walter Pitts published the first mathematical model of how neurons might work [1]. It’s abstract stuff, but it worked: logic’s building blocks -- true, false, and, or -- could exist within the confines of a formal system. This paper is often cited as the root of both neuroscience and AI.

Alan Turing went bolder in 1950 with *Computing Machinery and Intelligence*: Can machines think? [2] He avoided endless philosophy and provided something that can be tested. If a machine could converse and a human could not tell one from the other, calling it 'unintelligent' would become awkward. Turing never delivered a thinking machine; he left the rest of the field a finish line.

The name arrived in 1956. At Dartmouth, John McCarthy ran a summer workshop and argued that learning and intelligence could, in principle, be specified finely enough for a machine to imitate [3]. He described the project as “artificial intelligence.” Attendees were wildly optimistic: several thought human-level machine intelligence was a decade away. They were off by decades. The timeline was incorrect; the direction did not move either.

## Early Programs and the AI Winters (1960s-1980s)

The early programs came across as intelligent for their era. The Logic Theorist [11] and ELIZA (1966) [12] flattered back small talk with scripts. The catch: hand-coded rules. Reality has more angles than any rule list can hold.

Then progress froze twice. The first “AI winter” arrived in the 1970s, when funders realized that hype had outpaced outcomes [10]. Money thinned. We had a brief renaissance of that in the 1980s with expert systems, including MYCIN, which diagnosed blood infections via hundreds of if-then rules written by doctors [4]. Clients threw money at it, yet systems collapsed when they operated outside their rule books. And then winter came again, by the late 1980s. A field that once held promise of humanlike thinking nearly perished twice. That time is glossed over in cheerier accounts; it matters. AI was never a smooth ramp.

## Letting Machines Learn (1990s-2000s)

The field advanced when researchers asked a new question: Instead of defining rules, could machines learn rules by examining examples?

That is one line summary of machine learning. Spoon enough examples into the maw and trends emerge. A few hundred thousand cat and dog photos, and the system figures out the split without a lecture about whiskers. Back-propagation and better optimization (1986 onwards) gradually made deep nets teachable [5], but the big unlock was data + compute, not a single slick trick.

Neural networks, a mathematical structure loosely inspired by brain wiring, were already outlined in 1943 [1], but they worked only once computers became fast and datasets became massive.

In 1997, Garry Kasparov lost to IBM’s Deep Blue in a chess match [6]. Raw power, not mysticism: millions of moves per second searched. Yet a machine had conquered the game that people considered the height of intellect.

## Deep Learning Changes the Game (2010s)

In 2012, a team from Toronto submitted to an image contest, plumbing AlexNet: deep nets with many layers that take features from raw pixels [7]. Edges low down; shapes above that; upwards, objects and faces. AlexNet didn't just squeak past the field; it nearly cut error rates in half.

And two enablers he couldn’t spot at once. The internet had dumped vast mounds of labeled images and text to learn from. And gaming hardware was precisely what Matrix Math Networks needed. No one planned that pairing; it is pure luck.

The wave of deep learning came: images, speech, text, video. In 2016, DeepMind’s AlphaGo defeated a world champion at Go, a game with more positions than there are atoms in the observable universe [8]. No set script: it learned by playing itself over and over.

## The Language Breakthrough (2017-Present)

Transformers were introduced in 2017 when Google released *Attention Is All You Need* [9]. Attention allows the model to choose which words in a sentence matter most when predicting the next one, so context from across the sentence, not just the previous few tokens, informs each prediction. That opened the door to training on massive amounts of text and with models containing billions of parameters.

Transformers are the foundational structure of today’s large language models. After initial hesitation, OpenAI released GPT-2, followed by GPT-3, with around 175 billion parameters, much larger than its predecessors [13]. ChatGPT, based on GPT-3, launched in November 2022. *Reuters* later reported UBS estimates that ChatGPT reached roughly 100 million monthly active users within two months of launch, a rate analysts called the fastest ramp they had seen for a consumer internet app [14]. AI ceased being something for the lab. It resided in unremarkable browsers.

Since then, GPT-4, Gemini, Claude, LLaMA, and others have piled on. They program, summarize, translate, and chat in ways so convincing they may as well be a sharp human, until you poke at the edges. They do not think as humans do. They guess the likely next tokens from all that has gone before [9][13]. Do that at a massive scale, and something useful, and occasionally eerie, develops.

## What Comes Next

What we have now is still narrow AI: very strong on specific tasks, very weak on any kind of grounded model of how the world works [10]. ChatGPT doesn’t “know” in the same way we do; it compares patterns of text. Reliability continues to break down on edge cases, math without guardrails, and anything that requires verified facts in the wild [10].

The next, argued-over label is AGI, artificial general intelligence: a system that could learn any intellectual task a human can learn, hop domains, and tackle genuinely novel problems [10]. It does not exist yet. Speculation about timing ranges from a few years to many decades, and the definition itself evolves with each benchmark solved.

Building on this, the stage after AGI is known as ASI (superintelligence), which would surpass the best humans in every domain [10]. While ASI remains mostly speculative, it plays a role in serious safety work. Its utility is nearly taken for granted; control remains the difficult part.

Hephaestus forged servants in myth. Turing wondered whether machines could think. Today, hundreds of millions of people communicate with machines daily. The thread connecting old stories to today’s tools is much longer than a headline might imply, and the next chapters play out in real time.

---

## References

1. McCulloch, W. S. & Pitts, W. (1943). "A Logical Calculus of the Ideas Immanent in Nervous Activity." *Bulletin of Mathematical Biophysics*, 5(4), 115-133.
2. Turing, A. M. (1950). "Computing Machinery and Intelligence." *Mind*, 59(236), 433-460.
3. McCarthy, J., Minsky, M., Rochester, N. & Shannon, C. (1955). "A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence." [https://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html](https://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html)
4. Shortliffe, E. H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.
5. Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors." *Nature*, 323, 533-536. [https://www.nature.com/articles/323533a0](https://www.nature.com/articles/323533a0)
6. IBM. "Deep Blue." [https://www.ibm.com/history/deep-blue](https://www.ibm.com/history/deep-blue)
7. Krizhevsky, A., Sutskever, I. & Hinton, G. E. (2012). "ImageNet Classification with Deep Convolutional Neural Networks." *NeurIPS*. [https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks)
8. Silver, D. et al. (2016). "Mastering the game of Go with deep neural networks and tree search." *Nature*, 529, 484-489. [https://www.nature.com/articles/nature16961](https://www.nature.com/articles/nature16961)
9. Vaswani, A. et al. (2017). "Attention Is All You Need." *NeurIPS*. [https://papers.nips.cc/paper/7181-attention-is-all-you-need](https://papers.nips.cc/paper/7181-attention-is-all-you-need)
10. Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
11. Newell, A., Shaw, J. C. & Simon, H. A. (1956). "The Logic Theory Machine: A Complex Information Processing System." *IRE Transactions on Information Theory*, 2(3), 61-79.
12. Weizenbaum, J. (1966). "ELIZA: A Computer Program for the Study of Natural Language Communication Between Man and Machine." *Communications of the ACM*, 9(1), 36-45.
13. Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS*. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
14. Hu, K. (2023). "ChatGPT sets record for fastest-growing user base." *Reuters*. [https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/](https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/)
