---
title: "Karpathy's LLM Wiki Changes Everything #LLMWiki #andrejkarpathy #knowledgemanagement"
source: "https://www.youtube.com/watch?v=04z2M_Nv_Rk"
author:
  - "[[FluxStack]]"
published:
created: 2026-04-30
description: "Andrej Karpathy's LLM Wiki pattern is quietly changing how we create  personal knowledge bases. In this video I break down what it is, why it matters, and bu..."
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=04z2M_Nv_Rk)

Andrej Karpathy's LLM Wiki pattern is quietly changing how we create personal knowledge bases. In this video I break down what it is, why it matters, and bu...

## Transcript

### Intro

**0:00** · Hi all, welcome back to the channel.

**0:01** · Today we will talk about LLM wiki. So Andre Karpati dropped a tweet his idea stop making LLMs reread your documents make it compile them. He calls it LLM wiki and by the end of the video you will make your own LLM wiki. We will go through who and what is LLM wiki exactly the three tier architecture the three operations you will be building your own LLM wiki. So I will be showing you a demo and you can basically follow. We will see rag versus LLM Viki. Uh we will see the rear comparison between them and we'll see why it matters.

**0:32** · So let's start.

### WHO & WHAT

**0:41** · Uh let's look at his tweet first. He told that something he's finding useful recently is for LLM to build personal knowledge bases on various topic of research interest using less of his tokens into manipulating code and more of his tokens into manipulating knowledge which is stored as markdowns and images. So he told that the latest are very good at data inest. So data inest basically he will have some source documents. So they can be articles, they can be papers, repos, data sets, images.

**1:11** · uh you have to put that in row directory and then llm will be used to compile it.

**1:16** · He will be using LLM to look at these source files into this raw directory and then LLM will compile a wiki from the raw files in collection of MD files uh with directory structures and it will also include back links. Uh it will categorize them into concepts, write articles on them, links them all and he uses this Obsidian web clipper extension to convert web articles into MD files.

**1:41** · for IDE basically for UI he uses obsidian to see the compile wiki as a front end and derived visualization and the important thing is LLM will write and maintains the data in the wiki he will not even touch it once his wiki is big enough so his wiki is approximately

**1:59** · 100 articles and 400 keywords he will ask his llm complex questions against the wiki it will go off and search the answers and he didn't went for rack because currentm are pretty good at maintaining index files and brief summaries of all the documents and it reads all the important related data fairly easily and instead of getting answer in text and terminal he will render markdown files and he will again uh put those markdown files into uh the

**2:28** · LLM so that it will enhance LLM's response next time for the further query. to his own exploration and queries always adds up the knowledge base he has. One important thing is with this kind of setup there are chances that hallucination may enter the knowledge base. If you are ingesting some query which came back from LLM to your knowledge base there are chances that LLM has done some kind of hallucination there. If you are feeding that hallucinated file to your knowledge base then uh it will reflect on everything.

**2:59** · So a linting is very essential here. It is kind of health check for the wiki and this linting process is kind of a health check for our wiki and uh it will find inconsistent data, missing data. It will find connection to new article candidates and it will clean up your wiki and enhance data integrity. LLMs are very good at suggesting further questions to ask and look into. He has found it very interesting. He's also creating some web UI and some CLI for this. So once his uh tweet had a lot of views he gave this LLM wiki.

**3:32** · So basically you can go through this LLM wiki. I will be adding it to my description and basically it's a template which you can just copy paste in your own agent. Say you have claude or you have codeex and you can just give it maybe GitHub profile. You can just give it it will read it and it will ask you questions about your knowledge base.

**3:54** · Basically it is just a basic template file. uh by reading it agent will understand what it has to do and what parathy has done and it will create a similar project structure based on your needs. So it is not a fixed uh template like this folder structure should be there. it has to create that much of MD files and all but it is just a template by reading this your LLM would understand that what it has to do and you have to give it some more data about

**4:20** · what kind of knowledge base you are building and based on that it will take decision what is exactly uh LLM wiki here is the core idea which Karpathi used stop retrieving data every time you build a persistent and standard wiki once and you keep it updated forever here as you can see he has taken A very beautiful uh thing which we have in software engineering is we will take the source code we'll compile it once and we

### WHAT IS AN LLM WIKI, EXACTLY?

**4:46** · will make a binary which will run every type right we will not do this process every time the same idea it has used here in LM wikis where we have raw source file right and LLM will compile it instead of us and it will create a wiki which is synthesized interlin and always ready for us and let's say we have new data we can use that data to ingest again and it will add a new connection, update new connections, delete the connection based on the contradictions and everything. It will do it itself. You don't have to do it.

