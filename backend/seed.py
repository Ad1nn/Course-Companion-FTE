"""
Phase 2 — Course Content Seeding
Seeds 10 chapters and 50 quiz questions into Supabase.
Safe to re-run (upsert on id / chapter_id+order_num).

Usage:
    cd backend
    python3 seed.py
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

# ── Chapter content ───────────────────────────────────────────────────────────

CHAPTERS = [
    {
        "id": 1,
        "title": "Introduction to AI Agents",
        "description": "Learn what AI agents are and how they autonomously perceive, reason, and act. Covers the core components: LLM reasoning engine, tools, memory, and the agent loop.",
        "content": """An AI agent is a software system that can perceive its environment, reason about what to do, take actions, and learn from feedback — all autonomously, without requiring a human to direct each step. Unlike a simple chatbot that only responds to messages, an agent pursues goals by deciding on a sequence of actions and executing them over time.

**The Core Components of an AI Agent**

Every AI agent is built from four fundamental components:

1. **LLM Reasoning Engine** — The large language model (LLM) is the brain of the agent. It reads the current state, decides what to do next, and produces either a final answer or a tool call. Modern agents use models like GPT-4, Claude, or Gemini as their reasoning core.

2. **Tools** — Tools are functions the agent can call to interact with the world. A tool might search the web, execute code, read a file, query a database, or call an external API. The agent decides which tools to use and in what order based on its goal.

3. **Memory** — Agents need memory to function over time. Short-term memory holds the current conversation and recent observations. Long-term memory stores facts, past experiences, and learned preferences, often in a vector database so relevant memories can be retrieved when needed.

4. **The Agent Loop** — The agent loop is the cycle that drives autonomous behavior: Perceive → Reason → Act → Observe. The agent perceives its current state, reasons about what to do, takes an action (like calling a tool), observes the result, and repeats until the goal is achieved or it determines it cannot proceed.

**Why Agents Matter**

Traditional software is deterministic: given input X, it always produces output Y via a fixed sequence of steps written by a programmer. Agents are different — they decide their own steps based on the goal and the current context. This makes them capable of handling tasks that are too complex or too variable to program explicitly.

Consider a research agent: given a question like "What are the latest advances in protein folding?", it autonomously searches the web, reads papers, synthesizes findings, and writes a report — adapting its plan as it discovers new information. No programmer scripted those exact steps.

**Agents vs Chatbots**

A chatbot responds to each message independently, with no persistent goal or ability to take real-world actions. An agent has a goal it actively pursues, can take actions that affect the world (not just produce text), and maintains context across many steps. The key distinction is autonomy and action.

**Real-World Agent Use Cases**

AI agents are being deployed across many domains:
- **Coding agents** (GitHub Copilot, Devin) write, test, and debug code autonomously
- **Research agents** browse the web, read papers, and synthesize knowledge
- **Customer support agents** look up accounts, process refunds, and escalate issues
- **Data analysis agents** query databases, generate charts, and write reports
- **Personal assistant agents** manage calendars, draft emails, and book meetings

**The Agentic AI Stack**

Building production agents requires more than just an LLM. The complete stack includes:
- A capable LLM (reasoning layer)
- Tool integrations (action layer)
- Memory systems (context layer)
- An orchestration framework (coordination layer)
- Observability and eval (reliability layer)

This course will take you through each layer of the stack, from basic agent construction to production-grade multi-agent systems with evaluation pipelines.
""",
        "order_num": 1,
        "tier": "free",
    },
    {
        "id": 2,
        "title": "OpenAI Agents SDK",
        "description": "Build production agents using OpenAI's official SDK with Agents, Handoffs, and Guardrails. Covers the Runner execution model and streaming responses.",
        "content": """The OpenAI Agents SDK is an official Python library from OpenAI for building production-grade agentic applications. Released in 2024, it provides high-level primitives that handle the agent loop, tool calling, multi-agent coordination, and safety checks — so you can focus on defining agent behavior rather than managing infrastructure.

**Core Primitives**

The SDK is built around four main concepts:

**1. Agent**
An Agent combines an LLM model, a system prompt (called instructions), and a list of tools. You define what the agent knows how to do and how it should behave, and the SDK handles running it.

```python
from agents import Agent, Runner

agent = Agent(
    name="Research Assistant",
    instructions="You are a helpful research assistant. Search the web for accurate information.",
    tools=[web_search, read_file],
    model="gpt-4o"
)
```

**2. Runner**
The Runner executes the agent loop. You call `Runner.run()` with the agent and an initial message, and it handles all the back-and-forth: sending messages to the model, calling tools when requested, passing tool results back, and repeating until the agent produces a final response.

```python
result = await Runner.run(agent, "What are the best Python libraries for data visualization?")
print(result.final_output)
```

**3. Handoffs**
Handoffs allow one agent to transfer control to another. This enables multi-agent architectures where a coordinator agent routes tasks to specialist agents. For example, a customer support agent might hand off billing questions to a billing specialist agent.

```python
billing_agent = Agent(name="Billing Specialist", instructions="Handle all billing queries.")
support_agent = Agent(
    name="Support",
    instructions="Route billing questions to the billing specialist.",
    handoffs=[billing_agent]
)
```

**4. Guardrails**
Guardrails are safety checks that run on inputs or outputs before they reach the model or the user. They can block inappropriate content, enforce formatting requirements, or validate business rules. Input guardrails run before the agent processes a message; output guardrails run before the response is returned.

**Streaming**

The SDK supports streaming responses so you can display output to users as it is generated rather than waiting for the full response:

```python
async for event in Runner.run_streamed(agent, "Explain quantum computing"):
    if event.type == "text_delta":
        print(event.delta, end="", flush=True)
```

**Tracing and Debugging**

The SDK includes built-in tracing that records every step the agent takes: each LLM call, tool call, tool result, and handoff. This makes debugging much easier — you can see exactly why the agent made each decision and where it went wrong.

**Tool Definition**

Tools are Python functions decorated with `@tool`. The SDK automatically generates the JSON schema for the tool from the function signature and docstring, which it sends to the model so the model knows when and how to call the tool.

```python
from agents import tool

@tool
def get_weather(city: str) -> str:
    '''Get the current weather for a city.'''
    return f"The weather in {city} is sunny, 22°C."
```

**Why Use the OpenAI Agents SDK?**

Compared to building agent loops from scratch, the SDK saves significant development time. It handles token counting, tool call formatting, error recovery, and the multi-turn conversation structure automatically. For teams building on OpenAI models, it is the recommended starting point for agentic applications.
""",
        "order_num": 2,
        "tier": "free",
    },
    {
        "id": 3,
        "title": "Anthropic Claude Agent SDK",
        "description": "Create powerful agents using Anthropic's Claude models and the Claude Agent SDK. Covers tool use, multi-turn conversations, and safety best practices.",
        "content": """Anthropic's Claude is a family of large language models designed with safety and helpfulness as core principles. Claude models — including Claude 3.5 Sonnet, Claude 3 Opus, and Claude 3 Haiku — are among the most capable models available for agentic tasks, with strong performance on reasoning, coding, and tool use.

**The Anthropic Python SDK**

The `anthropic` Python package provides the primary interface for building Claude-powered agents. You send messages and receive responses, including tool use blocks when Claude decides to call a tool.

```python
import anthropic

client = anthropic.Anthropic()
```

**Tool Use with Claude**

