import click
from tabulate import tabulate

from .aws import get_instance_detail, get_instance_vpc, get_instances_from_vpc


@click.command()
def info():
    """Get instances from vpc"""
    detail = get_instance_detail()
    vpc = get_instance_vpc(detail["instanceId"], detail["region"])
    instances = get_instances_from_vpc(vpc, detail["region"])

    headers = ["Private IP", "mssh command", "Instance Name"]
    table = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            private_ip_addr = instance['PrivateIpAddress']
            table.append([
                private_ip_addr,
                f'mssh {instance["InstanceId"]} -r {detail["region"]}',
                [inst['Value'] for inst in instance['Tags']
                 if inst['Key'] == 'Name'][0]
            ])
    click.echo(f"Instances from current VPC {vpc}")
    click.echo(tabulate(table, headers, tablefmt="grid"))


if __name__ == '__main__':
    info()
