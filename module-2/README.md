# Module 2 — Orchestrating with AWS Step Functions

This repository contains all demo source code and setup instructions for **Module 2 of the course “AWS Data Pipelines: Orchestrating and Automating.”**  
Each demo builds incrementally to show how AWS Step Functions and related services handle orchestration, retries, fan-out, and integration with other managed tools like Amazon MWAA.

---

## 📁 Folder Structure

```
module-2/
├── demo-3-linear/
│   ├── lambdas/
│   │   ├── ps-clean-orders-lambda/
│   │   └── ps-summarize-report-lambda/
│   ├── statemachine/
│   │   └── ps-linear-pipeline-demo.asl.json
│   └── README.md
│
├── demo-4-retry-catch/
│   ├── lambdas/
│   │   ├── ps-clean-orders-lambda/
│   │   └── ps-summarize-report-lambda/
│   ├── statemachine/
│   │   └── ps-retry-catch-demo.asl.json
│   └── README.md
│
├── demo-6-parallel-map/
│   ├── lambdas/
│   │   ├── generate-datasets/
│   │   ├── clean-orders/
│   │   ├── summarize-report/
│   │   └── emit-execution-summary/
│   ├── statemachine/
│   │   └── ps-parallel-map-demo.asl.json
│   └── README.md
│
└── demo-8-mwaa-console-tour/
    └── README.md
```

---

## 🧩 Demo Summaries

### **Demo 3 — Linear Pipeline with Step Functions**
**Goal:** Build a simple linear pipeline that cleans and summarizes data in sequence.  
**Key Concepts:**
- Task chaining with `ResultPath`
- Controlled execution order
- Predictable outputs for downstream systems  
**AWS Services:** Step Functions | Lambda | CloudWatch Logs  

**Runtime Tip:** Start execution with `{ "source": "demo.run" }`.  
Review state transitions in the Step Functions console and verify each Lambda log stream.

---

### **Demo 4 — Add Retry and Catch**
**Goal:** Show automatic recovery from transient errors.  
**Key Concepts:**
- Using `Retry` for transient failures  
- Using `Catch` to capture unrecoverable states  
- Logging failure paths and error reasons  
**AWS Services:** Step Functions | Lambda | CloudWatch Logs  

**Validation:** Trigger one run with `fail_summary: true` to show retry and catch behavior in the execution graph.

---

### **Demo 6 — Parallel and Map Workflow**
**Goal:** Demonstrate fan-out processing and aggregation of results.  
**Key Concepts:**
- Parallel branches and Map iteration  
- Joining results safely with `ResultPath`  
- Emitting summary outputs to S3  
**AWS Services:** Step Functions | Lambda | S3 | CloudWatch Logs  

**Validation Flow:**
1. Run execution with empty `{}` input.  
2. Observe parallel branches (Clean → Summarize).  
3. Verify emitted JSON summary file in `ps-demo-quicksight-logs-<ACCOUNT_ID>/executions/…`.

---

### **Demo 8 — Amazon MWAA Console Tour**
**Goal:** Show how Managed Workflows for Apache Airflow complements Step Functions for DAG-based orchestration.  
**Key Concepts:**
- MWAA environment structure  
- DAGs folder mapping to S3  
- CloudWatch logging integration  
- Comparison to Step Functions orchestration  
**AWS Services:** MWAA | S3 | CloudWatch  

**On-Screen Flow:**
1. MWAA Console → *Create environment* wizard (walkthrough only)  
2. Explain each configuration group: S3 bucket, networking, monitoring, IAM.  
3. (Optional) Open Airflow UI to show DAGs and retry logs.

---

## ⚙️ Environment and Costs
- **Region:** `us-east-1`
- **Runtime:** Python 3.13 for all Lambda functions
- **IAM:** One role per Lambda; execution policies scoped to least privilege.
- **Cleanup:** Keep all resources for the duration of the course; delete after Module 5 final teardown.

Each demo is designed for a **free-tier or minimal-cost** AWS setup. Only the S3 emitter and MWAA environment may incur small storage or compute charges.

---

## 🧠 Learning Path Connection
| Concept | Demonstrated In |
|----------|----------------|
| Sequential orchestration | Demo 3 |
| Resilient execution with retries | Demo 4 |
| Parallel + fan-out + aggregation | Demo 6 |
| Managed DAG orchestration | Demo 8 |

Together these four demos complete the orchestration pattern coverage promised in the Module 2 learning objectives.

---

## 📦 How to Run Locally (Optional)
You can test Lambdas using the AWS Console or CLI:

```bash
aws lambda invoke --function-name ps-clean-orders-lambda out.json
```

All state-machine definitions are compatible with the **Amazon States Language (ASL)** format and can be imported directly into the Step Functions console.

---

*This repository accompanies the recorded demos for Pluralsight’s “AWS Data Pipelines: Orchestrating and Automating” and should be used solely for educational purposes.*
