ML WorkFlow

Overview

This project demonstrates a serverless, event-driven image classification workflow using AWS services. It classifies delivery vehicles (bicycles vs. motorcycles) to optimize loading-bay assignments. Key components:

Data Preparation & Training: A Jupyter notebook ingests CIFAR‑100, filters for bicycle/motorcycle images, and trains a SageMaker image classification model.

SageMaker Endpoint: Deployed model endpoint for on-demand inference.

Lambda Functions (3):

serialize_image.py – Downloads an image from S3 and base64‑encodes it.

classify_image.py – Calls the SageMaker endpoint to get class probabilities.

filter_inference.py – Checks if the highest confidence exceeds a threshold and either passes or fails.

Step Function: Orchestrates the three Lambdas in sequence, passing image data through.

S3 Storage: Holds train/ and test/ images and manifests, and captured data from Model Monitor.

Repository Structure

project/
├── README.md                   # This file
├── notebooks/                  # Data staging & model training
│   └── etl_and_training.ipynb
├── lambdas/                    # Lambda function source code
│   ├── serialize_image.py
│   ├── classify_image.py
│   └── filter_inference.py
├── step_function/              # State machine definition & test inputs
│   ├── state_machine.json
│   └── sample_input.json
├── screenshots/                # Console proof (Lambda, StepFn, S3)
│   ├── lambda_creation.png
│   ├── stepfn_success.png
│   └── s3_test_image.png

Setup Instructions

Prerequisites

AWS account with permissions for S3, SageMaker, Lambda, Step Functions, IAM.

AWS CLI configured or permissions in SageMaker Studio.

Python 3.8+ environment (for the notebook).

Dependencies

If running locally:

pip install -r requirements.txt
# requirements.txt can include: boto3, pandas, matplotlib, numpy, sagemaker, jsonlines

Running the Notebook

Launch etl_and_training.ipynb in SageMaker Studio (kernel: Python 3 Data Science).

Run cells to extract CIFAR‑100, filter images, save to train/ & test/.

Sync to your S3 bucket and train the image classification model.

Deploy the model to an endpoint.

Deploying Lambda Functions

Create three AWS Lambda functions (serialize_image, classify_image, filter_inference) using the code in lambdas/.

Ensure each Lambda has an IAM role with:

S3 read (s3:GetObject) for serialize_image.

SageMaker invoke (sagemaker:InvokeEndpoint) for classify_image.

CloudWatch logging for all.

Deploy your code, setting the handler to lambda_function.lambda_handler.

Step Function Setup

In the AWS Step Functions console, choose Author from scratch.

Import step_function/state_machine.json as the workflow definition.

Assign an IAM role that can invoke your Lambdas (states:InvokeFunction).

Start an execution with step_function/sample_input.json.

Testing

Verify each Step Function run succeeds (see screenshots/stepfn_success.png).

Use different sample_input.json keys (e.g. bicycle vs. motorcycle) to test both outcomes.

Inspect output JSON to confirm inferences and decision logic.

Cleanup

To avoid ongoing charges:

# Delete SageMaker endpoint & model
aws sagemaker delete-endpoint --endpoint-name <endpoint-name>
# Delete Lambda functions
aws lambda delete-function --function-name serialize_image
aws lambda delete-function --function-name classify_image
aws lambda delete-function --function-name filter_inference
# Delete Step Function
aws stepfunctions delete-state-machine --state-machine-arn <arn>
# Empty S3 bucket
aws s3 rm s3://<your-bucket> --recursive

Screenshots

Lambda Creation: screenshots/lambda_creation.png

Step Function Success: screenshots/stepfn_success.png

S3 Test Image: screenshots/s3_test_image.png