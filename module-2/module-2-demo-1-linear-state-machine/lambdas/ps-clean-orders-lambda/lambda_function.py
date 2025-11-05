import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _logkv(**kw):
    logger.info(json.dumps(kw, default=str))

def lambda_handler(event, context):
    _logkv(stage="start", fn="clean-orders",
           request_id=context.aws_request_id, event=event)

    # Failure injection for demos/tests
    if event.get("fail_clean") is True:
        _logkv(stage="error", fn="clean-orders",
               reason="Simulated failure in CleanOrders: bad input shape")
        raise Exception("Simulated failure in CleanOrders: bad input shape")

    result = {
        "cleaned_at": datetime.datetime.utcnow().isoformat(),
        "status": "cleaned"
    }

    _logkv(stage="result", fn="clean-orders", result=result)
    return result
