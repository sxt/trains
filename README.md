trains
======

Train Predictor

Requires certain environment variables:

wwwroot: location on file system of document root for HTML 
mbta_host: host name for MBTA API server (developer.mbta.com)
mq_host: host name for Iron MQ API server (mq-aws-us-east-1.iron.io)
mq_path: path for Iron MQ "get messages" API URI. Includes oauth info: 
   /1/projects/${projectId}/queues/train/messages?oauth=${oauthToken}
