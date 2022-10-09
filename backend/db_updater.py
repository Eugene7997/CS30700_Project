import schedule
import time


def update_db():
    print("hello")


def generate_placeholder_data():
    regions = ['north america', 'south america', 'europe', 'africa', 'asia', 'oceania']
    eas = ['temperature', 'earthquake frequency', 'rainfall', 'climate']
    for region in regions:
        


schedule.every(1).minutes.do(update_db)

while True:
    schedule.run_pending()
    time.sleep(1)