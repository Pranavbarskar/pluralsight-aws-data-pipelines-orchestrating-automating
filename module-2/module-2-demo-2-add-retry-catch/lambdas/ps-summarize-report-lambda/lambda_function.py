import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _logkv(**kw):
    logger.info(json.dumps(kw, default=str))

def lambda_handler(event, context):
    _logkv(stage="start", fn="summarize-report",
           request_id=context.aws_request_id, input=event)

    attempt = int(event.get("attempt", 0))
    transient_cutoff = int(event.get("transient_until_attempt", 0))

    if attempt < transient_cutoff:
        _logkv(stage="error", fn="summarize-report",
               reason=f"Transient error on attempt {attempt}")
        raise RuntimeError(f"Transient error on attempt {attempt}")

    if event.get("fail_summary") is True:
        _logkv(stage="error", fn="summarize-report",
               reason="Permanent failure in SummarizeReport")
        raise Exception("Permanent failure in SummarizeReport")

    summary = {"summary_status": "completed", "records": 120, "attempt": attempt}
    _logkv(stage="result", fn="summarize-report", summary=summary)
    return summary
