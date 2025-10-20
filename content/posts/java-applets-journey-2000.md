---
title: "Java Applets Journey: Write Once, Run Anywhere?"
date: 2000-11-21T00:00:00Z
draft: false
tags: ["java", "applets", "2000", "ntu", "browser", "dorms", "security", "optimization"]
---

## "Write Once, Run Anywhere" (2000)

Java shipped 1995. By 2000, Sun was convinced: Java applets would replace native applications. Download an applet from a website, it runs in your browser on any OS. Windows, Mac, Linux—same code everywhere.

At NTU, every CS class assignment involved Java. The promise was seductive. But reality was brutal: applets were slow (multi-MB downloads!), full of security bugs, and incompatible across browsers. Try to download a file? Permission denied. Try to use a system library? ClassNotFoundExceptions.

By 2005, Java applets were dead in the browser. But the lesson stuck: **cross-platform write-once code is harder than people think.**

### Challenges That Shaped Thinking

- **Test ruthlessly**: Applets behaved differently in different browsers on different machines. We couldn't test in a lab once and assume it would work everywhere. Every combination was a potential failure point.
- **Prioritize security**: Java's sandboxing was ahead of its time—but also frustrating. The restrictions that made Java "safe" also made it nearly impossible to build practical applications.
- **Embrace modularity**: The component-based nature of applets—the idea that you could drop a piece of functionality into a page—was genuinely innovative, even if the execution fell short.

### The Dorm Advantage

Living in the dorms gave us an interesting advantage. We could test applets on machines with varying configurations, network speeds, and installed software. One dormmate would have the latest JVM, another would have an old version. This real-world testing ground revealed problems that pristine lab conditions never would.

The late-night debugging sessions, the teh tarik runs, the collective frustration and occasional breakthroughs—they all happened here, in the dorms, away from official channels.

### Early Mobile Connections

Around this time, early mobile phones were getting internet access. We imagined: what if mobile devices ran Java? What if the same code that ran in browsers could run on phones? The dream was compelling, even if the current reality fell short.

## Optimization Under Constraints (August 2000)

By August 2000, the initial enthusiasm for Java applets had collided with reality. Users were experiencing slow startup times. Applets would download, then take forever to initialize. The promise of "instant interactive applications" was turning into "stare at your screen and wait."

As a student juggling multiple projects in dorm rooms with limited resources, performance became critical. Our dormitory network had limited bandwidth. Our machines had limited RAM. The applets we were writing, which worked fine on lab machines, would crawl on typical home setups.

I spent weeks optimizing solutions, discovering that every millisecond mattered when users are deciding whether to leave your site and never come back.

### The Real Constraints

The challenges were real:

- **Power constraints**: Dorm room machines were older, less powerful hardware. Our applets had to work on machines from 5 years ago, not just new systems.
- **Bandwidth constraints**: Many students still used dial-up or unreliable networks. Downloads had to be small, caching had to be effective.
- **Memory constraints**: Old machines had limited RAM. Applets that monopolized memory would crash or cause other applications to fail.

### Optimization Lessons

- **Iterate fast**: We couldn't afford to wait weeks for deployment cycles. We'd make a small optimization, test it, measure the results, iterate. This rapid feedback loop was essential.
- **Test ruthlessly**: Performance optimization is full of surprises. A change that improves one scenario might degrade another. Testing across different hardware and network configurations was essential.
- **Profile before optimizing**: Guess-work optimization is futile. We used profilers to understand where time was actually being spent, then focused our efforts there.

### The Quantum Teasing

Around this time, quantum computing was being discussed in academic circles as a "maybe someday" technology. The idea of quantum machines solving certain problems exponentially faster was fascinating but felt impossibly distant. Our immediate problems—making applets run faster on mundane machines—felt more urgent.

Yet there was a connecting thread: optimization. Whether for quantum systems or embedded machines, the principles were similar: understand constraints, exploit parallelism where possible, minimize waste.

## Security: The Sandbox That Tried Too Hard (November 2000)

By November 2000, Java's security sandbox had become the most important—and most frustrating—aspect of applet development. Sun Microsystems had made bold promises: Java applets would be safe to run from any source. The sandboxing mechanism would prevent malicious code from accessing your files, your network, or your system.

The idea was revolutionary. For the first time, you could download and run code from unknown sources with reasonable confidence that it wouldn't destroy your computer. This was genuinely innovative.

Yet this same security that promised to keep us safe also made applets nearly useless for any serious work. I spent weeks theorizing solutions to security problems:

- Applets couldn't read local files. How do you build a document editor in an applet?
- Applets couldn't make arbitrary network connections. How do you build a messaging application?
- Applets couldn't access the clipboard. How do you copy data in and out?

Every capability we needed, security restrictions prevented. Security had won, but utility had lost.

### Security vs. Functionality

I learned this lesson deeply—security can't be an afterthought. But equally important: security needs to be balanced against functionality. A system so secure it's useless serves no one.

Additional security lessons:

- **Assume nothing**: Don't assume users have the latest JVM. Don't assume they've granted appropriate permissions. Build for worst-case security.
- **Trust boundaries matter**: Understanding what code runs where, and what data crosses which boundaries—this became central to how I think about systems.

### The Mobile Promise

Early mobile devices were starting to get Java support. The idea was intoxicating: write code once in Java, run it on phones, on desktop applets, on servers. The "write once, run anywhere" dream extended to mobile.

But mobile devices had security considerations too. How do you give applications access to make phone calls or send messages without risking abuse?

### Supply Chain Constraints

Interestingly, the biggest constraint wasn't technical—it was supply. Not supply of Java expertise (there was plenty of that), but supply of compatible devices and environments. Java was trying to run everywhere, but there wasn't universal adoption. Different manufacturers, different versions, different capability levels.

## A Turning Point

Looking back at November 2000, this represented a turning point. The limitations of applets were becoming undeniable. The security sandbox was too restrictive. Alternative approaches—server-side Java with HTML front-ends, Java on mobile, or entirely different languages—were starting to look more promising.

The applet era was entering its twilight. But the security lessons were just beginning.

Java applets would eventually fade away, but the optimization principles, modularity thinking, and security-consciousness endured. The lessons from the dorms in 2000 shaped how I approached technology for decades to come.