**5:17** · He told in his wiki, if you read that wiki, it is a persistent compounding artifact. So, it will compound with every query you do, every uh raw artifact you add every day. You can tell it to ingest it. Every time you ingest something, it will compound. So, let's see the next section, which is the three layer architecture. Layer one will be your raw sources. This is your curated collection, your articles, your PDFs, your podcast notes, your images. These are the source of truth. Your LLM will only read it. It will never modify. This is immutable for your LLM.

### THE THREE-LAYER ARCHITECTURE

**5:49** · The next one is wiki. So, LLM will own this wiki entirely. You will rarely have to do anything yourself. It will create uh entity pages. It will create uh concept pages. It will create overview pages. It will create an index file, a log file.

**6:06** · It will create links. It will update them. It will maintain them. It will do everything. You have to rarely touch this. And the third layer is schema layer. It will be your plot.md file or any kind of agents MD file. Basically, it will have the rules, the convention, workflows and how to inest queries.

**6:24** · Basically, rules which will tell LLM how to behave. So, this will be mainly written by you or if you are using this wiki given by Andre Karpathi, it will create the wiki. So, you don't have to do it. Tarpati's own wiki reportedly grew around 100 articles and 400 keywords. This is fairly uh small knowledge base and it can handle it and it is all maintained automatically. This this layer is all maintained by the LLM itself. Arpati rarely touches. Let's move on to the three operation. So what action you have to do is you have to ingest your door data.

### THE THREE OPERATIONS

**6:55** · First you have to put all your curated corus into this raw folder. It will ingest files either one by one or together based on whatever needs you have. So basically you will drop the new source lm with read it summarizes it updates it and create 10 to 15 wiki pages and it will create wiki based on that. Okay. So this is wiki created based on your ingestion then you can query it.

**7:19** · Once you query something, LRM reads the Viki, synthesizes the answers and then you can feed that result into it back which will be added to your knowledge base and uh it will compound with every query you took.

**7:34** · Third thing you have to do is very essential which is a health check called as a linting operation. Basically it will check the whole health of your wiki. Find contradictions and orphans and stale data and links which are not even there and it will correct itself.

**7:49** · So it is very necessary process here because of the this process we are doing and it can contain hallucinations and it can ruin everything here. So linting is very necessary. Let's start with the demo. Here you can see I have two PDF files in my raw folder and I'm using claw. You can use any other agent and it will work with it. What I will be doing is I will be copying this whole So you can copy this and you can just paste it here.

### DEMO: BUILD YOUR OWN

**8:15** · So once it is pasted one more thing I want to do is I want to also paste a simple paragraph I have already written. Basically in this paragraph I am saying that I want plot to create this uh lines of wiki I pasted by Andre Karpati and help me set up this llm wiki in this directory and before it does it will ask me about what sources I plan to feed it and once I answer it will write me a clot.md schema file based on my answer. So let's uh hit enter.

**8:43** · It will process for some time and uh I will be back once it is done. It is asking me some questions. It is asking what is this wiki about and uh what sources do I plan to feed. Uh here is my answer. It's going to be a wiki about AI and the philosophy of software and uh I will feed it short essays and blog post from people like rich sutan and arpati pro probably 10 20 sources over time and uh

**9:11** · standard page types concept pages essay summaries uh I'm telling it what I am feeding and what this wiki will be all about. Let's see what it does. Uh make sure you put uh this uh accept edits on if you don't want to uh get interrupted again and again. It has stopped and it is asking me to start ingesting. Uh drop an essay into raw and say ingest file named. Okay. Uh let's see what it has done basically with that file. So with that file it read it understood almost everything. It understood llm concept.

**9:45** · Then it asked me some basic questions. I answered it and then it knows that we have to create a raw and it has written clot md based on my answer here as we told it to do. It has road plot and it has shown the whole structure. It has created blog, author's concept, essays.

**10:02** · I will say in justest it has given me summary about uh the PDF I gave. Uh it gave me the core thesis, the evidence, uh the second point and the concepts he will create the pages for the author, right? And it asks me anything I want him to emphasize, reframed or to be left

**10:20** · out. anything which I need it to not have in those wiki or it told me should he go ahead and write all this and I told him to go ahead of now and it is creating basically bunch of MDs now as you can see is updating the log file uh it is update the cloud file uh and uh with the sources in just one and wiki pages how much it has added so it is done with it what I want to show you is obsidian UI what Andre Karpati was

**10:49** · talking about this This is uh the obsidian UI Andre Karpati was talking about my all wiki pages are here and here in the graph view I can see connections between my MD files which is fully created by my ll MD and log MD files doesn't have any relation to anything because they are independent and other index file it has created which has connection to everything.