Claude uses a structured tool-use protocol. You define tools as JSON schemas and pass them to the API. When Claude decides to use a tool, it returns a `tool_use` content block instead of text. You execute the tool, return the result as a `tool_result` block, and Claude continues reasoning.

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in London?"}]
)
```

**Multi-Turn Tool Calling**

Building an agent with Claude requires implementing the tool-calling loop manually (or using the Claude Agent SDK). The loop continues until Claude returns a final text response with no tool calls:

1. Send user message + tool definitions to Claude
2. If response contains `tool_use` blocks, execute each tool
3. Append tool results as `tool_result` blocks
4. Send updated conversation back to Claude
5. Repeat until Claude returns pure text

**The Claude Agent SDK**

Anthropic's Claude Agent SDK (built on top of the raw API) provides higher-level abstractions similar to the OpenAI Agents SDK: Agent objects, a Runner, tool decorators, and multi-agent coordination. It handles the tool loop automatically so you can focus on agent behavior.

**System Prompts for Agent Behavior**

The system prompt is where you define the agent's identity, capabilities, and constraints. A well-crafted system prompt dramatically improves agent reliability. For a customer support agent, you might specify: the company name, what the agent can and cannot do, how to handle edge cases, and the tone to use.

**Safety and Constitutional AI**

Claude is trained using Constitutional AI (CAI) — a technique where the model learns to evaluate its own outputs against a set of principles. This gives Claude built-in refusal training for harmful requests and a strong tendency toward honest, helpful responses. For agent builders, this means Claude is less likely to take harmful actions even when not explicitly constrained.

**Computer Use**

Claude 3.5 Sonnet supports computer use — the ability to control a computer GUI by taking screenshots and issuing keyboard/mouse commands. This enables agents that can operate desktop applications, fill out web forms, and automate browser-based workflows without requiring custom tool integrations.

**Comparing Claude and GPT for Agents**

Both are excellent for agentic tasks. Claude tends to excel at longer-context reasoning, careful instruction following, and safety-critical applications. GPT-4o has strong function-calling performance and a mature ecosystem. The best choice depends on your specific use case, latency requirements, and cost budget.
""",
        "order_num": 3,
        "tier": "free",
    },
    {
        "id": 4,
        "title": "MCP Fundamentals",
        "description": "Understand the Model Context Protocol — the open standard for connecting agents to tools. Covers the client-server architecture, Resources, Prompts, and Tools primitives.",
        "content": """The Model Context Protocol (MCP) is an open standard developed by Anthropic for connecting AI agents and LLM applications to external tools, data sources, and services. Released in November 2024, MCP has rapidly become the de-facto standard for agent-tool integration, with support from major AI providers including Anthropic, OpenAI, Google, and Microsoft.

**Why MCP Exists**

Before MCP, every AI application had to build its own integrations for every tool it needed: custom code for web search, file reading, database access, API calls, and more. This created a fragmented ecosystem where integrations were not reusable and every tool provider had to build separate connectors for every AI platform.

MCP solves this by defining a standard protocol. A tool provider builds one MCP server, and any MCP-compatible AI application can use it immediately — no custom integration required.

**The Client-Server Architecture**

MCP uses a client-server model:

- **MCP Server**: Exposes tools, resources, and prompts. A server might provide web search, file system access, a database connection, or any other capability. MCP servers are typically small, focused services.
- **MCP Client**: The AI application (agent) that connects to MCP servers and uses their capabilities. The client handles the agent logic; the server handles tool execution.
- **MCP Host**: The application environment that manages client connections (e.g., Claude Desktop, an IDE extension, or a custom agent framework).

**The Three MCP Primitives**

MCP exposes capabilities through three standardised primitives:

**1. Tools**
Tools are functions the agent can call to take actions. They are the most commonly used primitive. Examples: `search_web(query)`, `execute_code(code)`, `send_email(to, subject, body)`. Tools have a name, description, and JSON schema for their inputs.

**2. Resources**
Resources are read-only data sources the agent can access. Unlike tools (which perform actions), resources expose data. Examples: a file's contents, a database table, a git repository's history, a calendar's events. Resources have URIs like `file:///path/to/file` or `db://mydb/users`.

**3. Prompts**
Prompts are reusable prompt templates that the MCP server exposes. They allow server operators to define structured workflows or conversation starters. For example, a code review server might expose a "review_pr" prompt template that guides the agent through a structured code review process.

**Transport Layers**

MCP supports two transport mechanisms:

- **stdio** (standard input/output): Used for local MCP servers running as child processes. The client launches the server process and communicates via stdin/stdout. Fast and simple for local tools.
- **SSE** (Server-Sent Events over HTTP): Used for remote MCP servers deployed as web services. Enables connecting to tools hosted in the cloud.

**MCP vs Function Calling**

Both MCP and function calling allow agents to use tools. The key difference is standardisation. Function calling is model-specific — each provider (OpenAI, Anthropic, Google) has its own schema and protocol. MCP is model-agnostic: the same MCP server works with any MCP-compatible client, regardless of which LLM powers it.

**Official SDKs**

Anthropic provides official MCP SDKs for Python and TypeScript:

```bash
pip install mcp          # Python SDK
npm install @modelcontextprotocol/sdk  # TypeScript SDK
```

These SDKs handle the protocol details so you can focus on implementing your tools.

**Real-World MCP Servers**

The MCP ecosystem already includes servers for: web search (Brave, Tavily), file systems, GitHub, Slack, Notion, PostgreSQL, SQLite, web browsers, code execution, and many more. You can find the full list at modelcontextprotocol.io.
""",
        "order_num": 4,
        "tier": "premium",
    },
    {
        "id": 5,
        "title": "Advanced MCP Server Development",
        "description": "Build production-grade MCP servers that expose tools and resources to AI agents. Covers transport layers, error handling, and real-world server patterns.",
        "content": """Building an MCP server means creating a service that exposes tools, resources, or prompts to any MCP-compatible AI agent. This chapter covers building production-quality MCP servers using the official Python SDK.

**Setting Up an MCP Server**

