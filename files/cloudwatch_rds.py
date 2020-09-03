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
    rds_name = event['detail']['SourceIdentifier']
    print(rds_name)
    rdsevent = event['detail']['Message']
    print(rdsevent)
    if rdsevent == "DB instance created":
        get_intance_type = client.describe_db_instances(
        DBInstanceIdentifier=rds_name,
        MaxRecords=20,
        Marker='string'
        )
        db_instance_type = get_intance_type['DBInstances'][0]
        instance_type = db_instance_type['DBInstanceClass']
        disk_size = db_instance_type['AllocatedStorage']
        
        type = instance_type[:3]
        if type == 'db.':
            db_instance_type_1 = instance_type[3:]
        else:
            db_instance_type_1 = instance_type
        
        print(db_instance_type_1)
        
        instance_mem_size = ec2_types.describe_instance_types(
          DryRun=False,
          InstanceTypes=[db_instance_type_1],
          )  
        # print(instance_mem_size) 
        db_instance_mem = instance_mem_size['InstanceTypes'][0]
        # print(db_instance_mem)
        instance_mem = db_instance_mem['MemoryInfo']['SizeInMiB']
        print(instance_mem)
        avail_mem = 100 - int(memory_threshold)
        percent = (instance_mem*avail_mem)/100 
        print(percent)
        
        cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " Freeable Memory below " +(memory_threshold) + "%",
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

        cw.put_metric_alarm(AlarmName = "RDS "+(rds_name) + " Available Disk below " +(disk_threshold) + "%",
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