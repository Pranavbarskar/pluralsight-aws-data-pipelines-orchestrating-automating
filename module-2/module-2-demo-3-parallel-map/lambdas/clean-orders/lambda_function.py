import json, datetime, logging
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _logkv(**kw): logger.info(json.dumps(kw, default=str))

def _norm(e: Any) -> Dict[str, Any]:
    if isinstance(e, dict): return e
    if isinstance(e, (bytes, bytearray)):
        try: return json.loads(e.decode("utf-8"))
        except: return {"_raw": str(e)}
    if isinstance(e, str):
        try: return json.loads(e)
        except: return {"_raw": e}
    return {} if e is None else {"_raw": str(e)}

def lambda_handler(event, context):
    e = _norm(event)
    dataset = e.get("dataset")
    _logkv(stage="start", fn="clean-orders", dataset=dataset, req=context.aws_request_id, input=e)
    if e.get("fail_clean") is True:
        reason = "CleanOrders demo failure"
        _logkv(stage="error", fn="clean-orders", dataset=dataset, reason=reason)
        raise Exception(reason)
    result = {"dataset": dataset, "cleaned_at": datetime.datetime.utcnow().isoformat(), "status": "cleaned"}
    _logkv(stage="result", fn="clean-orders", result=result)
    return result