The Python MCP SDK provides a `Server` class that manages the protocol. You define your tools, resources, and prompts, then run the server on your chosen transport.

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("my-tool-server")
```

**Implementing Tool Handlers**

Tools are the most common MCP primitive. You register a tool handler that receives tool call requests and returns results:

```python
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="calculate",
            description="Perform arithmetic calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate"}
                },
                "required": ["expression"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "calculate":
        try:
            result = eval(arguments["expression"])  # simplified example
            return [types.TextContent(type="text", text=str(result))]
        except Exception as e:
            raise ValueError(f"Calculation failed: {e}")
    raise ValueError(f"Unknown tool: {name}")
```

**Error Handling**

Production MCP servers must handle errors gracefully. Tool handlers should raise exceptions with descriptive messages — the SDK converts these into structured error responses that the client can interpret. Never return raw stack traces.

**Implementing Resource Endpoints**

Resources expose data rather than performing actions. Register resource handlers with URIs:

```python
@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="file:///data/config.json",
            name="Configuration",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "file:///data/config.json":
        return open("data/config.json").read()
    raise ValueError(f"Unknown resource: {uri}")
```

**Running on stdio Transport**

For local servers (launched as a subprocess by the client):

```python
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

import asyncio
asyncio.run(main())
```

**Running on SSE Transport**

For remote servers deployed as web services, use the SSE transport with a web framework like Starlette or FastAPI. This allows the server to be deployed to the cloud and accessed by any MCP client over HTTP.

**Authentication for Remote Servers**

Remote MCP servers should authenticate clients. The recommended patterns are:
- **API keys** in request headers: `Authorization: Bearer <api-key>`
- **OAuth2** for user-delegated access (e.g., accessing a user's Google Drive)

Validate credentials before processing any tool or resource request.

**Testing MCP Servers**

Use the MCP Inspector — a browser-based debugging tool from Anthropic — to test your server interactively. Point it at your server's stdio command or SSE endpoint and you can call tools, browse resources, and inspect all messages in real time.

```bash
npx @modelcontextprotocol/inspector python3 my_server.py
```

**Deployment Patterns**

- **Local server**: Distributed as a Python package, run via `uvx` or `pip install`
- **Docker container**: Containerise for consistent deployment on any host
- **Cloud service**: Deploy on Railway, Render, or Fly.io as an SSE endpoint

**Performance Considerations**

MCP servers should be fast — agents wait for tool results before continuing. For slow operations (database queries, external API calls), use async handlers and implement timeouts. Return partial results early if possible.
""",
        "order_num": 5,
        "tier": "premium",
    },
    {
        "id": 6,
        "title": "Agent Skills & MCP Code Execution",
        "description": "Learn how agents acquire and execute skills through MCP, including sandboxed code execution. Covers the skill registry pattern and safe execution environments.",
        "content": """Agent skills are reusable, registered capabilities that agents can invoke to accomplish specific tasks. Rather than solving every problem from scratch, a skilled agent draws on a library of proven capabilities — searching the web, executing code, querying databases, sending notifications, and more. This chapter covers the skill architecture and the critical topic of safe code execution.

**What is an Agent Skill?**

A skill is a named, well-defined capability with a clear interface (inputs and outputs). Skills differ from raw tools in that they are higher-level — a single skill might coordinate multiple tool calls to accomplish a goal. For example, a "research topic" skill might: search the web, read top results, and synthesise a summary — all as one composable unit.

**The Skill Registry Pattern**

A skill registry is a centralised catalogue of available skills that agents can discover and invoke. Skills are registered with their names, descriptions, input schemas, and handler functions. At runtime, an agent queries the registry to see what skills are available and selects appropriate ones for its current task.

In MCP, the skill registry is implemented as an MCP server — skills are exposed as MCP tools. This makes skills instantly available to any MCP-compatible agent.

**Code Execution as a Skill**

Code execution is one of the most powerful agent skills. An agent that can write and run code can solve a vast range of problems: data analysis, automation, testing, mathematical computation, file manipulation, and more.

However, executing agent-generated code on a host machine is extremely dangerous. Malicious or buggy code can delete files, exfiltrate data, consume system resources, or crash the host. **Sandboxing is non-negotiable for production code execution.**

**E2B Cloud Sandboxes**

E2B (e2b.dev) provides cloud-based micro virtual machines specifically designed for AI code execution. Each sandbox is an isolated Linux environment with:
- A full Python/Node.js runtime
- Pre-installed libraries
- Network access (configurable)
- Automatic cleanup after use

```python
from e2b_code_interpreter import Sandbox

sandbox = Sandbox()
execution = sandbox.run_code("import pandas as pd; df = pd.DataFrame({'x': [1,2,3]}); print(df)")
print(execution.text)
sandbox.close()
```

E2B sandboxes start in under a second, support file uploads/downloads, and handle timeout enforcement automatically.

**Docker-Based Execution**

For self-hosted code execution, Docker containers provide isolation. Each code execution runs in a fresh container with limited resources:

```python
import docker

client = docker.from_env()
result = client.containers.run(
    "python:3.11-slim",
    f'python3 -c "{code}"',
    mem_limit="128m",
    cpu_quota=50000,
    network_mode="none",  # no network access
    remove=True,
    timeout=30
)
```

Key security settings: `network_mode="none"` (no outbound connections), `mem_limit` (prevents memory exhaustion), `cpu_quota` (prevents CPU monopolisation), `remove=True` (cleanup after execution).

**Skill Chaining**

Complex agent tasks are accomplished by chaining skills: the output of one skill becomes the input for the next. For example: `search_web(query)` → `read_url(top_result)` → `extract_data(page_content)` → `execute_code(analysis_script)` → `format_report(results)`.

Skill chains can be defined as workflows (fixed sequences) or discovered dynamically by the agent (where the agent decides which skill to call next based on intermediate results).

**Stateful vs Stateless Skills**

Stateless skills are idempotent — calling them with the same inputs always produces the same output with no side effects. Stateful skills maintain state across calls (e.g., a database connection, a browser session, a running sandbox). Prefer stateless skills where possible; carefully manage lifecycle for stateful ones.

**Security Considerations**

Beyond sandboxing, apply these principles:
- **Principle of least privilege**: Skills only have access to what they need
- **Input validation**: Validate and sanitise all agent-provided inputs before execution
- **Output filtering**: Scan outputs for sensitive data before returning to the agent
- **Audit logging**: Log all skill invocations with inputs and outputs for review
- **Rate limiting**: Prevent agents from calling expensive skills in tight loops
""",
        "order_num": 6,
        "tier": "premium",
    },
    {
        "id": 7,
        "title": "FastAPI for Agents",
        "description": "Build agent-facing APIs using FastAPI with async endpoints, dependency injection, and OpenAPI specs. Covers deploying agent backends to production.",
        "content": """FastAPI is the leading Python web framework for building agent backends. Its combination of async support, automatic OpenAPI documentation, Pydantic validation, and performance makes it ideal for APIs that serve AI agents. This course's Phase 1 backend is built with FastAPI — this chapter explains why and how to use it effectively for agentic applications.

**Why FastAPI for Agent Backends?**

AI agents make many parallel API calls and require fast, reliable backends. FastAPI's async-first design means your server handles concurrent requests efficiently without blocking. Other key advantages:

- **Automatic OpenAPI/Swagger docs** — FastAPI generates interactive API documentation from your route definitions. This is what the ChatGPT App's OpenAPI spec is based on.
- **Pydantic validation** — Request and response bodies are automatically validated and serialised using Pydantic models. No manual validation code.
- **Type annotations** — FastAPI uses Python type hints to derive request schemas, response models, and parameter types. Your code is self-documenting.
- **Dependency injection** — FastAPI's `Depends()` system enables clean separation of authentication, database connections, and other shared resources.

**Async Endpoints**

Agent APIs should use async handlers to handle many concurrent requests efficiently:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: int):
    # async DB call — doesn't block the event loop
    result = await db.fetch_chapter(chapter_id)
    return result
```

**Dependency Injection**

FastAPI's `Depends()` system keeps route handlers clean. Authentication, database sessions, and configuration are injected rather than repeated:

```python
from fastapi import Depends, HTTPException

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    return {"email": user.email, "tier": user.tier}
```

**Pydantic Models**

Define request/response shapes with Pydantic. FastAPI automatically validates incoming data and serialises responses:

```python
from pydantic import BaseModel

class ChapterResponse(BaseModel):
    id: int
    title: str
    content: str
    tier: str

@app.get("/chapters/{id}", response_model=ChapterResponse)
async def get_chapter(id: int):
    return await fetch_chapter(id)  # FastAPI validates the return value
```

**Streaming Agent Responses**

For long-running agent operations, stream results back to the client rather than waiting for completion:

```python
from fastapi.responses import StreamingResponse

@app.post("/agent/run")
async def run_agent(query: str):
    async def generate():
        async for chunk in agent.run_streamed(query):
            yield f"data: {chunk}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**WebSocket for Real-Time Agent Communication**

WebSockets enable bidirectional communication, useful for interactive agent sessions where the client needs to send follow-up messages while the agent is running:

```python
@app.websocket("/agent/session")
async def agent_session(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for chunk in agent.run_streamed(message):
            await websocket.send_text(chunk)
```

**Deploying to Railway**

Railway is the recommended deployment platform for FastAPI agent backends:

1. Connect your GitHub repository to Railway
2. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables (Supabase keys, API keys)
4. Railway automatically deploys on every push to main

Railway provides zero-downtime deployments, automatic HTTPS, and scales horizontally when needed.

**Performance Best Practices**

- Use `async` for all I/O operations (database, external APIs)
- Return only the fields clients need (avoid over-fetching)
- Add database connection pooling for high-traffic endpoints
- Use FastAPI's background tasks for non-critical work that doesn't need to block the response
""",
        "order_num": 7,
        "tier": "premium",
    },
    {
        "id": 8,
        "title": "Vector Databases & RAG",
        "description": "Enable agents to retrieve relevant knowledge using vector databases and RAG pipelines. Covers embeddings, similarity search, and integrating retrieval into agent workflows.",
        "content": """Vector databases and Retrieval-Augmented Generation (RAG) are the foundation of knowledge-aware AI agents. Instead of relying solely on what was baked into the model during training, RAG-enabled agents can retrieve relevant, up-to-date information at runtime and use it to answer questions accurately.

**What is a Vector Embedding?**

A vector embedding is a numerical representation of text (or images, audio, etc.) that captures semantic meaning. Texts with similar meanings have embeddings that are close together in vector space, regardless of the exact words used. "dog" and "canine" will have similar embeddings; "dog" and "quantum physics" will be far apart.

Embeddings are generated by embedding models like OpenAI's `text-embedding-3-small` or Anthropic's embedding API. A typical embedding is a list of 1,536 floats (for OpenAI's model) that encodes the semantic content of the text.

**What is a Vector Database?**

A vector database stores embeddings and enables fast similarity search — finding the embeddings closest to a query embedding. Unlike traditional databases that match exact values, vector databases match by semantic similarity.

Popular vector databases:
- **Pinecone** — managed cloud service, easy to get started
- **Weaviate** — open-source, supports hybrid search
- **Qdrant** — open-source, high performance
- **pgvector** — PostgreSQL extension, works with Supabase
- **Chroma** — local-first, great for development

**What is RAG?**

Retrieval-Augmented Generation (RAG) is a pattern where relevant documents are retrieved from a knowledge base and included in the LLM's context before it generates a response. This allows the model to answer questions about documents it wasn't trained on.

The RAG pipeline has three stages:
1. **Indexing**: Chunk documents, generate embeddings, store in vector DB
2. **Retrieval**: Embed the user's query, find similar chunks in the vector DB
3. **Generation**: Include retrieved chunks in the LLM prompt, generate answer

**Chunking Strategies**

Documents must be split into chunks before embedding. Chunk size matters:
- **Too small**: Chunks lack context and miss meaning
- **Too large**: Chunks exceed context windows and dilute relevance

Common strategies:
- **Fixed-size chunking**: Split every N tokens (simple, but may break sentences)
- **Sentence chunking**: Split on sentence boundaries (better semantic units)
- **Semantic chunking**: Split when semantic similarity drops (most accurate, slower)
- **Recursive character splitting**: Split by paragraphs → sentences → words (LangChain default)

**Similarity Search**

The most common similarity metric is **cosine similarity**, which measures the angle between two vectors (1.0 = identical direction, 0.0 = perpendicular). Dot product similarity is also common and faster when vectors are normalised.

**Hybrid Search**

Hybrid search combines vector similarity search with traditional keyword (BM25) search. This handles cases where exact keyword matches matter (product codes, names, IDs) that pure semantic search might miss. Most production RAG systems use hybrid search.

**Integrating RAG into Agent Workflows**

An agent with RAG capability has a retrieval tool it can call when it needs information from its knowledge base:

```python
@tool
async def search_knowledge_base(query: str, top_k: int = 5) -> str:
    query_embedding = await embed(query)
    results = await vector_db.similarity_search(query_embedding, top_k=top_k)
    return "\n\n".join([r.content for r in results])
```

The agent decides when to call this tool based on its current goal and what information it needs.

**Evaluating Retrieval Quality**

Poor retrieval leads to poor answers. Key metrics:
- **Recall@K**: Are the relevant documents in the top K results?
- **Precision@K**: Are the top K results all relevant?
- **Faithfulness**: Does the generated answer stick to the retrieved context?
- **Answer relevance**: Does the answer address the original question?

RAGAS is a popular framework for automated RAG evaluation using these metrics.
""",
        "order_num": 8,
        "tier": "pro",
    },
    {
        "id": 9,
        "title": "Multi-Agent Reliability",
        "description": "Design reliable multi-agent systems with proper error handling, retries, and observability. Covers agent orchestration patterns and failure recovery strategies.",
        "content": """As agent systems grow in complexity — with multiple agents collaborating, tools being called in parallel, and tasks spanning long time horizons — reliability becomes critical. A single agent that occasionally fails is manageable; a multi-agent system with poor error handling can fail catastrophically, wasting time, money, and user trust. This chapter covers the patterns and practices for building reliable multi-agent systems.

**Orchestrator-Worker Pattern**

The most common multi-agent architecture is the orchestrator-worker pattern:

- **Orchestrator**: A coordinator agent that receives the high-level goal, breaks it into subtasks, delegates to worker agents, and assembles the final result.
- **Workers**: Specialist agents that handle specific subtasks (research, coding, writing, data analysis). Each worker is optimised for its domain.

This pattern enables parallelism (multiple workers run simultaneously), specialisation (workers can use the best model for their task), and fault isolation (one worker failing doesn't necessarily fail the whole system).

**Circuit Breaker Pattern**

A circuit breaker prevents cascading failures by stopping calls to a service that is repeatedly failing. The circuit has three states:

- **Closed** (normal): Requests flow through; failures are counted
- **Open** (failing): After N failures, stop sending requests; return errors immediately
- **Half-open** (testing): After a timeout, send one test request; if it succeeds, close the circuit

For agents, circuit breakers protect against: failing external APIs, overloaded tool servers, or misbehaving sub-agents.

**Retry Strategies**

Not all failures are permanent. Network glitches, rate limits, and temporary service outages often resolve quickly. Implement retries with exponential backoff:

```python
import asyncio

async def retry_with_backoff(fn, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return await fn()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

Use jitter (random variation in delay) to prevent thundering herd problems when many agents retry simultaneously.

**Idempotency in Agent Actions**

Agent actions should be idempotent where possible — calling the same action multiple times produces the same result with no unintended side effects. This is especially important for actions like sending emails, creating database records, or making financial transactions. Use idempotency keys to prevent duplicate operations:

```python
async def create_order(order_id: str, items: list):
    # Check if order already exists
    if await order_exists(order_id):
        return await get_order(order_id)
    return await insert_order(order_id, items)
```

**Distributed Tracing**

In a multi-agent system, understanding what happened requires tracing the flow across multiple agents and tools. Distributed tracing captures the full execution tree: which agent called which tool, how long each step took, and where errors occurred.

Tools like OpenTelemetry, Langfuse, and Arize AI provide tracing for agent systems. At minimum, log:
- Agent ID and run ID
- Tool calls with inputs and outputs
- Handoffs between agents
- Errors and retries
- Total duration and token usage

**Failure Isolation**

Design multi-agent systems so that one agent's failure does not cascade to others:
- **Timeouts**: Every agent call has a maximum duration; return an error if exceeded
- **Bounded retries**: Don't retry indefinitely; fail fast after a reasonable limit
- **Fallback responses**: When a worker fails, the orchestrator uses a default response rather than propagating the failure
- **Dead letter queues**: Failed tasks are moved to a queue for human review rather than being lost

**State Management**

Long-running multi-agent tasks need persistent state so they can resume after failures. Store task state in a durable store (database) rather than in memory. Each step should save its progress before proceeding to the next. This enables checkpoint-and-resume: if the system crashes mid-task, it can restart from the last checkpoint.

**Observability Checklist**

A production multi-agent system should provide:
- Structured logs for every agent action (JSON format for easy querying)
- Metrics: requests per second, error rates, latency percentiles per agent
- Traces: end-to-end execution trees showing agent-to-agent calls
- Alerts: notifications when error rates spike or latency degrades
- Dashboards: real-time visibility into system health
""",
        "order_num": 9,
        "tier": "pro",
    },
    {
        "id": 10,
        "title": "Evals — Measuring Agent Performance",
        "description": "Measure and improve agent quality using systematic evaluation frameworks. Covers eval metrics, test datasets, and continuous improvement pipelines.",
        "content": """Evaluation (evals) is the practice of systematically measuring how well an agent performs on a defined set of tasks. Without evals, you have no objective way to know whether your agent is getting better or worse as you iterate, whether a new model version is an improvement, or whether a prompt change fixed one problem while creating three others.

Evals are to agents what unit tests are to software: the foundation of reliable, iterative improvement.

**Why Evals are Uniquely Hard for Agents**

Traditional software testing is deterministic: given input X, the correct output Y is known. Agent outputs are often non-deterministic (the same input can produce different valid outputs) and subjective (what counts as a "good" answer?). This makes traditional testing approaches insufficient.

Agent evals must account for:
- **Non-determinism**: The same agent run might produce different but equally valid responses
- **Multi-step reasoning**: A wrong intermediate step might still lead to a correct final answer
- **Open-ended outputs**: There's often no single "correct" answer to compare against
- **Tool use**: Did the agent call the right tools in the right order?

**Types of Evals**

**1. Task Completion Evals**
Does the agent successfully complete the defined task? Binary pass/fail. Example: "Book a meeting for tomorrow at 2pm" — did the calendar event get created?

**2. Quality Evals**
How well does the agent complete the task on a continuous scale? Example: rate the accuracy, helpfulness, and conciseness of a research summary on a 1-5 scale.

**3. Regression Evals**
Does the agent still pass tests it previously passed? Run after every model update, prompt change, or tool modification to catch regressions.

**4. Adversarial Evals**
Does the agent behave safely when faced with edge cases, adversarial inputs, or attempts to jailbreak it? Critical for production systems.

**Building an Eval Dataset**

An eval dataset is a collection of (input, expected_output_or_criteria) pairs. Building a good dataset requires:
- **Real examples**: Use actual user queries from production logs (anonymised)
- **Edge cases**: Include unusual inputs that stress-test the agent
- **Coverage**: Cover all major use cases and user types
- **Ground truth**: For each example, define what success looks like (correct answer, criteria, or human rating)

A minimum viable eval dataset has 50-100 examples. Production systems need 500-1000+ for statistical significance.

**LLM-as-Judge**

One of the most powerful eval techniques is using a strong LLM (like Claude or GPT-4) to evaluate another LLM's output. You provide the judge with the input, the agent's output, and a rubric, and the judge scores the output. This scales to open-ended tasks where traditional metrics fail.

```python
def llm_judge(question: str, agent_answer: str, rubric: str) -> float:
    prompt = f'''Rate the following answer on a scale of 1-5 based on this rubric:
    Rubric: {rubric}
    Question: {question}
    Answer: {agent_answer}
    Return only a number 1-5.'''
    score = call_llm(prompt)
    return float(score)
```

**Eval Frameworks**

- **RAGAS**: Specialised for RAG pipeline evaluation. Measures faithfulness, answer relevance, context precision, and context recall.
- **DeepEval**: General-purpose eval framework with 14+ built-in metrics, LLM-as-judge support, and CI/CD integration.
- **Langfuse**: Observability + evals platform. Collect traces in production and run evals on them.
- **Braintrust**: Eval platform with dataset management, prompt playground, and A/B testing.

**Continuous Eval Pipelines**

The most mature teams run evals continuously as part of their development process:

1. **On every commit**: Run a fast eval suite (50 examples) to catch regressions before merge
2. **On every deployment**: Run a full eval suite (500+ examples) on the new production system
3. **Weekly**: Run adversarial evals and new example discovery against production traffic
4. **On model updates**: Run comprehensive evals before switching to a new model version

**The Eval-Driven Improvement Cycle**

1. Run evals → identify failure modes
2. Analyse failed examples → understand root causes
3. Fix root causes (prompt, tools, retrieval, model)
4. Re-run evals → confirm improvement, check for regressions
5. Deploy → collect new production failures
6. Add new failures to eval dataset → repeat

This cycle, applied consistently, leads to compounding improvements in agent quality over time.
""",
        "order_num": 10,
        "tier": "pro",
    },
]

# ── Quiz questions ────────────────────────────────────────────────────────────

QUIZZES = [
    # Chapter 1 — Introduction to AI Agents
    {"id": 1,  "chapter_id": 1, "order_num": 1, "question": "What is the primary role of an LLM in an AI agent?", "option_a": "Store data persistently", "option_b": "Act as the reasoning engine", "option_c": "Manage network requests", "option_d": "Handle authentication", "correct_answer": "B", "explanation": "The LLM (Large Language Model) serves as the brain of the agent — it reads the current state, reasons about what action to take next, and produces either a final answer or a tool call."},
    {"id": 2,  "chapter_id": 1, "order_num": 2, "question": "Which component allows an agent to remember past interactions?", "option_a": "Tools", "option_b": "Guardrails", "option_c": "Memory", "option_d": "Handoffs", "correct_answer": "C", "explanation": "Memory gives agents continuity across steps. Short-term memory holds the current conversation context; long-term memory stores facts and past experiences, often in a vector database."},
    {"id": 3,  "chapter_id": 1, "order_num": 3, "question": "What distinguishes an AI agent from a simple chatbot?", "option_a": "Larger model size", "option_b": "Autonomous goal pursuit with tool use", "option_c": "Faster response time", "option_d": "More training data", "correct_answer": "B", "explanation": "Unlike a chatbot that only generates text responses, an agent autonomously pursues goals by deciding on and executing a sequence of actions using tools, maintaining state across many steps."},
    {"id": 4,  "chapter_id": 1, "order_num": 4, "question": "What is the agent loop?", "option_a": "A debugging technique for LLMs", "option_b": "Perceive, Reason, Act, repeated until the goal is achieved", "option_c": "A network communication protocol", "option_d": "A type of memory storage", "correct_answer": "B", "explanation": "The agent loop is the cycle that drives autonomous behaviour: the agent perceives its environment, reasons about what to do, takes an action (such as calling a tool), observes the result, and repeats until the goal is complete."},
    {"id": 5,  "chapter_id": 1, "order_num": 5, "question": "Which of these is a real-world example of an AI agent use case?", "option_a": "Static website hosting", "option_b": "Autonomous code generation and testing", "option_c": "Serving cached HTML files", "option_d": "Running SQL queries on demand", "correct_answer": "B", "explanation": "Coding agents like Devin autonomously write code, run tests, observe failures, and iterate — a clear example of multi-step goal pursuit with tool use that goes far beyond what a chatbot can do."},

    # Chapter 2 — OpenAI Agents SDK
    {"id": 6,  "chapter_id": 2, "order_num": 1, "question": "What class represents an agent in the OpenAI Agents SDK?", "option_a": "Bot", "option_b": "Assistant", "option_c": "Agent", "option_d": "Runner", "correct_answer": "C", "explanation": "The Agent class is the core primitive in the OpenAI Agents SDK. It combines a model, instructions (system prompt), and a list of tools to define the agent's identity and capabilities."},
    {"id": 7,  "chapter_id": 2, "order_num": 2, "question": "What does Runner.run() do in the OpenAI Agents SDK?", "option_a": "Deploys the agent to production servers", "option_b": "Executes the agent loop until completion", "option_c": "Trains the underlying model", "option_d": "Opens a web server for the agent", "correct_answer": "B", "explanation": "Runner.run() executes the full agent loop: it sends messages to the model, handles tool calls, passes results back, and repeats until the agent produces a final text response."},
    {"id": 8,  "chapter_id": 2, "order_num": 3, "question": "What are Handoffs used for in the OpenAI Agents SDK?", "option_a": "Transferring files between servers", "option_b": "Passing control from one agent to another", "option_c": "Authenticating users", "option_d": "Caching LLM responses", "correct_answer": "B", "explanation": "Handoffs enable multi-agent architectures where a coordinator agent can route tasks to specialist agents. The receiving agent takes over the conversation and handles the task with its own tools and instructions."},
    {"id": 9,  "chapter_id": 2, "order_num": 4, "question": "What is the purpose of Guardrails in the OpenAI Agents SDK?", "option_a": "Network rate limiting", "option_b": "Input and output validation for safety", "option_c": "Memory management", "option_d": "Load balancing between models", "correct_answer": "B", "explanation": "Guardrails are safety checks that validate inputs before the agent processes them and outputs before they are returned to the user. They enforce business rules and prevent harmful content."},
    {"id": 10, "chapter_id": 2, "order_num": 5, "question": "How does the OpenAI Agents SDK support real-time streaming?", "option_a": "Via WebSockets only", "option_b": "Through periodic polling", "option_c": "Using Runner.run_streamed() which yields events as they occur", "option_d": "Via gRPC bidirectional streams", "correct_answer": "C", "explanation": "Runner.run_streamed() returns an async iterator that yields events (text deltas, tool calls, tool results) as they occur, enabling the client to display output progressively rather than waiting for completion."},

    # Chapter 3 — Anthropic Claude Agent SDK
    {"id": 11, "chapter_id": 3, "order_num": 1, "question": "How does Claude receive tool execution results?", "option_a": "Via a separate dedicated API call", "option_b": "As tool_result content blocks in the next message turn", "option_c": "Through environment variables", "option_d": "Via webhook callbacks", "correct_answer": "B", "explanation": "After Claude makes a tool_use request, you execute the tool and return the result as a tool_result content block in the next user message. Claude then continues its reasoning with this new information."},
    {"id": 12, "chapter_id": 3, "order_num": 2, "question": "What content block type does Claude use when it wants to call a tool?", "option_a": "function_call", "option_b": "tool_use", "option_c": "action", "option_d": "invoke", "correct_answer": "B", "explanation": "When Claude decides to use a tool, it returns a tool_use content block containing the tool name and input parameters. Your code detects this block, executes the tool, and returns the result."},
    {"id": 13, "chapter_id": 3, "order_num": 3, "question": "What is Claude's computer use capability?", "option_a": "Running terminal commands on the server", "option_b": "Controlling a computer GUI by taking screenshots and issuing actions", "option_c": "Browsing the web via URL requests only", "option_d": "Writing and executing files on disk", "correct_answer": "B", "explanation": "Claude's computer use capability allows it to perceive the screen via screenshots and issue keyboard and mouse commands, enabling agents to operate desktop applications and browser-based workflows without custom integrations."},
    {"id": 14, "chapter_id": 3, "order_num": 4, "question": "How do you primarily define a Claude agent's behaviour and personality?", "option_a": "By fine-tuning the model weights", "option_b": "Through a well-crafted system prompt", "option_c": "Via environment variables", "option_d": "Using configuration JSON files", "correct_answer": "B", "explanation": "The system prompt is where you define Claude's identity, capabilities, constraints, and tone. A carefully written system prompt is the most effective lever for shaping agent behaviour without any model training."},
    {"id": 15, "chapter_id": 3, "order_num": 5, "question": "What safety training approach does Anthropic use for Claude?", "option_a": "No automated safety measures", "option_b": "Constitutional AI — training the model to evaluate outputs against principles", "option_c": "User-managed keyword blocklists", "option_d": "Simple rate limiting on harmful topics", "correct_answer": "B", "explanation": "Constitutional AI (CAI) trains Claude to evaluate its own outputs against a set of principles and revise responses that violate them. This produces built-in safety behaviour that is robust to adversarial prompting."},

    # Chapter 4 — MCP Fundamentals
    {"id": 16, "chapter_id": 4, "order_num": 1, "question": "What does MCP stand for?", "option_a": "Multi-Cloud Protocol", "option_b": "Model Context Protocol", "option_c": "Managed Compute Platform", "option_d": "Message Control Protocol", "correct_answer": "B", "explanation": "MCP stands for Model Context Protocol — an open standard developed by Anthropic for connecting AI agents and LLM applications to external tools, data sources, and services."},
    {"id": 17, "chapter_id": 4, "order_num": 2, "question": "What are the three core MCP primitives?", "option_a": "Agents, Tools, Memory", "option_b": "Resources, Prompts, Tools", "option_c": "Models, Clients, Providers", "option_d": "Inputs, Outputs, Actions", "correct_answer": "B", "explanation": "MCP exposes capabilities through three primitives: Tools (functions agents can call), Resources (read-only data sources), and Prompts (reusable prompt templates). Every MCP server exposes some combination of these."},
    {"id": 18, "chapter_id": 4, "order_num": 3, "question": "In MCP architecture, what role does the AI agent play?", "option_a": "MCP Server", "option_b": "MCP Client", "option_c": "MCP Broker", "option_d": "MCP Registry", "correct_answer": "B", "explanation": "The AI agent acts as the MCP Client — it connects to MCP Servers and uses the tools and resources they expose. The server handles tool execution; the client handles agent logic and reasoning."},
    {"id": 19, "chapter_id": 4, "order_num": 4, "question": "Which transport layer is typically used for local MCP servers?", "option_a": "HTTP REST", "option_b": "WebSocket", "option_c": "stdio (standard input/output)", "option_d": "gRPC", "correct_answer": "C", "explanation": "Local MCP servers use stdio transport — the client launches the server as a child process and communicates via stdin/stdout. This is fast, simple, and requires no network configuration for local tool integrations."},
    {"id": 20, "chapter_id": 4, "order_num": 5, "question": "How does MCP differ from model-specific function calling?", "option_a": "MCP is significantly slower than function calling", "option_b": "MCP is a standardised protocol that works across any compatible model or client", "option_c": "MCP requires more tokens to describe tools", "option_d": "Function calling supports more concurrent tool calls", "correct_answer": "B", "explanation": "Function calling schemas are model-specific (OpenAI, Anthropic, and Google each have different formats). MCP defines a universal protocol — one MCP server works with any MCP-compatible client regardless of the underlying LLM."},

    # Chapter 5 — Advanced MCP Server Development
    {"id": 21, "chapter_id": 5, "order_num": 1, "question": "How do you register a tool in a Python MCP server?", "option_a": "Define a REST endpoint at /tools/{name}", "option_b": "Use the @server.list_tools() and @server.call_tool() handler decorators", "option_c": "Add an entry to a GraphQL schema", "option_d": "Register via a webhook URL", "correct_answer": "B", "explanation": "In the Python MCP SDK, you register tools by implementing two handlers: @server.list_tools() returns the tool definitions (names, descriptions, schemas), and @server.call_tool() executes the tool when called by a client."},
    {"id": 22, "chapter_id": 5, "order_num": 2, "question": "How should MCP tool handlers communicate errors to clients?", "option_a": "Return an empty response and log the error locally", "option_b": "Raise exceptions with descriptive messages that the SDK converts to structured error responses", "option_c": "Crash the server and let the client retry", "option_d": "Return None and let the client handle the null", "correct_answer": "B", "explanation": "MCP tool handlers should raise Python exceptions with clear messages. The SDK automatically converts these into structured MCP error responses that the client can interpret and present meaningfully to the agent."},
    {"id": 23, "chapter_id": 5, "order_num": 3, "question": "What is the purpose of MCP resource endpoints?", "option_a": "To store and manage user-uploaded files", "option_b": "To expose read-only data sources to the MCP client", "option_c": "To handle authentication and session management", "option_d": "To manage persistent server state", "correct_answer": "B", "explanation": "MCP resources are read-only data sources that the client can access via URIs (e.g., file:///path or db://table). Unlike tools (which perform actions), resources provide data — file contents, database records, configuration, logs, etc."},
    {"id": 24, "chapter_id": 5, "order_num": 4, "question": "What tool is recommended for testing MCP servers interactively during development?", "option_a": "Deploy to production and test live", "option_b": "MCP Inspector — a browser-based debugging tool from Anthropic", "option_c": "Write unit tests only with mock clients", "option_d": "Use Postman with custom MCP headers", "correct_answer": "B", "explanation": "The MCP Inspector (npx @modelcontextprotocol/inspector) is a browser-based tool that connects to your local MCP server and lets you call tools, browse resources, and inspect all protocol messages in real time — ideal for development and debugging."},
    {"id": 25, "chapter_id": 5, "order_num": 5, "question": "What authentication method is recommended for remote MCP servers?", "option_a": "No authentication is needed for MCP servers", "option_b": "API keys or OAuth2 tokens validated on every request", "option_c": "IP address whitelisting only", "option_d": "Client certificate pinning only", "correct_answer": "B", "explanation": "Remote MCP servers should require authentication on every request. API keys (in Authorization headers) are simple and effective; OAuth2 enables user-delegated access for servers that act on behalf of specific users (e.g., accessing their Google Drive)."},

    # Chapter 6 — Agent Skills & MCP Code Execution
    {"id": 26, "chapter_id": 6, "order_num": 1, "question": "What is an agent skill in the context of AI agents?", "option_a": "A model capability learned during pre-training", "option_b": "A reusable, registered capability an agent can invoke to accomplish a specific task", "option_c": "A type of system prompt template", "option_d": "A long-term memory module", "correct_answer": "B", "explanation": "An agent skill is a named, well-defined, reusable capability — higher-level than a raw tool. A skill might coordinate multiple tool calls to accomplish a goal (e.g., a research topic skill that searches, reads, and summarises)."},
    {"id": 27, "chapter_id": 6, "order_num": 2, "question": "Which service provides cloud-based micro VMs specifically designed for AI agent code execution?", "option_a": "Docker Hub", "option_b": "E2B (e2b.dev) cloud sandboxes", "option_c": "Local Python interpreter", "option_d": "AWS Lambda functions", "correct_answer": "B", "explanation": "E2B provides cloud-based micro virtual machines designed for AI code execution. Each sandbox is an isolated Linux environment that starts in under a second and is automatically cleaned up — safe for executing agent-generated code."},
    {"id": 28, "chapter_id": 6, "order_num": 3, "question": "Why is sandboxing essential when agents execute code?", "option_a": "It significantly improves code execution speed", "option_b": "It isolates potentially dangerous code from the host system, preventing damage", "option_c": "It reduces API costs by caching results", "option_d": "It simplifies deployment pipelines", "correct_answer": "B", "explanation": "Agent-generated code may be malicious or buggy. Without sandboxing, it could delete files, exfiltrate data, consume system resources, or crash the host. Sandboxes provide isolation so that even harmful code cannot escape the execution environment."},
    {"id": 29, "chapter_id": 6, "order_num": 4, "question": "What is skill chaining?", "option_a": "Linking multiple API authentication tokens", "option_b": "Composing multiple skills sequentially where the output of one becomes the input of the next", "option_c": "Training multiple skills simultaneously on the same dataset", "option_d": "Caching skill results for reuse across sessions", "correct_answer": "B", "explanation": "Skill chaining composes multiple skills into a pipeline to accomplish complex tasks. For example: search_web, read_page, extract_data, execute_analysis, format_report — where each skill's output feeds the next."},
    {"id": 30, "chapter_id": 6, "order_num": 5, "question": "What is the primary security risk of allowing agents to execute code without sandboxing?", "option_a": "Slower execution performance", "option_b": "Arbitrary code execution on the host system with full access", "option_c": "Higher LLM token consumption", "option_d": "Memory leaks in the Python interpreter", "correct_answer": "B", "explanation": "Without sandboxing, agent-generated code runs on the host system with the same permissions as the agent process. This enables arbitrary file deletion, data exfiltration, network attacks, and complete system compromise."},

    # Chapter 7 — FastAPI for Agents
    {"id": 31, "chapter_id": 7, "order_num": 1, "question": "What makes FastAPI particularly suitable for building agent-facing backends?", "option_a": "It is the oldest and most mature Python web framework", "option_b": "Its async support, automatic OpenAPI docs, and Pydantic validation", "option_c": "It uses XML for data serialisation", "option_d": "It requires no configuration to deploy", "correct_answer": "B", "explanation": "FastAPI's async-first design handles concurrent agent requests efficiently. Automatic OpenAPI documentation enables ChatGPT Apps to discover endpoints. Pydantic validation ensures request/response data integrity with minimal boilerplate."},
    {"id": 32, "chapter_id": 7, "order_num": 2, "question": "How does FastAPI's dependency injection system help agent API development?", "option_a": "It speeds up LLM inference by caching responses", "option_b": "It shares resources like authentication and DB connections cleanly across routes", "option_c": "It manages machine learning model weights automatically", "option_d": "It handles HTTP caching headers automatically", "correct_answer": "B", "explanation": "FastAPI's Depends() system lets you define shared dependencies (authentication, database sessions, configuration) once and inject them into any route. This keeps route handlers clean and avoids repetition."},
    {"id": 33, "chapter_id": 7, "order_num": 3, "question": "What does FastAPI automatically generate from your route definitions and Pydantic models?", "option_a": "Database migration scripts", "option_b": "Interactive OpenAPI/Swagger documentation", "option_c": "Unit test scaffolding", "option_d": "Docker deployment configurations", "correct_answer": "B", "explanation": "FastAPI introspects your route definitions, Pydantic models, and type annotations to automatically generate OpenAPI documentation available at /docs. This is what ChatGPT Apps use to understand your API's capabilities."},
    {"id": 34, "chapter_id": 7, "order_num": 4, "question": "How can you stream an agent's response progressively in FastAPI?", "option_a": "Only via client-side polling with timeouts", "option_b": "Using StreamingResponse or WebSocket endpoints", "option_c": "Via HTTP/1.0 chunked encoding only", "option_d": "By returning results via background jobs and polling", "correct_answer": "B", "explanation": "FastAPI's StreamingResponse lets you yield chunks as they are generated (server-sent events pattern). WebSocket endpoints enable bidirectional real-time communication for interactive agent sessions."},
    {"id": 35, "chapter_id": 7, "order_num": 5, "question": "Which platform is recommended for deploying FastAPI agent backends in this course?", "option_a": "Only on-premise physical servers", "option_b": "Railway, using uvicorn with --host 0.0.0.0 --port $PORT", "option_c": "FTP servers with cPanel", "option_d": "GitHub Pages static hosting", "correct_answer": "B", "explanation": "Railway is the recommended PaaS for this course. Connect your GitHub repository, set the start command to uvicorn main:app --host 0.0.0.0 --port $PORT, add environment variables, and Railway handles deployment, HTTPS, and scaling automatically."},

    # Chapter 8 — Vector Databases & RAG
    {"id": 36, "chapter_id": 8, "order_num": 1, "question": "What is a vector embedding?", "option_a": "A compressed image representation for storage", "option_b": "A numerical representation of text that captures its semantic meaning", "option_c": "A database index structure for fast lookups", "option_d": "A set of model weights for fine-tuning", "correct_answer": "B", "explanation": "A vector embedding is a list of numbers (typically 768-3072 floats) that encodes the semantic content of text. Texts with similar meanings have mathematically similar embeddings, enabling semantic search."},
    {"id": 37, "chapter_id": 8, "order_num": 2, "question": "What does RAG stand for?", "option_a": "Rapid Agent Generation", "option_b": "Retrieval-Augmented Generation", "option_c": "Recursive Attention Gradient", "option_d": "Resource Allocation Graph", "correct_answer": "B", "explanation": "RAG stands for Retrieval-Augmented Generation. It is a pattern where relevant documents are retrieved from a knowledge base and included in the LLM's context before it generates a response, enabling accurate answers about documents the model wasn't trained on."},
    {"id": 38, "chapter_id": 8, "order_num": 3, "question": "Which similarity metric is most commonly used to compare vector embeddings?", "option_a": "Euclidean distance exclusively", "option_b": "Cosine similarity", "option_c": "Hamming distance", "option_d": "Jaccard index", "correct_answer": "B", "explanation": "Cosine similarity measures the angle between two vectors (1.0 = identical direction, 0.0 = perpendicular). It is the standard metric for embedding comparison because it is robust to differences in vector magnitude."},
    {"id": 39, "chapter_id": 8, "order_num": 4, "question": "What is document chunking in a RAG pipeline?", "option_a": "Compressing model weights for faster inference", "option_b": "Splitting documents into smaller pieces before embedding them", "option_c": "Batching multiple API requests together", "option_d": "Caching embeddings across sessions", "correct_answer": "B", "explanation": "Documents are split into chunks before embedding because LLMs have context limits and smaller chunks produce more focused embeddings. Chunk size is a key tunable parameter — too small loses context, too large dilutes relevance."},
    {"id": 40, "chapter_id": 8, "order_num": 5, "question": "What is hybrid search in the context of RAG?", "option_a": "Searching across two separate databases simultaneously", "option_b": "Combining vector similarity search with keyword (BM25) search", "option_c": "Using two different embedding models in parallel", "option_d": "Searching both images and text in the same query", "correct_answer": "B", "explanation": "Hybrid search combines semantic vector search (good for meaning-based queries) with keyword search like BM25 (good for exact matches on names, codes, IDs). Most production RAG systems use hybrid search for best overall recall."},

    # Chapter 9 — Multi-Agent Reliability
    {"id": 41, "chapter_id": 9, "order_num": 1, "question": "In the orchestrator-worker multi-agent pattern, what is the orchestrator's role?", "option_a": "Each agent works entirely independently with no coordination", "option_b": "A coordinator agent breaks down goals, delegates to workers, and assembles results", "option_c": "Agents vote democratically on each action to take", "option_d": "All agents share a single shared memory and act together", "correct_answer": "B", "explanation": "The orchestrator receives the high-level goal, decomposes it into subtasks, delegates each to the most suitable worker agent, monitors progress, and assembles the final result. This enables parallelism and specialisation."},
    {"id": 42, "chapter_id": 9, "order_num": 2, "question": "What does a circuit breaker do in a multi-agent system?", "option_a": "Controls electrical safety in data centres", "option_b": "Stops sending requests to a repeatedly failing service to prevent cascading failures", "option_c": "Enforces firewall rules between agents", "option_d": "Limits the number of tool calls an agent can make", "correct_answer": "B", "explanation": "A circuit breaker tracks failures for a service. After N failures, it opens and immediately rejects further requests (rather than waiting for timeouts), preventing resource exhaustion and allowing the failing service time to recover."},
    {"id": 43, "chapter_id": 9, "order_num": 3, "question": "Why is idempotency important for agent actions?", "option_a": "It makes agent actions execute faster", "option_b": "It ensures repeating an action produces the same result without unintended side effects", "option_c": "It reduces token usage in the LLM", "option_d": "It simplifies the agent's system prompt", "correct_answer": "B", "explanation": "Agents may retry failed actions or re-execute steps due to crashes. If actions are not idempotent, retries cause duplicate orders, double-sent emails, or duplicate database records. Idempotency keys prevent these problems."},
    {"id": 44, "chapter_id": 9, "order_num": 4, "question": "What does distributed tracing provide in a multi-agent system?", "option_a": "Faster LLM inference through distributed computation", "option_b": "End-to-end visibility into agent interactions, tool calls, and latency across the full system", "option_c": "Automatic retry logic for failed agent steps", "option_d": "Shared memory between agents running in different processes", "correct_answer": "B", "explanation": "Distributed tracing captures the full execution tree — which agent called which tool, how long each step took, where errors occurred, and how agents handed off to each other. This is essential for debugging complex multi-agent failures."},
    {"id": 45, "chapter_id": 9, "order_num": 5, "question": "What is failure isolation in multi-agent system design?", "option_a": "Running each agent in a separate geographic region", "option_b": "Designing so that one agent's failure does not cascade and bring down other agents", "option_c": "Using different LLM models for different agents", "option_d": "Keeping training data separate for each agent", "correct_answer": "B", "explanation": "Failure isolation means that when one agent or tool fails, the impact is contained. Techniques include timeouts, bounded retries, fallback responses, and dead letter queues — so the overall system degrades gracefully rather than failing completely."},

    # Chapter 10 — Evals
    {"id": 46, "chapter_id": 10, "order_num": 1, "question": "Why are evals essential for agent development?", "option_a": "They replace the need for unit tests entirely", "option_b": "They provide an objective measure of whether agents reliably achieve goals", "option_c": "They train the underlying language model", "option_d": "They reduce API latency in production", "correct_answer": "B", "explanation": "Without evals, you have no objective way to know if your agent is improving or regressing as you iterate. Evals are to agents what unit tests are to software — the foundation of reliable, data-driven improvement."},
    {"id": 47, "chapter_id": 10, "order_num": 2, "question": "What is LLM-as-judge in agent evaluation?", "option_a": "A legal framework for AI liability", "option_b": "Using a strong LLM to score another LLM's outputs against a rubric", "option_c": "A standardised benchmark dataset for LLMs", "option_d": "A fine-tuning technique for evaluation models", "correct_answer": "B", "explanation": "LLM-as-judge uses a capable model (like Claude or GPT-4) to evaluate another model's outputs. You provide the judge with the input, the agent's output, and a scoring rubric. This scales to open-ended tasks where traditional metrics fail."},
    {"id": 48, "chapter_id": 10, "order_num": 3, "question": "What is a regression eval in the context of agent testing?", "option_a": "A test that is designed to always pass", "option_b": "A test that ensures previously working behaviour still works after changes", "option_c": "A performance load test under high traffic", "option_d": "A security penetration test for agents", "correct_answer": "B", "explanation": "Regression evals run after every code change, prompt update, or model switch to verify that capabilities that previously worked still work. They catch the common problem of fixing one thing and accidentally breaking another."},
    {"id": 49, "chapter_id": 10, "order_num": 4, "question": "What does the RAGAS framework measure?", "option_a": "Model parameter counts and memory usage", "option_b": "RAG pipeline quality including faithfulness and answer relevance", "option_c": "API endpoint latency and throughput", "option_d": "Token costs per query", "correct_answer": "B", "explanation": "RAGAS is specialised for evaluating RAG pipelines. Its key metrics include Faithfulness (does the answer stick to the retrieved context?), Answer Relevance (does it address the question?), Context Precision, and Context Recall."},
    {"id": 50, "chapter_id": 10, "order_num": 5, "question": "What is the primary input to an agent evaluation pipeline?", "option_a": "The model's weight files", "option_b": "A dataset of input examples paired with expected outputs or evaluation criteria", "option_c": "API authentication keys", "option_d": "Production deployment configuration files", "correct_answer": "B", "explanation": "An eval dataset is the foundation of any eval pipeline. Each example pairs an input (user query, task description) with expected output or evaluation criteria (correct answer, rubric, pass/fail conditions). Building a good dataset is the hardest part of evals."},
]


# ── Seeding functions ─────────────────────────────────────────────────────────

def seed_chapters():
    print("Seeding chapters...")
    result = supabase.table("chapters").upsert(CHAPTERS).execute()
    count = len(result.data) if result.data else 0
    print(f"✓ Upserted {count} chapters")
    return count


def seed_quizzes():
    print("Seeding quizzes...")
    result = supabase.table("quizzes").upsert(QUIZZES).execute()
    count = len(result.data) if result.data else 0
    print(f"✓ Upserted {count} quiz questions")
    return count


def main():
    ch_count = seed_chapters()
    q_count = seed_quizzes()
    print(f"\nSeeding complete — {ch_count} chapters, {q_count} questions.")


if __name__ == "__main__":
    main()
