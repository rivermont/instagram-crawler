#!/var/usr/env python3

from selenium.common import exceptions
from selenium import webdriver
# import json
import time


def get_time():
    """Used for logging."""
    return time.strftime("%H:%M:%S")


login_user = "r1vermont"
login_pass = "aIanbsctdaegfrgahm"

start_profile = "r1vermont"  # Your Instagram profile, or the profile the bot should start crawling at.
max_depth = 4  # The number of profiles the bot should go past the initial page.

url = "https://instagram.com/"

browser = webdriver.Firefox()  # Initialize Selenium driver
start_url = url + start_profile

browser.get(url + 'accounts/login')

time.sleep(2)

# Select login form elements
login_form_user = browser.find_element_by_xpath(
    '/html/body/span/section/main/div/article/div/div[1]/div/form/div[1]/div/input')
login_form_pass = browser.find_element_by_xpath(
    '/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/input')
login_form_button = browser.find_element_by_xpath(
    '/html/body/span/section/main/div/article/div/div[1]/div/form/span/button')

# Fill in login information and submit
login_form_user.send_keys(login_user)
login_form_pass.send_keys(login_pass)
login_form_button.click()

time.sleep(4)

# Verify that bot is logged in, exit if is not
# try:
#     assert True
#     # assert <something>
# except AssertionError:
#     browser.quit()
#     raise AssertionError(
#         "Browser could not log in to Instagram. Please double-check that your login information is correct.")

del login_user, login_pass
del login_form_user, login_form_pass, login_form_button

print('Successfully logged in.')


def crawl_profile(profile):
    global priority_level, todo, done

    print('[{0}] Crawling {1}'.format(priority_level, profile))

    browser.get(url + profile)

    # TODO: Scrape data and save to json

    try:
        followers_link = browser.find_element_by_xpath('/html/body/span/section/main/article/header/section/ul/li[2]/a')
        following_link = browser.find_element_by_xpath('/html/body/span/section/main/article/header/section/ul/li[3]/a')
    except exceptions.NoSuchElementException:
        print('Found private account: {0}'.format(profile))
        return None

    followers_link.click()  # Click on Followers link
    all_followers = browser.find_elements_by_class_name("_6e4x5")

    for f in all_followers:
        try:
            browser.execute_script("return arguments[0].scrollIntoView();", f)
            text = f.find_element_by_xpath('.//div/div[1]/div/div[1]/a').text
            todo.get(priority_level + 1).append(text)
        except exceptions.WebDriverException as e:
            print(e)

    close_button = browser.find_element_by_xpath('/html/body/div[4]/div/button')
    close_button.click()

    following_link.click()
    all_following = browser.find_elements_by_class_name('_6e4x5')

    for f in all_following:
        try:
            browser.execute_script("return arguments[0].scrollIntoView();", f)
            text = f.find_element_by_xpath('.//div/div[1]/div/div[1]/a').text
            todo.get(priority_level + 1).append(text)
        except exceptions.WebDriverException as e:
            print(e)

    todo[priority_level + 1] = list(set(todo[priority_level + 1]))

    done.add(profile)


priority_level = 0
done = set([])

todo = {x: list() for x in range(max_depth)}

todo.get(0).append(start_profile)

print('Beginning crawl.')

while priority_level <= max_depth:
    while len(todo[priority_level]) != 0:
        print('Depth level: {0}'.format(priority_level))
        for i in todo[priority_level]:
            if i not in done:
                crawl_profile(i)
            todo.get(priority_level).remove(i)
        priority_level += 1

print('Done.')

#   - Different connection styles for Following/Follower - arrows?
#   - Download profile pic in image:base64 and display as bubble.
#   - Bubble size based on relative follower count? (Sized by category - 10, 100, 1k, etc.)
