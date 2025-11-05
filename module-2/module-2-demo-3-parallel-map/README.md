# Demo 6 — Parallel and Map Workflow

**Clip goal (5 min):** Branch and iterate tasks, join results safely, and inspect the execution graph while emitting one summary JSON per run.

## Folder structure
- lambdas/
  - generate-datasets/lambda_function.py
  - clean-orders/lambda_function.py
  - summarize-report/lambda_function.py
  - emit-execution-summary/lambda_function.py
- statemachine/
  - ps-parallel-map-demo.asl.json

## Prereqs
- Region: `<REGION>` (course uses us-east-1)
- Account: `<ACCOUNT_ID>`
- Bucket: create `ps-demo-quicksight-logs-<ACCOUNT_ID>` in the same region

## 1) Create Lambdas (Python 3.13 for all)
1. `ps-generate-datasets-lambda` → paste `lambdas/generate-datasets/lambda_function.py` → **Deploy**.
2. `ps-clean-orders-lambda` → paste `lambdas/clean-orders/lambda_function.py` → **Deploy**.
3. `ps-summarize-report-lambda` → paste `lambdas/summarize-report/lambda_function.py` → **Deploy**.
4. `ps-emit-execution-summary-lambda` → paste `lambdas/emit-execution-summary/lambda_function.py` → **Deploy**.
   - Timeout: **120 seconds**
   - Environment:
     - `QS_BUCKET = ps-demo-quicksight-logs-<ACCOUNT_ID>`
     - `QS_PREFIX = executions/`
   - Role policy (inline) to allow writes under the prefix:
     - Service: S3
     - Actions: PutObject, PutObjectAcl
     - Resource: the bucket's `executions/*` path

## 2) Create the State Machine
- Name: `ps-parallel-map-demo` (Standard)
- Paste `statemachine/ps-parallel-map-demo.asl.json`
- Replace `<ACCOUNT_ID>` and `<REGION>`
- **Create**

## 3) Record Success Run
- Start execution with `{}`
- Show Map item:
  - CleanOrders output: dataset + cleaned status + timestamp
  - SummarizeReport output: completed + records 120
- Show fan-in: Parallel green → Reshape → Emitter green
- Show Emitter output (s3_key), then open the JSON in the bucket: execution id, itemCount=3, items for north, west, online

## 4) Logs Insights (validation)
- Log groups:
  - `/aws/lambda/ps-summarize-report-lambda`
  - `/aws/lambda/ps-emit-execution-summary-lambda`

**Summaries per dataset**
```
fields @timestamp, fn, stage, dataset, summary.summary_status, summary.records
| filter fn = "summarize-report"
| sort @timestamp asc
```

**Emitter confirmation**
```
fields @timestamp, fn, stage, s3_key, itemCount
| filter fn = "emit-execution-summary"
| sort @timestamp desc
| limit 10
```

## 5) Record Partial Failure Run (optional)
- Edit generator to include `"error"` in the list
- In summarizer, the code already raises when dataset equals `error`
- Run again:
  - One iteration turns red in SummarizeReport
  - Parallel fails overall; Emitter is skipped

## Notes
- Map uses **ItemSelector** to turn each list item into `{ "dataset": "<name>" }` before the iterator.
- Each task uses **ResultPath** to avoid field collisions.
- Reshape gathers Map items, audit info, and execution metadata for the emitter.
