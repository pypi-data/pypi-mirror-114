from urllib.parse import quote
from json import JSONDecodeError

import requests
from fire import Fire
from cloudscraper import (
    CloudScraper,
    CloudflareIUAMError,
    CloudflareCaptchaError,
    CloudflareChallengeError,
    CloudflareSolveError
)


RED = "\u001b[31;1m"
GREEN = "\u001b[32;1m"
WHITE = "\u001b[37;1m"


class HIBPy(object):
    def search(self, email: str):
        try:
            scraper = CloudScraper()
            headers = {
                "Accept": "*/*",
                "Referer": "https://haveibeenpwned.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.164 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = scraper.get(f"https://haveibeenpwned.com/unifiedsearch/{quote(email)}", headers=headers)

            if response.status_code == 404:
                print(f"{WHITE}[{GREEN}INFO{WHITE}] Good news — You have not been pwned!")
            elif response.text.__contains__("Breaches"):
                json = response.json()

                print(f"{WHITE}[{RED}INFO{WHITE}] You have been pwned :(")

                try:
                    for breach in json["Breaches"]:
                        print(f"{WHITE}[{RED}BREACH{WHITE}] {breach['Name']} - {breach['BreachDate']}")
                except TypeError:
                    pass

                try:
                    for paste in json["Pastes"]:
                        print(f"{WHITE}[{RED}PASTE{WHITE}] {paste['Title']} - {paste['Source']} - {paste['Date']}")
                except TypeError:
                    pass
            else:
                print(f"{WHITE}[{RED}ERROR{WHITE}] Unexpected response. Status Code: {response.status_code}")
        except requests.RequestException:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Requests Error")
        except CloudflareIUAMError:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Cloudflare IUAM Error")
        except CloudflareCaptchaError:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Cloudflare Captcha Error")
        except CloudflareChallengeError:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Cloudflare Challange Error")
        except CloudflareSolveError:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Cloudflare Solve Error")
        except JSONDecodeError:
            print(f"{WHITE}[{RED}ERROR{WHITE}] Error decoding JSON response.")


if __name__ == '__main__':
    Fire(HIBPy())
