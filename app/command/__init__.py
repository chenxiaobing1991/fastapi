import schedule


async def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

