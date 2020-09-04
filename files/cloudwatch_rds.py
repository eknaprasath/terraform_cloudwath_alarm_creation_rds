import boto3
import json
import os

client = boto3.client('rds')
ec2_types = boto3.client('ec2')  
ec2 = boto3.resource('ec2')
cw = boto3.client('cloudwatch')


rds_sns = os.environ['sns_arn']
cpu_threshold =  os.environ['cw_cpu_threshold']
memory_threshold =  os.environ['cw_memory_threshold']
disk_threshold =  os.environ['cw_disk_threshold']
number_of_connections = os.environ['cw_number_of_connections']

def lambda_handler(event, context):
   # print("Received event: " + json.dumps(event, indent=2))
    rds_name = event['detail']['requestParameters']['dBInstanceIdentifier']
    disk_size = event['detail']['requestParameters']['allocatedStorage']
    dbinstanceclass = event['detail']['requestParameters']['dBInstanceClass']
    type = dbinstanceclass[:3]
    if type == 'db.':
        db_instance_type = dbinstanceclass[3:]
    else:
        db_instance_type = dbinstanceclass
    
    print(db_instance_type)
    
    instance_mem_size = ec2_types.describe_instance_types(
    DryRun=False,
    InstanceTypes=[db_instance_type],
      )  
    # print(instance_mem_size) 
    db_instance_mem = instance_mem_size['InstanceTypes'][0]
    # print(db_instance_mem)
    instance_mem = db_instance_mem['MemoryInfo']['SizeInMiB']
    print(instance_mem)
    avail_mem = 100 - int(memory_threshold)
    percent = (instance_mem*avail_mem)/100 
    print(percent)

    cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " Freeable Memory below " +str(avail_mem) + "%",
    AlarmDescription='Freeable Memory ',
    ActionsEnabled=True,
    AlarmActions=[rds_sns,],
    MetricName='FreeableMemory',
    Namespace='AWS/RDS',
    Statistic='Average',
    Dimensions=[ {'Name': "DBInstanceIdentifier",'Value': rds_name},],
    Period=300,
    EvaluationPeriods=1,
    Threshold=float(percent),
    ComparisonOperator='LessThanOrEqualToThreshold')

    avail_disk = 100 - int(disk_threshold)
    disk_percent = (disk_size*avail_disk)/100

    cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " Available Disk below " +str(avail_disk) + "%",
    AlarmDescription='Freeable Memory ',
    ActionsEnabled=True,
    AlarmActions=[rds_sns,],
    MetricName='FreeStorageSpace',
    Namespace='AWS/RDS',
    Statistic='Average',
    Dimensions=[ {'Name': "DBInstanceIdentifier",'Value': rds_name},],
    Period=300,
    EvaluationPeriods=1,
    Threshold=float(disk_percent),
    ComparisonOperator='LessThanOrEqualToThreshold')

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

    cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " number of connection above "+(number_of_connections),
    AlarmDescription='Number of DB connection',
    ActionsEnabled=True,
    AlarmActions=[rds_sns],
    MetricName='DatabaseConnections',
    Namespace='AWS/RDS',
    Statistic='Average',
    Dimensions=[ {'Name': "DBInstanceIdentifier",'Value': rds_name},],
    Period=300,
    EvaluationPeriods=1,
    Threshold=float(number_of_connections),
    ComparisonOperator='GreaterThanOrEqualToThreshold')