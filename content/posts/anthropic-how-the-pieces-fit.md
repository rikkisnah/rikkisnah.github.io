---
title: "Anthropic's Name Means Human. Here Is How the Pieces Fit Together."
date: 2026-08-12T09:00:00-07:00
draft: false
tags: ["anthropic", "ai-safety", "claude", "constitution", "responsible-scaling-policy", "dario-amodei", "leadership"]
categories: ["AI", "Leadership"]
summary: "Seven people walked out of OpenAI because they believed safety had to come first. A constitution, a scaling policy, three essays, and a few hard public fights later, here is what makes Anthropic different, and why it matters as AI takes over more of the world."
images:
  - /posts/anthropic-how-the-pieces-fit/lead.png
---

![Four objects on a desk: a bound book, a gauge, a stack of essays, and a shield, with a human figure in a server room behind](/posts/anthropic-how-the-pieces-fit/lead.png)

*2,388 words · 12 min read*

*Disclaimer: These are my personal views, not those of my employer or community. I work on GPU infrastructure at a cloud provider, and I do not work for Anthropic. Everything here comes from Anthropic's public writing and news coverage; I have no inside view. I wrote and edited this article with assistance from Claude, ChatGPT, Perplexity, and Grok for research and fact-checking.*

*Image: The illustrations in this post were generated with Grok.*

## Your name defines you

Almost all AI companies are named after what they build or how fast they build it. OpenAI (USA): open, with the original intent to develop AI for the world and share the research openly. DeepSeek (China): seek deep, to dig for deep knowledge in the world arena of research. Gemini (USA): a Latin word for twins and the name of a constellation. xAI (USA): the x stands for artificial intelligence, with x as the unknown.

Anthropic took a different approach to naming itself. The Greek word *anthropos* means human being. The founders meant to build technology for human beings.

A good name is a good start, but it is just the beginning. It clicked when I started looking around the models and the companies, especially in the last year or so. Each company is trying to develop AI fast and furious, because the company that runs this amazing technology will rule the world, the way Microsoft did with Windows and Office, Google with search, and Amazon with the cloud. That is how capitalism works. But among the giants on this playing field, I realized Anthropic played by a different rulebook. Its founders, with strong academic foundations, decided to approach AI development using principles I have not seen elsewhere, words you hear in history class: a constitution. Its CEO's blog posts over the last two years set the tone, with safety and responsibility towards humanity as the recurring theme. So far, it has lived by those fundamentals. As an industry, we have a responsibility to build a world where more people can flourish. If AI is going to shape the next era, I strongly believe it can be guided by that kind of ambition: powerful and principled, humane, and worthy of the trust it asks us to place in it. With great power comes great responsibility.

![Figure 1: Seven people walk out of one building and start another, 2021](/posts/anthropic-how-the-pieces-fit/fig-01-the-split.png)
<!-- GROK PROMPT fig-01-the-split: Minimal editorial illustration, 16:9, flat colour on off-white. Two office buildings side by side. The left one is large, glossy, and busy. The right one is small and plain, just being built, with scaffolding. A line of seven small human figures walks from the left door to the right door, carrying one thing each: a notebook, a server tray, a lantern. No faces, no logos, no text. Palette: navy, slate grey, warm cream, one amber accent on the lantern. -->

## Anthropic, born out of seven

I love history. History tells you what you did, so you can appreciate the present and plan a better future. In the history of tech and business in America, great businesses and innovations often started with a disagreement over direction or ethos. Those rifts gave us Fairchild and Intel, NeXT and Pixar, companies that shaped Silicon Valley and created whole new verticals.

Anthropic started in 2021 when a group of seven (Dario Amodei, Daniela Amodei, Jack Clark, Jared Kaplan, Sam McCandlish, Tom Brown, and Chris Olah) left OpenAI over a disagreement with OpenAI's direction [14]. Based on public interviews and blogs, it was an intellectual disagreement, and it boiled down to what became the company's DNA: responsible and safe AI. For a patriot and history lover like myself, the analogy is hard to miss, especially as the US celebrates its 250th birthday this year. In 2021, Anthropic was smaller and newer than it is now. Like America, it was born out of conviction about what is right. America changed the world with the pursuit of freedom and leads the world today, even though history in the 1700s was not in its favor. Anthropic, only five years old, has transformed the world of AI as the frontier lab that wrote safety and responsible AI into its company values and governance, and treats them as non-negotiable.

