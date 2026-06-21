# 🏠 HomeOS

### Autonomous Household Economic Intelligence Platform

HomeOS is an AI-powered multi-agent system designed to help households reduce food waste, optimize grocery spending, automate meal planning, and maintain accurate pantry inventories.

Built for **Agentrix 2026**, HomeOS combines Multi-Agent AI, Retrieval-Augmented Generation (RAG), Inventory Intelligence, and Household Economic Optimization into a single autonomous platform.

---

# 📌 Problem Statement

Modern households face several recurring challenges:

* Food waste due to forgotten or expiring ingredients
* Inefficient grocery shopping
* Lack of pantry visibility
* Poor meal planning
* Budget overruns
* Manual inventory tracking

HomeOS addresses these issues through an intelligent agent ecosystem capable of planning, reasoning, retrieving knowledge, validating decisions, and tracking real-world consumption.

---

# 🎯 Project Objectives

* Reduce household food waste
* Optimize grocery spending
* Generate intelligent meal plans
* Track pantry inventory automatically
* Utilize expiring ingredients first
* Provide explainable AI decision making
* Demonstrate advanced Agentic AI patterns

---

# 🚀 Key Features

## Multi-Agent Meal Planning

Generates intelligent meal plans based on:

* Available inventory
* Family size
* Budget constraints
* Ingredient expiry dates
* Historical meal preferences
* Waste-risk scores

---

## Retrieval-Augmented Generation (RAG)

Uses semantic search to retrieve relevant recipes before planning.

Capabilities:

* Recipe vectorization
* Embedding generation
* Similarity search
* Context-aware meal recommendations

---

## Inventory Management

Tracks:

* Current stock levels
* Ingredient consumption
* Pantry replenishment
* Expiry monitoring

Features:

* Automatic stock deduction
* Inventory dashboard
* Pantry health monitoring

---

## Meal Execution Tracking

When a meal is completed:

* Ingredients are deducted automatically
* Family-size scaling is applied
* Inventory updates instantly
* Agent trace is recorded

---

## Receipt Processing

Users can upload or enter receipt data.

The system:

* Extracts purchased items
* Updates pantry inventory
* Stores purchase history
* Maintains stock consistency

---

## Reflection & Self-Correction

A dedicated Reflection Agent validates generated plans.

Checks:

* Budget compliance
* Waste reduction goals
* Ingredient utilization
* Planning constraints

If issues are detected, the workflow automatically re-plans.

---

## Explainable AI

Every decision is traceable through:

* Agent traces
* Decision logs
* Reflection reports
* Planning summaries

---

# 🏗 System Architecture

```text
Frontend (React + Vite)
            │
            ▼
      FastAPI Backend
            │
            ▼
      LangGraph Workflow
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
SQLite    Qdrant     Gemini
Database  Vector DB    AI
```

---

# 🤖 Agent Architecture

## Coordinator Agent

Responsibilities:

* Initialize planning workflow
* Collect user objectives
* Load historical meal records

---

## Inventory Agent

Responsibilities:

* Retrieve pantry inventory
* Detect expiring ingredients
* Prepare inventory context

---

## Waste Analysis Agent

Responsibilities:

* Calculate spoilage risk
* Prioritize ingredient usage
* Generate waste scores

---

## Recipe Retrieval Agent

Responsibilities:

* Query Qdrant
* Retrieve candidate recipes
* Provide RAG context

---

## Meal Planner Agent

Responsibilities:

* Generate meal schedules
* Balance nutrition and budget
* Produce planning rationale

---

## Budget Agent

Responsibilities:

* Estimate meal costs
* Generate shopping lists
* Validate affordability

---

## Reflection Agent

Responsibilities:

* Critique generated plans
* Validate constraints
* Trigger self-correction

---

## Reporting Agent

Responsibilities:

* Compile final plan
* Generate user-facing output
* Preserve explainability

---

# 🧠 AI Technologies

## Large Language Models

### Google Gemini 2.5 Flash

