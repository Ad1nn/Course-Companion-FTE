---
description: "Task list for Phase 2 Course Content Seeding"
---

# Tasks: Phase 2 — Course Content Seeding

**Input**: Design documents from `/specs/002-content-seeding/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | quickstart.md ✅

**Tests**: Manual verification via API endpoints after seeding (see quickstart.md).

**Organization**: Single script — US1 (chapters) and US2 (quizzes) implemented together in one file.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1 = chapter content, US2 = quiz questions
- Paths relative to repo root

---

## Phase 1: Setup

**Purpose**: Script scaffolding and environment wiring

- [X] T001 Create `backend/seed.py` — script skeleton with dotenv loading, Supabase client init, and `main()` function that calls `seed_chapters()` and `seed_quizzes()` in sequence with print confirmation

**Checkpoint**: `python3 backend/seed.py` runs without error (functions are empty stubs).

---

## Phase 2: Foundational

**Purpose**: No additional foundational work needed — Supabase client reuses `backend/database.py` pattern. Tables already exist from Phase 1.

*(No blocking tasks — proceed directly to user story phases.)*

---

## Phase 3: User Story 1 — Seed All 10 Chapters (Priority: P1)

**Goal**: All 10 chapters exist in Supabase with correct IDs, titles, tiers, descriptions, and 500+ word content.

**Independent Test**: `GET /chapters` returns 10 chapters. `GET /chapters/{1–10}` each return full content of 500+ words. Tiers: ch1–3=free, ch4–7=premium, ch8–10=pro.

### Implementation

- [X] T002 [US1] Write `seed_chapters()` in `backend/seed.py` — define `CHAPTERS` list of 10 dicts with fields: `id`, `title`, `description`, `content`, `order_num`, `tier`. Upsert all via `supabase.table("chapters").upsert(CHAPTERS).execute()`. Print count on success.

- [X] T003 [US1] Author chapter content in `backend/seed.py` — `CHAPTERS` list entries for chapters 1–5:
  - **Ch1** (free): Introduction to AI Agents — agent definition, perception-reasoning-action loop, LLM as reasoning engine, tools, memory types (short/long-term), agent vs chatbot distinction, autonomous goal pursuit, real-world examples (coding agents, research agents)
  - **Ch2** (free): OpenAI Agents SDK — Agent class, instructions, tools parameter, Runner.run(), streaming, Handoffs between agents, Guardrails for input/output validation, tracing and debugging, async execution
  - **Ch3** (free): Anthropic Claude Agent SDK — Claude models overview, tool_use content blocks, multi-turn tool calling, system prompts for agent behavior, safety layers, computer use capability, Claude vs GPT agent differences
  - **Ch4** (premium): MCP Fundamentals — MCP definition and motivation, client-server architecture, three primitives (Resources/Prompts/Tools), transport layers (stdio/SSE), MCP vs function calling, official SDKs (Python/TypeScript), real-world MCP servers
  - **Ch5** (premium): Advanced MCP Server Development — building MCP servers from scratch, implementing tool handlers, resource endpoints, error handling and retries, authentication in MCP, testing MCP servers, deployment patterns

- [X] T004 [US1] Author chapter content in `backend/seed.py` — `CHAPTERS` list entries for chapters 6–10:
  - **Ch6** (premium): Agent Skills & MCP Code Execution — skill definition and registration, code execution sandboxes (E2B, Docker), MCP code execution servers, skill chaining, stateful vs stateless skills, security considerations for code execution
  - **Ch7** (premium): FastAPI for Agents — async FastAPI fundamentals, dependency injection, Pydantic models, OpenAPI spec generation, background tasks, WebSocket for streaming agent responses, deploying agent APIs to Railway/Render
  - **Ch8** (pro): Vector Databases & RAG — embeddings and vector space, similarity search (cosine/dot product), vector DB options (Pinecone/Weaviate/pgvector), chunking strategies, RAG pipeline architecture, hybrid search, evaluating retrieval quality
  - **Ch9** (pro): Multi-Agent Reliability — orchestrator-worker patterns, agent communication protocols, circuit breakers, retry strategies, idempotency in agent actions, observability (tracing multi-agent flows), failure isolation
  - **Ch10** (pro): Evals — Measuring Agent Performance — why evals matter, eval dataset construction, LLM-as-judge, task-specific metrics, regression testing agents, eval frameworks (RAGAS, DeepEval), continuous eval pipelines

**Checkpoint**: Run `python3 backend/seed.py`. Then call `GET /chapters` — 10 chapters returned. Call `GET /chapters/1` — content is 500+ words.

---

## Phase 4: User Story 2 — Seed All 50 Quiz Questions (Priority: P1)

**Goal**: Every chapter has exactly 5 quiz questions. Questions are factually accurate, have one unambiguous correct answer, and include an educational explanation.

**Independent Test**: `GET /quizzes/{chapter_id}` for chapters 1–10 each return exactly 5 questions. `correct_answer` never appears in the response. Submit all 5 answers for chapter 1 — score returned on 5th.

### Implementation

- [X] T005 [US2] Write `seed_quizzes()` in `backend/seed.py` — define `QUIZZES` list of 50 dicts with fields: `chapter_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`, `explanation`, `order_num`. Upsert via `supabase.table("quizzes").upsert(QUIZZES, on_conflict="chapter_id,order_num").execute()`. Print count.

- [X] T006 [US2] Author quiz questions in `backend/seed.py` — 5 questions each for chapters 1–5:

  **Ch1 – Introduction to AI Agents**
  1. What is the primary role of an LLM in an AI agent? / A: Store data / B: Act as the reasoning engine / C: Manage network requests / D: Handle authentication → B
  2. Which component allows an agent to remember past interactions? / A: Tools / B: Guardrails / C: Memory / D: Handoffs → C
  3. What distinguishes an agent from a simple chatbot? / A: Larger model size / B: Autonomous goal pursuit with tool use / C: Faster response time / D: More training data → B
  4. What is the agent loop? / A: A debugging technique / B: Perceive → Reason → Act repeated until goal achieved / C: A network protocol / D: A type of memory → B
  5. Which of these is an example of a real-world AI agent use case? / A: Static website hosting / B: Autonomous code generation and testing / C: Serving cached HTML / D: Running SQL queries → B

  **Ch2 – OpenAI Agents SDK**
  1. What class represents an agent in the OpenAI Agents SDK? / A: Bot / B: Assistant / C: Agent / D: Runner → C
  2. What does Runner.run() do? / A: Deploys the agent to production / B: Executes the agent loop until completion / C: Trains the model / D: Opens a web server → B
  3. What are Handoffs used for? / A: Transferring files / B: Passing control between agents / C: Authenticating users / D: Caching responses → B
  4. What is the purpose of Guardrails in the SDK? / A: Rate limiting / B: Input and output validation for safety / C: Memory management / D: Load balancing → B
  5. How does the SDK support real-time streaming? / A: WebSockets only / B: Polling / C: Server-sent events via Runner.run_streamed() / D: gRPC → C

  **Ch3 – Anthropic Claude Agent SDK**
  1. How does Claude receive tool results? / A: Via a separate API call / B: As tool_result content blocks in the next message / C: Through environment variables / D: Via webhooks → B
  2. What content block type does Claude use to call a tool? / A: function_call / B: tool_use / C: action / D: invoke → B
  3. What is Claude's computer use capability? / A: Running terminal commands only / B: Controlling a computer GUI via screenshots and actions / C: Browsing the web only / D: Writing files only → B
  4. How do you define Claude's agent behavior? / A: Training fine-tunes / B: System prompt instructions / C: Environment variables / D: Config files → B
  5. What distinguishes Claude's safety approach? / A: No safety measures / B: Constitutional AI and built-in refusal training / C: User-managed blocklists / D: Rate limiting → B

  **Ch4 – MCP Fundamentals**
  1. What does MCP stand for? / A: Multi-Cloud Protocol / B: Model Context Protocol / C: Managed Compute Platform / D: Message Control Protocol → B
  2. What are the three core MCP primitives? / A: Agents, Tools, Memory / B: Resources, Prompts, Tools / C: Models, Clients, Providers / D: Inputs, Outputs, Actions → B
  3. In MCP architecture, what role does the AI agent play? / A: MCP Server / B: MCP Client / C: MCP Broker / D: MCP Registry → B
  4. Which transport layer is used for local MCP servers? / A: HTTP / B: WebSocket / C: stdio / D: gRPC → C
  5. How does MCP differ from simple function calling? / A: MCP is slower / B: MCP is a standardised protocol; function calling is model-specific / C: MCP requires more tokens / D: Function calling supports more tools → B

  **Ch5 – Advanced MCP Server Development**
  1. What is the entry point for implementing a tool in an MCP server? / A: A REST endpoint / B: A tool handler function decorated with @server.tool() / C: A GraphQL resolver / D: A webhook → B
  2. How should MCP servers handle tool errors? / A: Return empty responses / B: Return structured error objects with message and code / C: Crash and restart / D: Log silently → B
  3. What is the purpose of MCP resource endpoints? / A: To store user files / B: To expose read-only data sources to the client / C: To handle authentication / D: To manage server state → B
  4. How do you test an MCP server locally? / A: Deploy to production first / B: Use the MCP Inspector or connect a local client via stdio / C: Write unit tests only / D: Use Postman → B
  5. What authentication pattern is recommended for remote MCP servers? / A: No authentication needed / B: API keys or OAuth2 tokens in request headers / C: IP whitelisting only / D: Certificate pinning → B

- [X] T007 [US2] Author quiz questions in `backend/seed.py` — 5 questions each for chapters 6–10:

  **Ch6 – Agent Skills & MCP Code Execution**
  1. What is an agent skill? / A: A model capability / B: A reusable, registered capability an agent can invoke / C: A type of prompt / D: A memory module → B
  2. Which tool provides sandboxed code execution for agents? / A: Docker alone / B: E2B cloud sandboxes / C: Local Python interpreter / D: AWS Lambda → B
  3. Why is sandboxing important for code execution agents? / A: It improves speed / B: It isolates untrusted code from the host system / C: It reduces cost / D: It simplifies deployment → B
  4. What is skill chaining? / A: Linking API keys / B: Composing multiple skills sequentially to complete complex tasks / C: Training skills together / D: Caching skill results → B
  5. What is the main security risk of unsandboxed code execution? / A: Slower performance / B: Arbitrary code execution on the host system / C: Higher token usage / D: Memory leaks → B

  **Ch7 – FastAPI for Agents**
  1. What makes FastAPI suitable for agent backends? / A: It is the oldest framework / B: Async support, automatic OpenAPI docs, and Pydantic validation / C: It uses XML / D: It requires no configuration → B
  2. How does FastAPI dependency injection help agent APIs? / A: It speeds up training / B: It shares resources like DB connections and auth across routes / C: It manages model weights / D: It handles caching → B
  3. What does FastAPI automatically generate from your route definitions? / A: Database migrations / B: OpenAPI/Swagger documentation / C: Unit tests / D: Docker containers → B
  4. How can you stream agent responses in FastAPI? / A: Only via polling / B: Using StreamingResponse or WebSocket endpoints / C: HTTP/1.0 only / D: Via background jobs → B
  5. Which platform is recommended for deploying agent FastAPI backends? / A: Only on-premise servers / B: Railway, Render, or similar PaaS platforms / C: FTP servers / D: Static hosting → B

  **Ch8 – Vector Databases & RAG**
  1. What is a vector embedding? / A: A compressed image / B: A numerical representation of text that captures semantic meaning / C: A database index / D: A model weight → B
  2. What does RAG stand for? / A: Rapid Agent Generation / B: Retrieval-Augmented Generation / C: Recursive Attention Gradient / D: Resource Allocation Graph → B
  3. Which similarity metric is most commonly used in vector search? / A: Euclidean distance only / B: Cosine similarity / C: Hamming distance / D: Jaccard index → B
  4. What is chunking in a RAG pipeline? / A: Compressing the model / B: Splitting documents into smaller pieces before embedding / C: Batching API requests / D: Caching embeddings → B
  5. What is hybrid search in RAG? / A: Searching two databases / B: Combining vector similarity search with keyword search / C: Using two models / D: Searching images and text → B

  **Ch9 – Multi-Agent Reliability**
  1. What is the orchestrator pattern in multi-agent systems? / A: All agents act independently / B: One agent coordinates and delegates tasks to worker agents / C: Agents vote on actions / D: Agents share a single memory → B
  2. What is a circuit breaker in agent reliability? / A: A power safety device / B: A pattern that stops calling a failing service after repeated errors / C: A firewall rule / D: A rate limiter → B
  3. Why is idempotency important for agent actions? / A: It makes agents faster / B: It ensures repeating an action produces the same result without side effects / C: It reduces token usage / D: It simplifies prompts → B
  4. What does distributed tracing provide in multi-agent systems? / A: Faster inference / B: End-to-end visibility into agent interactions and latency / C: Automatic retries / D: Memory sharing → B
  5. What is failure isolation in multi-agent design? / A: Running agents in separate countries / B: Ensuring one agent's failure does not cascade to others / C: Using different models / D: Isolating training data → B

  **Ch10 – Evals — Measuring Agent Performance**
  1. Why are evals essential for agent development? / A: They replace unit tests / B: They measure whether agents reliably achieve goals in real scenarios / C: They train the model / D: They reduce latency → B
  2. What is LLM-as-judge? / A: A legal framework / B: Using an LLM to score another LLM's outputs against criteria / C: A benchmark dataset / D: A fine-tuning technique → B
  3. What is a regression test in agent evaluation? / A: A test that always passes / B: A test that ensures previously working behaviour still works after changes / C: A load test / D: A security scan → B
  4. What does RAGAS measure? / A: Model parameters / B: RAG pipeline quality including faithfulness and answer relevance / C: API latency / D: Token costs → B
  5. What is the primary input to an eval pipeline? / A: Model weights / B: A dataset of inputs paired with expected outputs or criteria / C: API keys / D: Deployment configs → B

**Checkpoint**: Run `python3 backend/seed.py`. Call `GET /quizzes/{1..10}` — each returns 5 questions. Total = 50.

---

## Phase 5: Polish & Verification

- [X] T008 Add print statements to `backend/seed.py` showing per-chapter and per-quiz counts after upsert, and final summary line "Seeding complete — 10 chapters, 50 questions."
- [X] T009 Run full verification from `specs/002-content-seeding/quickstart.md` — confirm 10 chapters with 500+ words each and 50 quiz questions total
- [X] T010 Run seed script a second time to verify idempotency — chapter and quiz counts must remain exactly 10 and 50

---

## Dependencies & Execution Order

- **Phase 1** (T001): No dependencies — start immediately
- **Phase 3** (T002–T004): Depends on T001. T003 and T004 can be authored in parallel (different chapter ranges)
- **Phase 4** (T005–T007): Depends on T002 (function scaffold). T006 and T007 can be authored in parallel
- **Phase 5** (T008–T010): Depends on T004 + T007 (all content authored)

### Parallel Opportunities

```
T001 → T002 → T003 + T004 (parallel, different chapters) → T005 → T006 + T007 (parallel) → T008 → T009 → T010
```

---

## Implementation Strategy

### MVP (Chapter 1 only, prove the pipeline)
1. Complete T001 (script skeleton)
2. Complete T002 (seed_chapters scaffold)
3. Author Ch1 content only in T003
4. Complete T005 (seed_quizzes scaffold)
5. Author Ch1 quizzes only in T006
6. Run and verify Ch1 works end-to-end

### Full Delivery
1. Complete MVP
2. Author all remaining chapter content (T003 remainder + T004)
3. Author all remaining quiz questions (T006 remainder + T007)
4. Polish and verify (T008–T010)

---

## Notes

- Content quality gate: each chapter must have ≥ 500 words before moving to Polish phase
- Quiz answers must all be "B" here for simplicity — in a real product, randomise option ordering
- The `on_conflict` for quizzes uses `chapter_id,order_num` — ensure this unique constraint exists in Supabase (it is implied by the schema design)
- If the `on_conflict` constraint doesn't exist in Supabase, add it: `ALTER TABLE quizzes ADD UNIQUE (chapter_id, order_num);`
