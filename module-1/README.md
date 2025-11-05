# Module 1 — Foundations of Data Pipeline Orchestration

This module introduces the fundamentals of orchestration in modern AWS data pipelines.  
You’ll learn why timing alone isn’t enough, how orchestration prevents silent failures, and how AWS services connect to form dependable workflows.

---

## 🎯 Learning Objectives

- Understand the difference between scheduling and orchestration  
- Identify orchestration components in AWS (EventBridge, Step Functions, Lambda, S3)  
- Build a baseline event-driven workflow using Step Functions and Amazon EventBridge  

---

## 🧩 Module Structure

| Folder                                    | Purpose                                                                               |
| ----------------------------------------- | ------------------------------------------------------------------------------------- |
| **Demo1_Scheduler_Lambda**                | Create a simple Lambda-based scheduler to trigger pipeline tasks                      |
| **Demo2_Event_Rule_StepFunction**         | Use Amazon EventBridge to trigger AWS Step Functions based on custom rules            |
| **Demo3_Hybrid_Late_Data_Reconciliation** | Handle delayed data arrival with a hybrid Step Function–based reconciliation pipeline |

---

## 🧪 Demos

### Demo 1 — Scheduler Lambda
- Use AWS Lambda and Amazon CloudWatch Events to trigger jobs on a schedule  
- Demonstrates the move from *time-based jobs* to *event-triggered orchestration*  

### Demo 2 — Event Rule + Step Function
- Build an EventBridge rule that invokes a Step Function when an upstream event occurs  
- Logs workflow progress in Amazon CloudWatch  

### Demo 3 — Hybrid Late Data Reconciliation
- Combine scheduled and event-based triggers for late-arriving data  
- Validate data freshness and reconcile missing records  

---

## 🧱 AWS Resources Used

| Service                | Purpose                             |
| ---------------------- | ----------------------------------- |
| **AWS Lambda**         | Custom job runner and scheduler     |
| **Amazon EventBridge** | Central event bus for orchestration |
| **AWS Step Functions** | Workflow engine and state control   |
| **Amazon S3**          | Data source and target for jobs     |
| **Amazon CloudWatch**  | Logs, metrics, and alerting         |

---

## 🧰 Environment

- **Account ID:** `081448897918`  
- **Region:** `us-east-1`  
- Use IAM roles with least privilege (Lambda execution, Step Functions invoke, S3 read/write)  
- Clean up all resources after testing to avoid costs  

---

## ⚙️ Expected Outcomes

By the end of this module, you will:
- Recognize orchestration as a control plane for pipelines  
- Deploy your first Step Functions workflow  
- Understand event-driven triggers and recovery patterns  

---

## 🧾 Authoring Notes

- Slides follow **Pluralsight Keynote 2025.02.a** template  
- All demos include **setup → execution → failure → recovery → teardown** steps  
- Scripts are written in **Python 3.12** and **AWS CLI v2**  
- Narration uses the **WHY → WHAT → HOW** format  

---

**Author:** Rupesh Tiwari  
© Pluralsight 2025 — For educational use only.
