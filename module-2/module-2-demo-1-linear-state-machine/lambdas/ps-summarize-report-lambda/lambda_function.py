import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _logkv(**kw):
    logger.info(json.dumps(kw, default=str))

def lambda_handler(event, context):
    _logkv(stage="start", fn="summarize-report",
           request_id=context.aws_request_id, input=event)

    # Failure injection for demos/tests
    if event.get("fail_summary") is True:
        _logkv(stage="error", fn="summarize-report",
               reason="Simulated failure in SummarizeReport: Athena throttled")
        raise Exception("Simulated failure in SummarizeReport: Athena throttled")

    summary = {"summary_status": "completed", "records": 120}

    _logkv(stage="result", fn="summarize-report", summary=summary)
    return summary
