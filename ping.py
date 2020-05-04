import subprocess
import time
import re
import os

from influxdb import InfluxDBClient 

hosts = os.environ.get('HOSTS_TO_PING').split(',')
ping_interval_seconds = int(os.environ.get('PING_INTERVAL_SECONDS'))
print(hosts)

influxdb = InfluxDBClient(host='influxdb', port=8086, database='internet')

def insert_ping(host, latency):
    influxdb.write_points([{'measurement': "ping", 'tags': {'host': host}, 'fields': {'latency': latency}}])

while True:
    for host in hosts:
        p = subprocess.Popen(['ping', '-q', '-c', '1', '-W', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        output = output.decode("utf-8")
        if p.returncode == 1 and '0 received' in output:
            latency = 0.0
        elif p.returncode == 0 and '1 received' in output:
            latency_pattern = r"rtt min\/avg\/max\/mdev = ([^\/]+)"
            latency = float(re.findall(latency_pattern, output).pop())
        else:
            print(p.returncode)
            print(output)
            raise NotImplementedError('Unknown state')
        print(host, latency)
        insert_ping(host, latency)
    time.sleep(1)
