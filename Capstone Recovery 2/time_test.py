from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%m/%d/%Y_%H:%M:%S")
print(dt_string)
