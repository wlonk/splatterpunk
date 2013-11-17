from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

try:
    assert 'Splatterpunk' in browser.title
finally:
    browser.quit()
