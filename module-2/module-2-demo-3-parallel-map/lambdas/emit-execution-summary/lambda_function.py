import json
import os
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.getenv("QS_BUCKET", "ps-demo-quicksight-logs-605024711850")
S3_PREFIX = os.getenv("QS_PREFIX", "executions/")


def _logkv(**kw):
    logger.info(json.dumps(kw, default=str))


def lambda_handler(event, context):
    # Always log first so Logs Insights can see the run
    input_keys = list(event.keys()) if isinstance(event, dict) else "not_dict"
    _logkv(stage="start", fn="emit-execution-summary", input_preview=input_keys)

    # Create the client only now (avoids module-import failures)
    try:
        import boto3  # safe on Python 3.11

        s3 = boto3.client("s3")
    except Exception as e:
        _logkv(
            stage="error",
            fn="emit-execution-summary",
            reason=f"boto3/client init failed: {e}",
        )
        raise

    results = event.get("results", {}) if isinstance(event, dict) else {}
    items = results.get("map", {}).get("items", [])
    exec_arn = results.get("execution", {}).get("arn")
    started = results.get("execution", {}).get("startTime")

    doc = {
        "executionArn": exec_arn,
        "startTime": started,
        "itemCount": len(items),
        "items": [
            {
                "dataset": i.get("summary", {}).get("dataset"),
                "records": i.get("summary", {}).get("records"),
                "status": i.get("summary", {}).get("summary_status"),
            }
            for i in items
        ],
        "emittedAt": datetime.datetime.utcnow().isoformat(),
    }

    body = json.dumps(doc) + "\n"
    date_prefix = datetime.datetime.utcnow().strftime("%Y/%m/%d")
    key = f"{S3_PREFIX}{date_prefix}/exec={context.aws_request_id}.json"

    try:
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body.encode("utf-8"))
    except Exception as e:
        _logkv(
            stage="error",
            fn="emit-execution-summary",
            reason=f"S3 put_object failed: {e}",
        )
        raise

    _logkv(
        stage="result", fn="emit-execution-summary", s3_key=key, itemCount=len(items)
    )
    return {"s3_key": key, "written": True}
