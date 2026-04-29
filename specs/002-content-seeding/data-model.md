# Data Model: Phase 2 — Course Content Seeding

**Branch**: `002-content-seeding` | **Date**: 2026-04-28

Schema is defined in Phase 1. This document records the exact values being seeded.

---

## Chapter Seed Data

| id | title | tier | order_num | description (2 sentences) |
|----|-------|------|-----------|--------------------------|
| 1 | Introduction to AI Agents | free | 1 | Learn what AI agents are and how they autonomously perceive, reason, and act. Covers the core components: LLM reasoning engine, tools, memory, and the agent loop. |
| 2 | OpenAI Agents SDK | free | 2 | Build production agents using OpenAI's official SDK with Agents, Handoffs, and Guardrails. Covers the Runner execution model and streaming responses. |
| 3 | Anthropic Claude Agent SDK | free | 3 | Create powerful agents using Anthropic's Claude models and the Claude Agent SDK. Covers tool use, multi-turn conversations, and safety best practices. |
| 4 | MCP Fundamentals | premium | 4 | Understand the Model Context Protocol — the open standard for connecting agents to tools. Covers the client-server architecture, Resources, Prompts, and Tools primitives. |
| 5 | Advanced MCP Server Development | premium | 5 | Build production-grade MCP servers that expose tools and resources to AI agents. Covers transport layers, error handling, and real-world server patterns. |
| 6 | Agent Skills & MCP Code Execution | premium | 6 | Learn how agents acquire and execute skills through MCP, including sandboxed code execution. Covers the skill registry pattern and safe execution environments. |
| 7 | FastAPI for Agents | premium | 7 | Build agent-facing APIs using FastAPI with async endpoints, dependency injection, and OpenAPI specs. Covers deploying agent backends to production. |
| 8 | Vector Databases & RAG | pro | 8 | Enable agents to retrieve relevant knowledge using vector databases and RAG pipelines. Covers embeddings, similarity search, and integrating retrieval into agent workflows. |
| 9 | Multi-Agent Reliability | pro | 9 | Design reliable multi-agent systems with proper error handling, retries, and observability. Covers agent orchestration patterns and failure recovery strategies. |
| 10 | Evals — Measuring Agent Performance | pro | 10 | Measure and improve agent quality using systematic evaluation frameworks. Covers eval metrics, test datasets, and continuous improvement pipelines. |

---

## Quiz Question Structure (per chapter)

Each chapter has 5 questions. Each question must cover a distinct concept from the chapter.
Questions are ordered 1–5 by `order_num`.

### Question quality rules:
- Each question tests a specific, unambiguous fact from the chapter content
- Distractors (wrong answers) are plausible but clearly incorrect on reflection
- Explanation (shown after submit) references the chapter concept directly
- No two questions in the same chapter test the same concept
