from selenium import webdriver

browser = webdriver.Firefox(executable_path='/Applications/Firefox.app/Contents/MacOS/firefox')
browser.get('http://localhost:8000')

assert 'Django' in browser.title
