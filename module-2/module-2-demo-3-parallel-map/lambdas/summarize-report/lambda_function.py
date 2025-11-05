import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _logkv(**kw):
    logger.info(json.dumps(kw, default=str))


def lambda_handler(event, context):
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except:
            event = {"_raw": event}

    dataset = event.get("dataset")
    _logkv(
        stage="start",
        fn="summarize-report",
        dataset=dataset,
        req=context.aws_request_id,
        input=event,
    )

    # Enable this block only for the partial-failure recording
    if dataset == "error":
        _logkv(
            stage="error",
            fn="summarize-report",
            dataset=dataset,
            reason="Simulated failure",
        )
        raise Exception("Simulated failure in SummarizeReport")

    if event.get("fail_summary") is True:
        reason = f"Permanent failure in SummarizeReport for {dataset}"
        _logkv(stage="error", fn="summarize-report", dataset=dataset, reason=reason)
        raise Exception(reason)

    summary = {
        "dataset": dataset,
        "summary_status": "completed",
        "records": 120,
        "attempt": 0,
    }
    _logkv(stage="result", fn="summarize-report", summary=summary)
    return summary
