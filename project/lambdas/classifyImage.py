import json
import base64
import boto3

# Create a SageMaker runtime client
runtime = boto3.client('sagemaker-runtime')

ENDPOINT = "image-classification-2025-04-28-16-12-53-457"

def lambda_handler(event, context):
    # Decode the incoming image
    image = base64.b64decode(event["image_data"])
    
    # Invoke the SageMaker endpoint
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType="image/png",
        Body=image
    )
    
    # Parse the inference result
    inferences = json.loads(response['Body'].read().decode('utf-8'))
    
    # Add the inferences to the event for the next step
    event["inferences"] = inferences
    
    return event
