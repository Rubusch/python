# Selenium

Some first steps with selenium.  

## References
https://selenium-python.readthedocs.io/

## Preparations

install selenium  
```
$ pip install selenium
```

install a webdriver, according to your browser  

| browser | webdriver                                     |
|---------|-----------------------------------------------|
| Chrome: | https://sites.google.com/chromium.org/driver/ |
| Edge:   | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Firefox:| https://github.com/mozilla/geckodriver/releases |
| Safari: | https://webkit.org/blog/6900/webdriver-support-in-safari-10/ |

e.g. for firefox under debian/ubuntu  
```
$ sudo apt install -y firefox-geckodriver chromium-chromiumdriver
```

NB: chromium is better installed by snap (future)  

## Issues

issue: error when running the demo with name seleniumply  
```
$ python3 ./selenium.py
    Traceback (most recent call last):
      File "./selenium.py", line 1, in <module>
          from selenium import webdriver
    ...
    cannot import name 'webdriver' from partially initialized module 'selenium' (most likely due to a circular import)
    ...
```
fix: never call a file "selenium.py" when importing a "selenium" package :)  
