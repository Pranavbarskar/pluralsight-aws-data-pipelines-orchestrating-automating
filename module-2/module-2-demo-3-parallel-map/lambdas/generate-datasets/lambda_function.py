import json, datetime, logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    datasets = ["north", "west", "online"]
    logger.info(json.dumps({"stage":"result","fn":"generate-datasets","datasets":datasets}))
    return {"datasets": datasets, "generated_at": datetime.datetime.utcnow().isoformat()}