Used for:

* Meal planning
* Reflection
* Reasoning
* Constraint validation

---

## Embedding Model

### Gemini Embedding Model

Used for:

* Recipe vectorization
* Semantic retrieval
* Similarity matching

---

## Agent Framework

### LangGraph

Used to orchestrate:

* Agent workflows
* State transitions
* Reflection loops
* Multi-agent collaboration

---

# 🗄 Database Architecture

## SQLite Database

Stores:

### Inventory

* Ingredients
* Quantities
* Expiry dates
* Original stock levels

### MealExecution

* Completed meals
* Execution timestamps

### MealHistory

* Historical meal plans

### WasteHistory

* Spoilage records
* Waste scores

### Receipts

* Purchase history

---

## Qdrant Vector Database

Stores:

* Recipe embeddings
* Semantic recipe metadata
* Retrieval payloads

Used for:

* Similarity search
* Context retrieval
* Recipe recommendation

---

# 🔄 Workflow

## Meal Plan Generation

```text
User Input
    │
    ▼
Coordinator Agent
    │
    ▼
Inventory Agent
    │
    ▼
Waste Agent
    │
    ▼
Recipe Retrieval Agent
    │
    ▼
Meal Planner Agent
    │
    ▼
Budget Agent
    │
    ▼
Reflection Agent
    │
 PASS/FAIL
    │
    ▼
Reporting Agent
    │
    ▼
Final Meal Plan
```

---

## Meal Completion Flow

```text
User Completes Meal
        │
        ▼
Inventory Update
        │
        ▼
Ingredient Deduction
        │
        ▼
Database Update
        │
        ▼
Agent Trace Update
```

---

# 📡 API Endpoints

## Meal Planning

### Generate Plan

```http
POST /api/plan/generate
```

### Get Day Plan

```http
GET /api/plan/day/{id}
```

### Get Agent Trace

```http
GET /api/plan/trace
```

---

## Inventory

### Get Inventory

```http
GET /api/inventory
```

### Complete Meal

```http
POST /api/plan/complete-meal
```

---

## Receipts

### Add Receipt

```http
POST /api/receipts
```

### Pantry Items

```http
GET /api/receipts/pantry
```

### Receipt Inventory

```http
GET /api/receipts/inventory
```

---

# 🖥 Technology Stack

## Frontend

* React
* Vite
* JavaScript
* Lucide React

---

## Backend

* Python
* FastAPI
* Uvicorn
* LangGraph

---

## AI Stack

* Google Gemini 2.5 Flash
* Gemini Embeddings
* Retrieval-Augmented Generation

---

## Databases

* SQLite
* Qdrant

---

# ⚙ Installation

## Clone Repository

```bash
git clone <repository-url>
cd AGENTRIX26-TEAM39-Neural-Surge
```

---

## Backend Setup

```bash
cd homeos/backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create:

```text
.env
```

Add:

```env
GOOGLE_API_KEY=your_key_here
GROQ_API_KEY=your_groq_key
```

Run:

```bash
uvicorn app:app --reload --env-file .env
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd homeos/frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🧪 Verification

Run:

```bash
python verify_ai.py
```

Verifies:

* Gemini connectivity
* Embedding generation
* Qdrant access
* Database initialization
* Agent workflow readiness

---

# 🏆 Agentrix 2026 Alignment

HomeOS demonstrates the core Agentrix evaluation patterns:

### Multi-Agent Collaboration

Multiple specialized agents working together.

### Tool Usage

SQLite, Qdrant, APIs, and inventory tools.

### Reflection Pattern

Independent plan auditing.

### Self-Correction

Automatic re-planning loop.

### Retrieval-Augmented Generation

Semantic recipe retrieval.

### Explainability

Full decision tracing and reporting.

### Real-World Impact

Food waste reduction and household economic optimization.

---

# 👥 Team

**Agentrix 2026**

**Team 39 – Neural Surge**

---

# 📄 License

Educational and Competition Use Only.
