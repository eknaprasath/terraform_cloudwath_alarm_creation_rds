
import boto3
import json
import os

cw = boto3.client('cloudwatch')
rds_sns = os.environ['sns_arn']
cpu_threshold =  os.environ['cw_cpu_threshold']
rds_number_of_connections = os.environ['cw_number_of_connections']

def lambda_handler(event, context):
  #  print("Received event: " + json.dumps(event, indent=2))
    rds_name = event['detail']['SourceIdentifier']
   # print(rds_name)
    rdsevent = event['detail']['Message']
   # print(rdsevent)
    if rdsevent == "DB instance created":
        print('New DB instance created, creating cloudwatch alarm')   
        cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " CPU utilization above " +(cpu_threshold) + "%",
        AlarmDescription='CPU Utilization ',
        ActionsEnabled=True,
        AlarmActions=[rds_sns,],
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[ {'Name': "DBInstanceIdentifier",'Value': rds_name},],
        Period=300,
        EvaluationPeriods=1,
        Threshold=float(cpu_threshold),
        ComparisonOperator='GreaterThanOrEqualToThreshold')
        cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " number of connection above "+(rds_number_of_connections),
        AlarmDescription='Number of DB connection',
        ActionsEnabled=True,
        AlarmActions=[rds_sns],
        MetricName='DatabaseConnections',
        Namespace='AWS/RDS',
        Statistic='Average',
        Dimensions=[ {'Name': "DBInstanceIdentifier",'Value': rds_name},],
        Period=300,
        EvaluationPeriods=1,
        Threshold=float(rds_number_of_connections),
        ComparisonOperator='GreaterThanOrEqualToThreshold')