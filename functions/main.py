# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from index import fetch_properties_anomaly
from casafari import SearchParameters
import json

initialize_app()


@https_fn.on_request()
def on_request_anomaly(req: https_fn.Request) -> https_fn.Response:
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
        response=json.dumps(ouliers),
        status=200,
        mimetype="application/json",
    )
