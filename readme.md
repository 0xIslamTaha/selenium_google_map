# 🔥🔥 Selenium google map
A fully E2E page-object test suite that tests the basic functionality of the google map search engine.

## 🔑 Testing Stack:
![testing stack](testing_stack.png)
- Python
- Selenium
- Docker
- Github Action

## 👌 Design pattern:
It follows the page-object design pattern

## 🎬 Execution script:
As I dockerized all the requirements in a customized image, You don't have to do anything but execute the following one line command to fire the test suite.
```bash
docker container run -t -v /dev/shm:/dev/shm -v $(pwd):/google-map -e "PYTHONPATH='$PYTHONPATH:/google-map" -w /google-map 0xislamtaha/seleniumchromenose:83 bash -c "nosetests -vs --nologcapture --tc-file=config.ini --tc=browser.headless:True tests"
```

## 👌The structure:
```bash
.
├── config.ini
├── lib
│   ├── __init__.py
│   ├── page_objects
│   │   ├── __init__.py
│   │   ├── locators.yml
│   │   ├── page.py
│   │   └── search_map_page.py
│   └── selenium_plus.py
└── tests
    ├── base_tests.py
    └── test_search_map_page.py
```

## Execution results:
[Here](https://github.com/0xIslamTaha/selenium_google_map/actions) is the latest execution results based on the Github Action.
