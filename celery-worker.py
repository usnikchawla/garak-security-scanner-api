from celery import Celery
from api.models import Session, Scan
import garak
from garak import probes, detectors
import boto3
import json
from config.config import Config

celery = Celery('garak_worker', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def run_garak_scan(scan_id, model_id, probe_names, detector_names, prompt):
    session = Session()
    scan = session.query(Scan).get(scan_id)

    garak_config = garak.Config()
    garak_config.probes = [getattr(probes, probe)() for probe in probe_names]
    garak_config.detectors = [getattr(detectors, detector)() for detector in detector_names]

    client = boto3.client('bedrock-runtime', region_name=Config.AWS_REGION)
    garak_config.model = garak.models.BedrockModel(
        model_id,
        client=client
    )

    run = garak.Run(garak_config)
    results = run.start(prompts=[prompt])

    scan.status = 'completed'
    scan.results = json.dumps(results.to_dict())
    session.commit()
    session.close()

if __name__ == '__main__':
    celery.start()
