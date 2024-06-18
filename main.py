from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class HttpTool:
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload

    def make_http_request(self):
        user_agent_array = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        ]

        try:
            chrome_options = Options()
            chrome_options.add_argument("--ignore-ssl-errors=yes")
            chrome_options.add_argument("--ignore-certificate-errors")

            chrome_options.add_argument("ignore-certificate-errors")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disavle-extensions")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--headless=new")  # To run in headless mode
            wd = webdriver.Chrome(options=chrome_options)
            wd.get(self.url)
            elem = wd.find_element(By.XPATH, "/html/body/h1")
            html = wd.execute_script("return arguments[0].innerHTML;", elem)

            return html

        except Exception:
            return None


if __name__ == "__main__":
    url = "https://ab.crapi.mooncake.msk.ru/check_score"
    payload = {"username": "test@test.ru", "password": "!Qaz2wsx"}

    req = HttpTool(url, payload)
    result = req.make_http_request()
    print(result)
