# Build Your Agents 101

Welcome to **Build Your Agents 101** - a hands-on tutorial series where you'll learn to build AI agents from scratch!

## What You'll Learn

This tutorial takes you through building a complete SQL query agent that converts natural language questions into database queries. Along the way, you'll master:

- **ReAct Pattern** - The reasoning and acting loop that powers modern agents
- **Function Calling** - How LLMs interact with external tools
- **Security** - Building safe agents that can't be exploited
- **Practical Skills** - Real-world agent development patterns

## The Project

We'll build a **Natural Language SQL Agent** for a bookstore database:

```
User: "Who are my top 5 customers by revenue?"
Agent: Generates SQL → Executes → Returns formatted answer
```

## Tutorial Stages

### [Stage 1: Database Setup](tutorial/stage1-database.md)
Create a SQLite database with sample data. Learn schema design and relationships.

**Time:** 30 minutes | **Difficulty:** Beginner

### [Stage 2: Basic Agent](tutorial/stage2-basic-agent.md)
Build your first agent from scratch using OpenAI's API. Understand the ReAct loop.

**Time:** 1-2 hours | **Difficulty:** Intermediate

### [Stage 3: LangChain Version](tutorial/stage3-langchain.md)
Rebuild using LangChain to understand what frameworks provide.

**Time:** 1 hour | **Difficulty:** Intermediate

### [Stage 4: Custom Tools](tutorial/stage4-custom-tools.md)
Extend LangChain agents with custom tools beyond built-in capabilities.

**Time:** 45-60 minutes | **Difficulty:** Intermediate-Advanced

## Prerequisites

- Python 3.8+
- Basic SQL knowledge
- Familiarity with APIs
- OpenAI API key (or use Ollama for free local models)

## Why Build Agents?

Agents are the future of AI applications. Unlike simple chatbots, agents can:

- Break down complex tasks
- Use tools to interact with external systems
- Reason through multi-step problems
- Make decisions autonomously

By building one from scratch, you'll understand exactly how they work - no magic, just clear patterns.

## Ready to Start?

Jump into [Stage 1: Database Setup](tutorial/stage1-database.md) and let's build something real!

---

**Questions?** Open an issue on [GitHub](https://github.com/chidamnat/buildAgents)