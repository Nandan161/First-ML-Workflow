import json

THRESHOLD = 0.7

def lambda_handler(event, context):
    # `event["inferences"]` is already a list
    inferences = event["inferences"]

    # Check if any value is above threshold
    meets_threshold = any(float(value) > THRESHOLD for value in inferences)
    
    if meets_threshold:
        # Good prediction
        return event
    else:
        # Raise an error to fail the Step Function
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
