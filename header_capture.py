import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserDevTools:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--ignore-ssl-errors=yes")
        self.options.add_argument("--ignore-certificate-errors")

        # Enable Performance Logging
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.options.add_argument(
            "--enable-blink-features=NetworkService,NetworkServiceInProcess"
        )

        # Start the WebDriver
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_cdp_cmd("Network.enable", {})

    def open_page(self, url):
        self.driver.get(url)

    def get_network_events(self):
        logs = self.driver.get_log("performance")
        events = [json.loads(entry["message"])["message"] for entry in logs]
        return events

    def extract_headers(self, events):
        requests = []
        responses = []
        for event in events:
            if event["method"] == "Network.requestWillBeSent":
                requests.append(event)
            elif event["method"] == "Network.responseReceived":
                responses.append(event)
        return requests, responses

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    browser = BrowserDevTools(headless=False)
    browser.open_page("https://ab.crapi.mooncake.msk.ru")

    # Fetch network events
    events = browser.get_network_events()
    requests, responses = browser.extract_headers(events)

    print("Requests:")
    for req in requests:
        print(json.dumps(req, indent=2))

    print("\nResponses:")
    for res in responses:
        print(json.dumps(res, indent=2))

    browser.close()
