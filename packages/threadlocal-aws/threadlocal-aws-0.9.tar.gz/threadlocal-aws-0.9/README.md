# Threadlocal AWS clients and resources

Convinient access to threadlocal boto3 clients and resources.

## Usage

### Resource
```
from threadlocal_aws.resources import ec2

for instance in ec2().instances.all():
     print(instance.id)
```

### Client

```
from threadlocal_aws.clients import ec2

instance = ec2().describe_instances(InstanceIds=["i-0fd31cg97d77ddfff"])
```
