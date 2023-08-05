import time, os, sched

schedule = sched.scheduler(time.time, time.sleep)

def perform_command(cmd, inc):
  os.system(cmd)
  print("task")


def timming_exe(cmd,inc=10):
  schedule.enter(inc, 0, perform_command,(cmd,inc))
  schedule.run()

print("2s--->")
timming_exe("date", 2)
