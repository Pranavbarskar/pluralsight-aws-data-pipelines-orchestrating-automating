# Demo 1: Automate Jobs with Amazon EventBridge Scheduler

## Objective
Create a recurring serverless schedule using Amazon EventBridge Scheduler to trigger an AWS Lambda function every minute. Demonstrates scheduling without relying on cron servers.

---

## Steps

1. **Create Lambda Function**
   - Open AWS Console → Lambda → Create function.
   - Select *Author from scratch*.
   - Name: `ps-scheduler-lambda`
   - Runtime: Python 3.13
   - Role: Create a new role with basic Lambda permissions.
   - Replace the default code with:

```python
import json, datetime

def lambda_handler(event, context):
    result = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "job": "daily-order-refresh",
        "status": "started"
    }
    print(json.dumps(result))
    return result
```

   - Deploy and test using `{}` as payload.

2. **Create EventBridge Scheduler**
   - Open *Amazon EventBridge* → *Schedules* → *Create schedule*.
   - Name: `ps-scheduler-demo`
   - Description: `Hourly order data refresh`
   - Occurrence: Recurring schedule
   - Time zone: (UTC+05:30) Asia/Calcutta
   - Schedule type: Rate-based → `rate(1 minute)`
   - Flexible window: Off
   - Target: AWS Lambda → Select `ps-scheduler-lambda`
   - Execution role: Auto-create
   - Enable schedule and create.

3. **Verify in CloudWatch Logs**
   - Go to *CloudWatch Logs* → `/aws/lambda/ps-scheduler-lambda`
   - Confirm entries appear every minute with correct timestamps.

4. **Cost and Free Tier**
   - First 14M invocations per month are free.
   - Beyond that: $1 per million invocations.

---

## Expected Output
Logs in CloudWatch every minute:

```
{"timestamp": "2025-10-13T10:45:15Z", "job": "daily-order-refresh", "status": "started"}
```

---

## Cleanup
Keep all resources for next demos. Do not delete.
