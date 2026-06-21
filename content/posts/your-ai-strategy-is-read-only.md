---
title: "Your AI Strategy Is Read-Only"
date: 2026-06-20T10:00:00-07:00
draft: false
tags: ["Juneteenth", "AI", "AI Strategy", "Enterprise AI", "RAG", "Tech Leadership"]
summary: "Why enterprise AI ROI sits upstream with a few model providers, and how owning the learning loop, not renting the outcome, brings that value home."
images:
  - /posts/your-ai-strategy-is-read-only/lead.jpg
---

![Your AI Strategy Is Read-Only](/posts/your-ai-strategy-is-read-only/lead.jpg)

*1,241 words · 7 min read*

*Disclaimer: This post reflects my personal views and does not represent the views of my employer or my community.*

*Caveat: This was written with research assistance from AI tools, but I curated the content, edited the draft, and cross-checked the references.*

*Image: The illustration above was generated with Grok.*

On June 19, 1865, Maj. Gen. Gordon Granger arrived in Galveston, Texas, and announced to enslaved people that they were free. The Emancipation Proclamation had promised freedom back on January 1, 1863, but in Texas, it remained just words until the Union army enforced it [1][2]. The law existed all along, but it had not reached them. For two and a half years, they were free on paper but not in reality.

This gap between what is promised and what is actually delivered is similar to how many companies approach AI. They talk about value before it truly arrives.

My team at OCI, working on GPU Infrastructure, has launched many AI applications that work as expected and are live in production. Even so, the returns often fall short or take time to show up, and the numbers support this. Deloitte's 2025 research found that only about one in five organizations is an AI ROI leader [3]. An MIT study found that about 95 percent of generative AI pilots had no clear impact on profits [4]. Gartner predicts that over 40 percent of agentic AI projects will be canceled by the end of 2027 because unresolved issues with cost, value, or risk controls [5].

The problem is not with the models themselves. This explains why the promised value takes so long to show up, and where it sits in the meantime.

## The diagnosis nobody wanted

In June 2026, Satya Nadella explained the reason, focusing more on economics than technology. When just a few base models take in everything, the value does not vanish. Instead, it collects with the few vendors who control those central models [6].

He compared this to the first wave of globalization. On the surface, the numbers looked good, but outsourcing ultimately weakened entire industries. By the time the real costs showed up, the ability to do the work was gone [6]. The takeaway was not that trade is bad, but that efficiency and ownership are not the same. A company can succeed in one area while quietly losing in another.

This is the risk with enterprise AI: good adoption numbers can hide the fact that lasting business value is moving to the key model providers. Your dashboard might show success, but the real power could be shifting away from you.

## Read-only AI

Most enterprise AI is still read-only. A user asks a question; the app finds relevant context; the model provides an answer; and the system logs it. After that, nothing new is learned.

At first, this seems like progress. But often, it just means a better interface on top of information that does not change. The system does not learn more about your business over time. The real question is: after a year, what does our AI know that others do not? If the answer is nothing unique, then the company has built usage, not real value.

## The subtle part is the important part.

Nadella did not suggest hiding the data. Raw data by itself is not the real asset. The true value comes from the learning loop, built from your workflows, domain knowledge, and your team's judgment. This loop improves the more your business uses it. He described it as building both human capital and token capital: token capital is the AI capability your company owns, and human capital is your people's judgment [7].

He gives a simple test for owning that learning loop: can you change to a different general model without losing the expertise your systems have built up [7]? If switching providers means starting over, you do not own the asset. You are just renting it, following someone else's rules. Most companies would not pass this test today, and many have not even considered it.

## Is RAG dead?

This leads to a question I keep getting asked: Is RAG obsolete?

No. AWS defines retrieval-augmented generation as a method in which a model consults an authoritative knowledge base beyond its training data before answering [8]. NVIDIA describes it as grounding generative AI in specific, relevant sources [9]. That is useful. It helps with freshness and grounding, but RAG is just a way to retrieve information, not a full strategy. If you treat it as your only approach, you end up with a faster search through static documents. Good production systems need more: the quality of a RAG system depends on how well it retrieves information, the quality of its answers, human review, and its ability to keep things on track [10]. A strong platform also needs private evaluations, feedback-collection mechanisms, and a process for experts to make corrections that improve future results. Without this learning loop, retrieval stays the same and does not improve. Teams that say RAG is obsolete often built only the first part and skipped the rest.