**11:12** · Let's ingest the next uh PDF. Even though I didn't give this folder, it knows that it has to be ingested by something in raw directory. The source folder or source of truth will be in my raw directory. So it has taken that as default found the file and it has given me some summary about it. Uh the core thesis the new concepts cross wiki connections between those previous PDF and current PDF and uh he's writing everything now. So once it is done with everything it will update the log file and everything.

**11:42** · We will see the updated graph view from obsidian and we will see the whole structure of picky. It is done with uh the processing. It has created a bunch of files. What it is showing it has updated clot md that is has ingested two sources and the number of wiki pages it created. It also added a log in the log file and it created bunch of MD file. Let's see the obsidian view. So you can see the view has been updated.

**12:09** · The index file has been updated. The claude and log file are still independent entities. And there is some connection between these two PDFs. There is some uh connection between the concepts they both have. I don't want to go deep into the connections as of what to just show you what it can do. I have a question I wanted to answer based on the knowledge gathered. How do Saturn and Karpati agree about the future of software and where might they agree? So if you see this question this needs synthesis of both the PDFs.

**12:38** · So it should know about both the PDFs should have some connection between them and it will be able to get it because it has created the whole bunch of connections between both the knowledge sources. You can see bunch of uh links between them. So let's see what it answers. Uh it has replied me back. As you can see, it is reading the relevant wiki pages to ground the answers and uh it has given me where they agree and where they disagree. If you want, you can go deep into this answers and everything. But it is just a demo.

**13:10** · Uh you can have it for anything, any knowledge base you can create. But uh make sure that the number of pages are of small scale like 100 pages, 200 pages. Use it for your own deep research instead of uh general research. Uh let's go to the next section. Uh this is our next section which is rag versus LLM the real comparison. I will go through the most basic thing here. I won't bore you going through all of this. You can read it yourself by pausing it if you want.

### RAG vs LLM WIKI: THE REAL COMPARISON

**13:37** · But the main thing is neither of them wins. They solve a completely different problem. Basically you will use rag when you have millions of documents and that will change constantly. You need a precise citations to an exact chunk.

**13:52** · Think customer support maybe legal search maybe enterprise fact look LLM wiki here is great when you have bounded curated corpus maybe few hundred sources of uh static knowledge and research papers articles books you are reading courses you are studying your own journal so here where synthesis matter more than retrieval you will use this LLM wicki if your retrieval is more priority than your synthesis you will use rack if you're looking for less tokens This is basically a better option.

**14:23** · But currently everyone has some tokens and uh can use them for knowledge base you can use this. Okay. And if you have less curated sources like you can use this. If you have large sources this guy will fail. So it is better for large data and it is better for small data.

**14:40** · One more thing I want to discuss is LLM can hallucinate. When you are using your query results as the data ingest to make your knowledge more compounding, hallucination can get baked into facts, it can ruin the whole wiki. Uh for that we have lints. Linds will be very helpful there. Hallucinations here will be only local to answer and here it can ruin everything if you don't lint it regularly. Okay. Here fresh data is always reread. If you want to do update new data, you will have to reingest or you have to ingest the updated data.

**15:14** · Okay, let's move on to the next section which is why it matters. It is uh really not about wikis. It is more about a deeper shift. Karpathi is pointing something whenever Bush described in 1945 as MMEX which is your memory extender. The idea was a personal curated knowledge store where connection between documents are as valuable as the document itself. Uh Karpati has made something similar.

### WHY THIS MATTERS

**15:41** · Previously we had some concerns because of that we cannot make it which is people don't want to uh do all these things like bookkeeping, updating your cross references and they don't want to be get buried into all these hassle. That's why this meme X was not created. Now we have LLM to do this.

**16:04** · They won't get bored. They can not forget any cross reference. They can work on 15 files at a time. Uh we have a capability of doing that. So uh why don't uh we do this now. So the tedious part which was uh handling on hassle of all these things are solved now. So we can completely focus on thinking instead of filing. uh we can focus on the knowledge store.

**16:28** · We can build our second brain because LLM will be bookkeeping it and we will be compounding it every time we ask a query or reingesting some data asking it the relevant articles which we can add as a next contender we can do that and it can use web to lint and everything. If you want to try it yourself, links to Andre Karpati's original gist, his tweets are there in the description. You can follow him.

### Outro

**16:55** · He is super dope and every day he gives something new to the community basically. And you can comment what would you build a personal wiki for. I'm very curious what people will actually create this personal knowledge for. So you can help me. If this explanation helped, a like and subscribe will genuinely help this channel. Uh see you in the next video. Happy coding.