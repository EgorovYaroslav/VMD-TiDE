from crontab import CronTab
cron = CronTab(user='user')

cron.remove_all()
cron.write()

job = cron.new(command='cd /home/user/Work/F107 && python3 regular_job.py')
job.minute.every(1)
job7 = cron.new(command='cd /home/user/Work/F107 && python3 regular_job_7.py')
job7.hour.every(12)
job27 = cron.new(command='cd /home/user/Work/F107 && python3 regular_job_27.py')
job27.hour.every(12)
screenshot = cron.new(command='cd /home/user/Work/F107 && python3 regular_screenshot.py')
screenshot.hour.every(23)
# srh = cron.new(command='cd /home/user/Work/SRH && python3 regular_prediction.py')
# srh.hour.every(12)

cron.write()