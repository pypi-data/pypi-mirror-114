import z 
import cron



#z.out(cron.doc)
def work():
   z.out("test----------------")
   z.out("job done! If not stop, please press [ctrl + c] => exit")


cron.execute_circularly(work, interval="1s")

