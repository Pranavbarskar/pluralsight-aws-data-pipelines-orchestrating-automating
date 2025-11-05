# Demo 3: Hybrid Late-Arriving Data Reconciliation

## Objective
Detect and fix late-arriving records using EventBridge + Step Functions + Lambda. Demonstrates hybrid orchestration combining schedules and event triggers.

---

## Steps

1. **Create Lambda Function**
   - Name: `ps-reconcile-lambda`
   - Runtime: Python 3.13
   - Role: Auto-create with basic permissions.
   - Paste code below:

```python
import json, datetime

def lambda_handler(event, context):
    order = event.get('detail', event)
    order_id = order.get('orderId', 'N/A')
    amount = order.get('amount', 'N/A')
    reason = order.get('reason', 'N/A')
    timestamp = datetime.datetime.utcnow().isoformat()

    print("🔁 Starting late-order reconciliation job")
    print(f"Order ID: {order_id}, Amount: ${amount}, Reason: {reason}")
    print(f"Reconciled at {timestamp}")

    return {"orderId": order_id, "status": "reconciled", "time": timestamp}
```

2. **Create Step Function**
   - Name: `ps-reconcile-workflow`
   - Paste JSON below:

```json
{
  "Comment": "Reconcile late orders",
  "StartAt": "FlagLateOrder",
  "States": {
    "FlagLateOrder": {
      "Type": "Pass",
      "Result": {"flag": "Late order flagged"},
      "ResultPath": "$.flag",
      "Next": "TriggerCorrection"
    },
    "TriggerCorrection": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "ps-reconcile-lambda",
        "Payload.$": "$"
      },
      "End": true
    }
  }
}
```

3. **Create Event Rule**
   - EventBridge → Rules → Create rule.
   - Name: `ps-late-order-rule`.
   - Event pattern:

```json
{
  "source": ["orders.data"],
  "detail-type": ["late.record"]
}
```

   - Target: Step Function → `ps-reconcile-workflow`.
   - Expand Retry/DLQ panel (don’t attach queue, just show location).
   - Create rule.

4. **Publish Test Event**
   - EventBridge → Event bus → Send events.
   - Paste payload:

```json
{
  "source": "orders.data",
  "detail-type": "late.record",
  "detail": {
    "orderId": "A1080",
    "amount": 420.5,
    "reason": "arrived_after_cutoff"
  }
}
```

5. **Verify**
   - Step Functions → Executions → confirm success.
   - Check CloudWatch logs for printed order details.

---

## Notes
- Scheduler triggers regular loads.
- Event rules catch late data.
- Together they ensure real-time accuracy.

---