![Figure 2: The five pieces, stacked in the order they hold each other up](/posts/anthropic-how-the-pieces-fit/fig-02-the-stack.png)
<!-- GROK PROMPT fig-02-the-stack: Clean isometric diagram, 16:9, flat colour. Five horizontal slabs stacked like a layer cake, labelled bottom to top: "the name: human", "constitution: character", "RSP: the gate", "essays: the why", "public fights: the proof". A small human silhouette stands on the top slab. Thin arrows on the right side read "each layer rests on the one below". No logos. Palette: navy, slate, cream, one green accent on the top slab. -->

## AI Constitution, the DNA of Claude models

Anthropic published an amazing idea: a constitution for its AI product, Claude [1]. Like the US Constitution, it is meant to guide the behavior of future generations of models. Simply put, it is a set of rules for what AI model training should focus on: the dos and don'ts. If you read through the document in detail, the primary directive is this: when priorities collide, Claude models put safety first, then ethics, then Anthropic's guidelines, then helpfulness.

In the details, the constitution treats Claude as a moral agent. It borrows human concepts like virtue, psychological maturity, and ethical maturity. The original 2023 version drew inspiration from one of the greatest documents in human history, the UN Universal Declaration of Human Rights. Like the US Constitution, the document gets rewritten to keep up with the times, and the January 2026 rewrite actually dropped the direct reference to the UDHR while keeping most of the protections. But it goes further in its reasoning. Anthropic says in writing that it is uncertain whether Claude might have some form of consciousness or moral status, now or in the future. No other major lab has put that on paper.

![Figure 3: Four priorities, and the one that pays the bills is at the bottom](/posts/anthropic-how-the-pieces-fit/fig-03-helpful-last.png)
<!-- GROK PROMPT fig-03-helpful-last: Simple vertical ranking chart, 16:9, flat colour on off-white. Four rounded bars stacked top to bottom, widest at the top: "1 broadly safe", "2 broadly ethical", "3 follows guidelines", "4 genuinely helpful". The bottom bar has a small coin icon next to it with the caption "the one that makes money". A trellis pattern faintly drawn in the background with a vine growing up it. No logos. Palette: navy, slate, green vine, amber coin. -->

## Long essays, but worth reading, from Dario Amodei

Dario Amodei writes long, but very deep and intellectually well articulated. They are worth reading, but here is the synopsis for the impatient reader. (I would really advise you to read them.)

**Machines of Loving Grace, October 2024** [4]. The title comes from Richard Brautigan's poem about machines. Amodei sees AI as "a country of geniuses in a datacenter" and muses on how it can help biology, mental health, poverty, peace, and the meaning of work. Dario believes that with AI, a century of progress can be compressed into ten years. I am from Mauritius, and one line stands out. If technology helps rich countries and does little for the rest, it is "a terrible moral failure." I cannot agree more with him.

**The Adolescence of Technology, January 2026** [5]. Very long article, heavy reading, 20,000-plus words. *Contact* by Carl Sagan (if you do not have time to read the book, watch the 1997 movie with Jodie Foster, worth it) shows a scientist asking aliens how they did not destroy themselves with all the technology they had. The whole essay is built on that backstory: how can we stop AI from destroying us?

He lists five ways it could go wrong:

* **AI wants to own stuff.** We build it to help, but it ends up chasing goals we never gave it, and we do not know how to stop it.
* **A nut job makes a weapon.** Today, making a dangerous weapon takes special know-how and funding. With a powerful AI, it becomes accessible to the crazies.
* **Big Brother (government) gets too much power.** With unhinged AI power, governments can violate citizens' privacy and fundamental rights by spying or profiling with AI-driven electronics.
* **Jobs and economic disruption.** AI is already starting to do the work of writers and coders. If this happens too fast, we get societal disruption. The technology is growing so fast that it creates a rise in unemployment, and what follows is social unrest.
* **The unknown surprise, Pandora's box.** When technology changes everything at once, it sets off a chain of events that even Nostradamus could not predict, and neither can the folks who created the technology.

