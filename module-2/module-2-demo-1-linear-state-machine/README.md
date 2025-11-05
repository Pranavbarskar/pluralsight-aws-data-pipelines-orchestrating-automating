# Module 2 – Demo: Build a Linear State Machine

**Account:** xxxxxxx850
**Region:** us-east-1
**Runtime:** Python 3.13
**Goal:** Orchestrate two Lambdas with AWS Step Functions in a linear flow; prove success and controlled failures; verify in CloudWatch.

---

## 1) Create Lambda: ps-clean-orders-lambda
Console: AWS Lambda → **Create function**
- Name: `ps-clean-orders-lambda`
- Runtime: Python 3.13
- Arch: x86_64
- Permissions: Create a new role with basic Lambda permissions
- Create

Code: paste `lambdas/ps-clean-orders-lambda/lambda_function.py` and **Deploy**.

Quick test: run with `{}` and confirm success. Log groups will be created under `/aws/lambda/ps-clean-orders-lambda`.

**Behavior**
- Logs structured JSON for `stage=start` and `stage=result`.
- If input contains `{ "fail_clean": true }`, logs `stage=error` and raises an exception.

---

## 2) Create Lambda: ps-summarize-report-lambda
Console: AWS Lambda → **Create function**
- Name: `ps-summarize-report-lambda`
- Runtime: Python 3.13
- Arch: x86_64
- Permissions: Create a new role with basic Lambda permissions
- Create

Code: paste `lambdas/ps-summarize-report-lambda/lambda_function.py` and **Deploy**.

Quick test: run with `{}` and confirm success. Log group `/aws/lambda/ps-summarize-report-lambda` is created.

**Behavior**
- Structured logs for `stage=start` and `stage=result`.
- If input contains `{ "fail_summary": true }`, logs `stage=error` and raises an exception.

---

## 3) Create State Machine: ps-linear-pipeline-demo
Console: AWS Step Functions → **Create state machine**
- Type: **Standard**
- Name: `ps-linear-pipeline-demo`
- Author with code → paste `stepfunctions/ps-linear-pipeline-demo/definition.json`

**Definition key points**
- `StartAt`: `CleanOrders`
- `CleanOrders` (Task) → `ResultPath: "$.clean"`
- `SummarizeReport` (Task) uses **Parameters** to pass just:
  - `clean.$`: `$.clean`
  - `fail_summary.$`: `$.fail_summary`
- `ResultPath: "$.summary"`
- `NotifySuccess` (Pass) with `End: true`

**IAM**
- Let the console create the role automatically.
- If needed, attach an inline policy like `iam/stepfunctions-invoke-lambdas-policy.json` to allow `lambda:InvokeFunction` on both Lambdas.

---

## 4) Run Executions

### Success
Start execution with:
```json
{ "source": "demo.run" }
```
Expected:
- Graph: CleanOrders → SummarizeReport → NotifySuccess (all green)
- Output object contains `clean`, `summary`, and message
- Click each state node to view inputs/outputs in the right panel

### Fail CleanOrders
Start:
```json
{ "source": "demo.run", "fail_clean": true }
```
Expected:
- CleanOrders fails (red); downstream states do not run
- Details pane shows exception; CloudWatch log shows `stage=error`

### Fail SummarizeReport
Start:
```json
{ "source": "demo.run", "fail_summary": true }
```
Expected:
- CleanOrders succeeds; SummarizeReport fails (red)
- Details pane shows exception; CloudWatch log shows `stage=error`

---

## 5) CloudWatch verification

Open CloudWatch Logs → Log groups:
- `/aws/lambda/ps-clean-orders-lambda`
- `/aws/lambda/ps-summarize-report-lambda`

**Logs Insights – structured lines**
```sql
fields @timestamp, fn, stage, result, summary, reason
| filter ispresent(stage)
| sort @timestamp desc
| limit 20
```

**Errors only**
```sql
fields @timestamp, fn, stage, reason, @message
| filter stage = "error"
| sort @timestamp desc
| limit 20
```

---

## 6) Best practices captured
- Log as data: one compact JSON per phase (`start`, `error`, `result`)
- Keep Lambda outputs minimal and stable for orchestration
- Use `Parameters` to pass only what the task needs; avoid `InputPath` flag loss
- End workflows explicitly (`End: true`) for clean traces and alerting
- Use UTC timestamps for consistent auditing

---
