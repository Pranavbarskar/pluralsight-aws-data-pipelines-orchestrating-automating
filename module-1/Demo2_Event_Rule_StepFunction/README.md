# Demo 2: Event-Driven Workflow with Step Functions

## Objective
Build an event-driven orchestration pipeline that triggers an AWS Step Functions workflow using Amazon EventBridge when an order event occurs.

---

## Steps

1. **Create Step Function**
   - Open AWS Console → Step Functions → Create state machine.
   - Name: `ps-order-workflow`
   - Type: Standard.
   - Paste JSON below:

```json
{
  "Comment": "Process incoming orders",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Pass",
      "Result": {"validation": "ok"},
      "Next": "GenerateReport"
    },
    "GenerateReport": {
      "Type": "Pass",
      "Result": {"report": "completed"},
      "End": true
    }
  }
}
```

   - Allow AWS to create a new role.
   - Create state machine.

2. **Create EventBridge Rule**
   - Navigate to Amazon EventBridge → Rules → Create rule.
   - Name: `ps-order-created-rule`
   - Event pattern:

```json
{
  "source": ["order.api"],
  "detail-type": ["order.created"]
}
```

   - Target: Step Functions → Select `ps-order-workflow`.
   - Leave Retry and DLQ default (disabled for now).
   - Create rule.

3. **Send Test Event**
   - Go to EventBridge → Event bus → Send events.
   - Paste:

```json
{
  "source": "order.api",
  "detail-type": "order.created",
  "detail": {"orderId": "1234", "totalAmount": 599.0}
}
```

   - Click *Send event*.

4. **Verify**
   - Open Step Functions → `ps-order-workflow` → Executions.
   - Confirm successful run and inspect input/output JSON.

---

## Expected Output
Two Pass states run sequentially with success.

---

## Notes
Keep this for next demo. Don’t delete.