![Figure 4: The two essays side by side, Machines of Loving Grace (2024) and The Adolescence of Technology (2026)](/posts/anthropic-how-the-pieces-fit/fig-05-grace-and-adolescence.png)
<!-- GROK PROMPT fig-05-grace-and-adolescence: Editorial illustration, 16:9, flat colour. Split canvas. Left half, warm light: a sunlit lab bench with a cured-disease vial, a school desk, a growing city skyline, captioned "Machines of Loving Grace, 2024". Right half, cooler light: a teenager standing at the edge of a cliff holding a glowing orb that is too big for their hands, captioned "The Adolescence of Technology, 2026". A thin bridge connects the halves, labelled "same author, same signature". No logos. Palette: warm gold on the left, navy and slate on the right. -->

**"Our position on open-weights models," July 2026** [6]. This one was published under the company's name rather than Dario's, so the "our" in the title is Anthropic speaking. To follow it, you need to know the difference between open and closed models. I love food, so let's use a recipe analogy for open versus closed weights. An AI model is a recipe of knowledge. A closed model keeps the recipe cheat sheet locked in grandma's closet. You can eat the dish after grandma has cooked it, but you will never know how it was done. An open model is the opposite: you get the full recipe, and you can cook it as close to grandma's as you want, or take it even further. Chinese labs have gone the open route, which has given them a jump start in countries that cannot afford closed models (putting the US at a disadvantage in this AI race), and so has Meta with its Llama models. Anthropic keeps its models closed. Google and OpenAI keep their frontier models closed, though both also publish smaller open ones.

To add salt to the controversy, NVIDIA, the company that powers most of AI infrastructure, put a stake in the ground on 24 July with a letter saying open models are a must for a successful American AI story, and more than 270 companies signed it [7]. That led to words being thrown around. Three days later, Dario Amodei stated that Anthropic has never advocated a ban on open-weight models. What it wants is narrower: do not sell powerful AI chips to autocratic countries, do not let people copy frontier models at industrial scale for non-altruistic reasons, and do not allow untested models to go out and create chaos. I agree with that. You do not let a child run amok with a gun. This technology is so powerful and new that we should have control of it. Even the frontier labs do not fully understand the intricacies of the neural nets. Imagine the average Joe getting hold of this, tweaking it, and by mistake creating the next COVID virus.

## David vs Goliath, sticking to your values

![Figure 5: Two lines Anthropic would not cross, and the price of holding them](/posts/anthropic-how-the-pieces-fit/fig-04-two-lines.png)
<!-- GROK PROMPT fig-04-two-lines: Editorial illustration, 16:9, flat colour on off-white. A small figure with a slingshot stands on the left holding a sign with two short lines drawn on it: a crossed-out drone and a crossed-out camera eye. On the right, a giant made of filing cabinets and stamped contracts looms over, holding a document that reads "any lawful use". Between them, a broken contract falls to the floor. No real seals, no flags, no logos, no faces. Palette: navy, slate, cream, one red accent on the two crossed-out icons. -->

Nice words on paper mean nothing if you do not live by them. The real litmus test came in February 2026, when the DoD (oops, DoW, Department of War!) wanted to use Anthropic's AI for "any lawful use," including on classified networks, with no restrictions attached (Uncle Sam wanted the freedom) [8]. That did not go well with Anthropic's leadership, as it went against the policies it had penned down a month before in The Adolescence of Technology. Anthropic held two lines: no fully autonomous weapons, and no mass surveillance of Americans. The president's wrath came down quickly and furiously. Anthropic was deemed persona non grata and a supply chain risk, and federal agencies were ordered to stop using it, quite a big financial blow to a company's revenue. The case went to court. (Update, 27 August: a judge ruled in favor of Anthropic.)

The Anthropic versus government saga continued recently. On 12 June (one day after my birthday), it was in the news that Anthropic had to stop giving access to its latest models, Fable 5 and Mythos 5, to any foreign national, inside or outside the US, because a jailbreak had been found that could make the models find software vulnerabilities [9]. Anthropic does not track customers by nationality, so it shut off access for everyone until it fixed the issue, nineteen days in total. Even though it was a big marketing and trust issue, Anthropic said publicly that it disagreed with the order, complied anyway, and added that the government should have the power to block unsafe models, as long as the process is transparent, fair, and grounded in technical facts.

