from datetime import datetime

now = datetime.now()

print(int(now))
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)