import time
from seleniumbase import Driver

driver = Driver(uc=True)
driver.get("https://nowsecure.nl")
print(driver.title)
time.sleep(3)
driver.quit()