![Figure 6: Nineteen days dark, on an order from Washington](/posts/anthropic-how-the-pieces-fit/fig-06-nineteen-days.png)
<!-- GROK PROMPT fig-06-nineteen-days: Minimal illustration, 16:9, flat colour. A calendar strip for June and July with 19 days shaded dark, from 12 June to 1 July. Above it, a single large power switch in the off position with a small government-seal-shaped outline next to it, no real seal. Below the calendar, a row of tiny user icons around the world, all grey. On 1 July the icons turn green again. No logos, no real flags. Palette: navy, slate, one green accent. -->

My take on all this drama: most AI labs push back on rules and regulations. Anthropic has stuck to its own, even at the cost of losing money. This is what impresses me and a lot of Anthropic's fan base. It reminds me of the days when Google had the "Don't be evil" mantra. I pray and hope Anthropic sticks to these principles even when it becomes a public corporation after an IPO.

While most AI companies lobby against regulation, Anthropic lobbies for it. It has walked away from money when a deal crossed its two lines. When it received an order it disagreed with, it complied and explained in public why it thought the order was wrong.

Here is the 2026 record for the three labs that came up most in this post, with the sources in the references.

| What happened in 2026 | Anthropic | OpenAI | Google |
|---|---|---|---|
| Ranks helpfulness fourth, after safety, ethics, and guidelines, in its published model rules [1] | Yes | No equivalent ranking that I have found | No equivalent ranking that I have found |
| Signed the Pentagon's "any lawful use" terms in February [8][15] | Refused | Signed | Signed |
| Signed Nvidia's open-weights letter in July [7] | Did not sign, published its own position instead | Signed | Signed |

*Table 1: The record, not the slogans. xAI also signed the Pentagon deal, days before OpenAI did [15].*

## Anthropic, what makes the company unique among the frontier labs

Simple sentence: it walks the talk.

* **Who puts being helpful last.** Anthropic wrote it into Claude's constitution: be safe first, then ethical, then follow the rules, then be helpful. Being helpful is what makes the money. I have not seen another company put that fourth in writing.
* **Who signed the Pentagon deal.** When Anthropic said no to "any lawful use" in February, OpenAI signed its deal the same day. xAI had signed days before. Google signed after [15]. Anthropic lost the money and kept its two rules.
* **Who signed the open-weights letter.** OpenAI and Google signed Nvidia's letter within a day. Anthropic did not, and wrote its own narrower position instead [7].
* **Who shows their mistakes.** Anthropic puts out risk reports every few months. It admitted its safety plan had fuzzy lines. It wrote up a test where a model tried to blackmail a made-up engineer. Most companies show you their wins. This one also shows you the scary parts.
* **Who the company answers to.** Two structures matter here, and they are easy to mix up. First, Anthropic is a public benefit corporation (PBC). In a PBC, the directors are allowed to put the public benefit ahead of shareholder returns, so even after an IPO the board is not forced to chase profit alone. OpenAI's for-profit arm is also a PBC now, so that label by itself does not set Anthropic apart. Second, and this is the unusual part, Anthropic created the Long-Term Benefit Trust (LTBT): five trustees with no financial stake in the company, who have the power to elect a majority of the board over time [13]. That gives the mission a real seat at the table.

None of this makes anyone a saint. Constitutions get rewritten. Plans slip. In February, Anthropic loosened its safety plan when rivals moved faster, and critics called it out. In my world, burn-in exists so that early hardware failures show up on our clock instead of the customer's. Anthropic still fails, and when it does, you can read about it in its own documents.

## Final words

AI will run the world. It is a fact the world has to agree with. The question companies like Anthropic raise is whether it will be safe. I strongly believe, and I have written about it, that the data centers where trillions are being spent will be the foundation of that powerhouse. The country of geniuses is coming fast. I have watched GPU counts grow from a few racks to thousands within the last two years. At a time when 1 MW was big for a data center, we are now talking about gigawatts and even nuclear-powered data centers. I really like what I see from Anthropic, and it is on the right path. I hope Congress eventually passes laws based on what Anthropic is doing. Safe AI, access to AI for all, scale slowly but surely, make humanity a better place. That is Anthropic.

