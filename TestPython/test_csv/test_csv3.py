__author__ = 'R.Azh'
import csv, datetime
data = [{}]
start_time = datetime.datetime.utcnow()
with open('/tmp/ports.csv', 'w') as f:  # 'r+'
        writer = csv.DictWriter(f, sorted(c.first()))
        writer.writeheader()
        for port in c.iterator():
            writer.writerow(port)
print(datetime.datetime.utcnow()-start_time)

                        
