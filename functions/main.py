# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from numpy import Infinity
from index import fetch_properties_anomaly
from casafari import SearchParameters
import json

initialize_app()

class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        obj = self.prepare(obj)
        return super(CustomJSONEncoder, self).encode(obj)

    def prepare(self, obj):
        if isinstance(obj, float):
            if obj == float('inf'):
                return "Infinity"
            elif obj == float('-inf'):
                return "-Infinity"
            elif obj != obj:  # Checks for NaN
                return "NaN"
        elif isinstance(obj, list):
            return [self.prepare(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.prepare(value) for key, value in obj.items()}
        return obj

@https_fn.on_request(timeout_sec=300, memory=options.MemoryOption.MB_512, region="europe-west3")
def on_request_anomaly_v2(req: https_fn.Request) -> https_fn.Response:
    # POST request
    if req.method != "POST":
        return https_fn.Response("Hello world!")
    parameters = req.get_json()
    try:
        parameters = SearchParameters(**parameters)
        ouliers = fetch_properties_anomaly(parameters)
    except Exception as e:
        return https_fn.Response(
            response=json.dumps({"error": str(e)}),
            status=400,
            mimetype="application/json",
        )
    # return outliers as json
    return https_fn.Response(
        response=json.dumps({"properties": ouliers}, cls=CustomJSONEncoder),
        status=200,
        mimetype="application/json",
        content_type="application/json"
    )