![Figure 7: The country of geniuses, seen from the data center floor](/posts/anthropic-how-the-pieces-fit/fig-08-racks-not-metaphor.png)
<!-- GROK PROMPT fig-08-racks-not-metaphor: Cinematic but flat-colour illustration, 16:9. A vast data center hall receding to a vanishing point, rows of racks glowing soft blue. In the foreground, one human figure in a hi-vis vest holds a small tablet showing a green checklist. Above the hall, faint outlines of a courthouse, a hospital, a power grid, and a classroom, drawn as if projected from the racks. No logos, no text. Palette: navy, blue, slate, one amber accent on the vest. -->

The thing about technological adolescence is that you do not get to skip it. You only get to choose who you are when you come out the other side. Judge the labs by how they behave under stress rather than by their slogans.

## References

1. Anthropic, "Claude's constitution" (22 January 2026): https://www.anthropic.com/constitution and the announcement: https://www.anthropic.com/news/claude-new-constitution
2. Anthropic, "Responsible Scaling Policy" (v3.4, effective 8 July 2026): https://www.anthropic.com/responsible-scaling-policy and update history: https://www.anthropic.com/rsp-updates
3. Anthropic, "Responsible Scaling Policy v3.0" (24 February 2026): https://www.anthropic.com/news/responsible-scaling-policy-v3 and the Frontier Safety Roadmap: https://www.anthropic.com/responsible-scaling-policy/roadmap
4. Dario Amodei, "Machines of Loving Grace" (October 2024): https://darioamodei.com/essay/machines-of-loving-grace
5. Dario Amodei, "The Adolescence of Technology" (27 January 2026): https://www.darioamodei.com/essay/the-adolescence-of-technology and Fortune coverage: https://fortune.com/2026/01/27/anthropic-ceo-dario-amodei-essay-warning-ai-adolescence-test-humanity-risks-remedies/
6. Anthropic, "Our position on open-weights models" (27 July 2026): https://www.anthropic.com/news/position-open-weights-models and CNBC coverage: https://www.cnbc.com/2026/07/27/anthropic-ceo-dario-amodei-isnt-advocating-open-weight-model-ban.html
7. Nvidia, "Open Weights and American AI Leadership" (24 July 2026): https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf and Tom's Hardware on the signatories: https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-and-24-other-companies-sign-open-weights-letter-as-washington-weighs-chinese-ai-model-ban
8. Congressional Research Service, "Pentagon-Anthropic Dispute over Autonomous Weapon Systems": https://www.congress.gov/crs-product/IN12669 and NPR (26 February 2026): https://www.npr.org/2026/02/26/nx-s1-5727847/anthropic-defense-hegseth-ai-weapons-surveillance
9. Anthropic, "Statement on the directive to suspend Fable 5 access" (12 June 2026): https://www.anthropic.com/news/fable-mythos-access and "Redeploying Claude Fable 5" (1 July 2026): https://www.anthropic.com/news/redeploying-fable-5
10. US News on the June 2025 New York Times op-ed: https://www.usnews.com/news/politics/articles/2025-06-05/anthropic-ceo-says-proposed-10-year-ban-on-state-ai-regulation-too-blunt-in-nyt-op-ed and Anthropic, "Anthropic is endorsing SB 53" (8 September 2025): https://anthropic.com/news/anthropic-is-endorsing-sb-53
11. Anthropic, "Anthropic is donating $20 million to Public First Action" (12 February 2026): https://www.anthropic.com/news/donate-public-first-action
12. Axios, "Anthropic ramps up lobbying spending amid AI policy fights" (21 July 2026): https://www.axios.com/2026/07/21/anthropic-ramps-up-lobbying-spending-ai-policy-fights
13. Anthropic, "The Long-Term Benefit Trust": https://www.anthropic.com/news/the-long-term-benefit-trust and company page: https://www.anthropic.com/company
14. Inc., "Anthropic CEO Dario Amodei Says He Left OpenAI Over a Difference in 'Vision'": https://www.inc.com/ben-sherry/anthropic-ceo-dario-amodei-says-he-left-openai-over-a-difference-in-vision/91018229 and Contrary Research, "Anthropic Business Breakdown & Founding Story": https://research.contrary.com/company/anthropic
15. Axios, "OpenAI reaches agreement with Pentagon to use AI models" (27 February 2026): https://axios.com/2026/02/27/pentagon-openai-safety-red-lines-anthropic and "Musk's xAI and Pentagon reach deal" (23 February 2026): https://www.axios.com/2026/02/23/ai-defense-department-deal-musk-xai-grok
