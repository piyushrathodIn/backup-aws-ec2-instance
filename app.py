import boto3
import collections
import datetime
from pprint import pprint

ec = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['auto_snapshot', 'true']},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print ("Found %d instances that need backing up" % len(instances))

    to_tag = collections.defaultdict(list)

    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 3

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print ("Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId']))

            snap = ec.create_snapshot(
                VolumeId=vol_id,
            )

            to_tag[retention_days].append(snap['SnapshotId'])
            
            for tags in instance['Tags']:
                if tags["Key"] == 'Name':
                    instancename = tags["Value"]

            print("Retaining snapshot {0} of volume {1} from instance {2} for {3} days for {4}".format(
                snap['SnapshotId'],
                vol_id,
                instance['InstanceId'],
                retention_days,
                instancename
            ))
            delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
            delete_fmt = delete_date.strftime('%Y-%m-%d')
            print("Will delete {0} snapshots on {1}".format(len(to_tag[retention_days]), delete_fmt))
            print("instance id now ")
            ec.create_tags( Resources=[snap['SnapshotId']],Tags=[
                            {'Key': 'DeleteOn', 'Value': delete_fmt},
                            {'Key': 'Name', 'Value': instancename},
                            {'Key': 'Instance ID', 'Value': instance['InstanceId']}
            ])

