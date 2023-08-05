import lxml.html as lh
import cloudscraper
from decimal import Decimal


class BlockFiRates:
    __RATES_URL = "https://blockfi.com/rates/"
    __XPATH = "//*[@id='gatsby-focus-wrapper']/section[1]/div/div/div/div[2]/table/tbody"

    def get_all_rates(self):
        scraper = cloudscraper.create_scraper()
        html = scraper.get(BlockFiRates.__RATES_URL).content
        doc = lh.fromstring(html)

        i = 1
        end = 0
        rates = []
        while end == 0:
            try:
                tr_elements = doc.xpath(f'{BlockFiRates.__XPATH}/tr[{i}]')
                col = []
                for t in tr_elements[0]:
                    name = t.text_content()
                    col.append(name)
                rates.append({
                    "Currency": col[0],
                    "Amount": self._convert_amount_to_rule(col[1], col[0]),
                    "APY": float(Decimal(col[2].replace("*", "").rstrip("%"))/100)
                })
                i += 1
            except Exception as e:
                end = 1

        return rates

    def _convert_amount_to_rule(self, AMOUNT, CURRENCY):
        amount = AMOUNT.replace(CURRENCY[:CURRENCY.find(" ")], "").replace(",", "").strip()

        if amount.find("-") > 0:
            rule = {
                "condition": "between",
                "minimum": float(amount[:amount.find("-")].strip()),
                "maximum": float(amount[amount.find("-") + 1:].strip())
            }
        elif amount.find(">") == 0:
            rule = {
                "condition": "greater than",
                "amount": float(amount.replace(">", "").strip())
            }

        return rule

    def get_amount(self, CURRENCY):
        rates = self.get_all_rates()

        return [i for i in rates if i["Currency"] == CURRENCY][0]["Amount"]

    def get_apy(self, CURRENCY):
        rates = self.get_all_rates()

        return [i for i in rates if i["Currency"] == CURRENCY][0]["APY"]
