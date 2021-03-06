#! /usr/bin/env python

from collections import defaultdict
import os

from fabric.api import run, env, sudo, task, runs_once, roles
from utils import instances, use
from cloudflare_utils import instances as cf_instances

env.nodes = []
env.roledefs = defaultdict(list)

@task
def all():
    "All nodes"
    for node in instances():
        use(node)
    for node in cf_instances():
        use(node)

@task
def cloudflare(exp='.*'):
    for node in cf_instances(exp):
        use(node)

@task
def ec2(exp='.*'):
    for node in instances(exp):
        use(node)

@task
def preview():
    "Preview nodes"
    for node in instances('preview-.*'):
        use(node)
    for node in cf_instances('preview-.*'):
        use(node)

@task
def production():
    "Production nodes"
    for node in instances('production-.*'):
        use(node)
    for node in cf_instances('production-.*'):
        use(node)

@task
def nodes(exp):
    "Select nodes based on a regular expression"
    for node in instances(exp):
        use(node)
    for node in cf_instances(exp):
        use(node)

@task
@runs_once
def list():
    "List EC2 name and public and private ip address"
    for node in env.nodes:
        print "%s (%s, %s)" % (node.tags["Name"], node.ip_address,
            node.private_ip_address)

@task
def uptime():
    "Show uptime and load"
    run('uptime')

@task
def free():
    "Show memory stats"
    run('free')

@task
def updates():
    "Show package counts needing updates"
    run("cat /var/lib/update-notifier/updates-available")

@task
def upgrade():
    "Upgrade packages with apt-get"
    sudo("apt-get update; apt-get upgrade -y")