## Where the value shows up

ROI often seems slow because we look for it at the wrong times, like during demos, pilots, or launches. A learning loop does not pay off right away. The real value shows up months later, after it has seen your operations, learned from mistakes, handled unusual cases, and taken in feedback from your experts. No ready-made model can match this, because none have worked in your environment.

Think about a support assistant that solves more tickets each month, not because the base model got better, but because it learned which answers your top agents rely on. That kind of improvement is the real asset. It will not show up in a demo; it is yours, and it is tough for others to copy.

From where I sit, building AI and GPU infrastructure at OCI, the pattern is clear. The companies pulling ahead did not simply pick the best model. Models are a commodity that influences whether you act. These organizations chose to own the learning loop rather than rent the outcome.

## What to do on Monday

The answer is simple, even if it is not trendy. Stop focusing on rating vendors and start measuring outcomes. Create private evaluations based on what matters to your business, and let those results define success instead of relying on public benchmarks.

Build your learning loop on infrastructure you control, and make sure you can switch models from the start. That way, if your provider changes its terms, it is just another day, not a crisis.

See your organization's judgment as an asset to capture. When a senior engineer makes a correction, it is not just a chat message. It is your company's memory in action. Save it, keep it within your organization, and use it to improve your systems.

I have celebrated the launch of another AI app, just like anyone else. But the more important question is: Did we also create another learning loop?

This idea goes beyond just companies; it applies to entire countries. Either you own the learning loop, or you end up renting your future.

## The point of the holiday

If your freedom depends on someone else's system, it was never truly yours. It is a license, not a right, and a license can always be revoked when it comes up for renewal.

The ROI from all those AI applications is not missing. It has been there all along. It is just sitting upstream, like freedom once did in law before it finally reached the people it was meant for. So let us build the learning loop that brings that value home.

In God we trust. All others bring data.

---

## References

1. National Archives, "National Archives Safeguards Original Juneteenth General Order." [https://www.archives.gov/news/articles/juneteenth-original-document](https://www.archives.gov/news/articles/juneteenth-original-document)
2. HISTORY, "Juneteenth: Why It Took 2.5 Years for Freedom to Reach Texas." [https://www.history.com/articles/juneteenth-emancipation-proclamation-texas](https://www.history.com/articles/juneteenth-emancipation-proclamation-texas)
3. Deloitte, "AI ROI: The paradox of rising investment and elusive returns." [https://www.deloitte.com/global/en/issues/ai/ai-roi-the-paradox-of-rising-investment-and-elusive-returns.html](https://www.deloitte.com/global/en/issues/ai/ai-roi-the-paradox-of-rising-investment-and-elusive-returns.html)
4. Fortune, "MIT report: 95% of generative AI pilots at companies are failing." [https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/)
5. Gartner, "Gartner Predicts Over 40 Percent of Agentic AI Projects Will Be Canceled by End of 2027." [https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
6. VentureBeat, "Satya Nadella warns that AI could hollow out entire industries, echoing the damage done by globalization." [https://venturebeat.com/technology/satya-nadella-warns-that-ai-could-hollow-out-entire-industries-echoing-the-damage-done-by-globalization](https://venturebeat.com/technology/satya-nadella-warns-that-ai-could-hollow-out-entire-industries-echoing-the-damage-done-by-globalization)
7. The Indian Express, "Don't let a few models eat everything: Satya Nadella's blueprint for the AI-era firm." [https://indianexpress.com/article/technology/tech-news-technology/satya-nadella-token-capital-ai-blueprint-microsoft-10739746/](https://indianexpress.com/article/technology/tech-news-technology/satya-nadella-token-capital-ai-blueprint-microsoft-10739746/)
8. AWS, "What is RAG? Retrieval-Augmented Generation AI Explained." [https://aws.amazon.com/what-is/retrieval-augmented-generation/](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
9. NVIDIA, "What Is Retrieval-Augmented Generation, aka RAG?" [https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)
10. Dean Wampler, Dave Nielson, and Alireza Seddighi, "Engineering the RAG Stack: A Comprehensive Review of the Architecture and Trust Frameworks for Retrieval Augmented Generation Systems." [https://arxiv.org/html/2601.05264](https://arxiv.org/html/2601.05264)
