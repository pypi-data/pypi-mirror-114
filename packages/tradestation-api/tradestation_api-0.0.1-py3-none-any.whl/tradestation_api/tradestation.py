from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
import random
import os
import pyotp

class TradeStation:
    __instance = None
    def __init__(self, **kwargs):
        """
            The TradeStation class. Used to interact with schwab.
            Expected arguments:
                username -- the TradeStation username,
                password -- the schwab password,
                user_agent -- the user agent we're using to scrape,
        """
        if TradeStation.__instance is None:
            TradeStation.__instance = self
        else:
            raise Exception("Only one TradeStation instance is allowed")

        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.user_agent = kwargs.get("user_agent", None)
        self.totp = kwargs.get("totp", None)
        self.user_data_dir = kwargs.get("user_data_dir", "user_data_dir")

        if self.username is None or self.password is None or self.user_agent is None or self.totp is None:
            raise Exception("TradeStation expects the following constructor variables: `username`, `password`, `user_agent`, `totp`")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            slow_mo= random.randint(100,300),
            headless=True,
            timeout=15*1000
        )

    @staticmethod
    def get_instance(**kwargs):
        """The TradeStation class. Used to interact with Charles TradeStation. 
            This is a singleton class to prevent issues from arising 
            with playwright
        Parameters
        ----------
        username: TradeStation username
        password: TradeStation password
        user_agent: The user agent to spoof using Playwright. This needs to be something
            recent and up-to-date. TradeStation doesn't allow logins from super old browsers.
        user_data_dir: The directory location of where to save persistent authentication 
            data. Defaults to `user_data_dir`
        **kwargs
            Parameters that are passed on to basically every module and methods
            that interact with this main class. These may or may not be documented
            in other places.
        """
        if not TradeStation.__instance:
            TradeStation(**kwargs)
        return TradeStation.__instance

    def __del__(self):
        try:
            self.context.close()
        except:
            pass
        try:
            self.playwright.stop()
        except:
            pass


    def login(self, screenshot=False):
        """
            Logs into TradeStation using the initialized username and password.
            Will save an auth.json that holds cookies/auth information which we might use later.
            screenshot (Bool) - Whether to screenshot after logging in
        """
        self.context = self.browser.new_context(
            user_agent=self.user_agent,
            viewport={ 'width': 1920, 'height': 1080 }
        )
        # Open new page
        self.page = self.context.new_page()
        stealth_sync(self.page)

        print("Attempting to login")
        # Go to https://webtrading.tradestation.com/
        self.page.goto("https://webtrading.tradestation.com/")
        self.page.wait_for_load_state('networkidle')

        username = self.page.query_selector("[placeholder=\"username\"]")

        if not username:
            print("Already logged in!")
            return

        # Click [placeholder="username"]
        self.page.click("[placeholder=\"username\"]")
        # Fill [placeholder="username"]
        self.page.fill("[placeholder=\"username\"]", self.username)
        # Press Tab
        self.page.press("[placeholder=\"username\"]", "Tab")
        # Fill [placeholder="password"]
        self.page.fill("[placeholder=\"password\"]", self.password)
        # Click text=Log in
        # with page.expect_navigation

        with self.page.expect_navigation():
            self.page.click("text=Log in")

        # Check if we need to do two factor authentication

        # Click [aria-label="Enter your one-time code"]
        self.page.click("[aria-label=\"Enter your one-time code\"]")
        # Click [aria-label="Enter your one-time code"]
        self.page.click("[aria-label=\"Enter your one-time code\"]")

        totp = pyotp.TOTP(self.totp)
        # Fill [aria-label="Enter your one-time code"]
        self.page.fill("[aria-label=\"Enter your one-time code\"]", totp.now())
        print("Using OTP code: " + totp.now())

        # Click text=Continue
        self.page.click("text=Continue")

        self.page.wait_for_load_state('networkidle')
        self.context.storage_state(path="auth.json")
        print("Login info accepted successfully")

        if screenshot:
            self.page.screenshot(path="Logged_in.png")

    def trade(self, ticker, side, qty, account_index=0, screenshot=False):
        """
            ticker (Str) - The symbol you want to trade,
            side (str) - Either 'Buy' or 'Sell',
            qty (int) - The amount of shares to buy/sell,
            account_index - The index of the account you want to trade on. 
                For example, if you have more than one account, you may want
                to specify which account to perform the trade on. The default is
                0 (the first account). If you're looking to identify the index,
                choose the dropdown on https://client.schwab.com/Areas/Trade/Allinone/index.aspx,
            screenshot (Bool) - Whether to screenshot proof of the trade
        """

        print(f"Attempting to {side} {qty} shares of {ticker} on account #{account_index}")
        self.page.wait_for_load_state('networkidle')
        # Close the annoying container if we have it
        container = self.page.query_selector("[data-testid=\"modalContainer\"] div div")
        if container:
            self.page.click("[data-testid=\"modalContainer\"] div div")
        
        # Click a:has-text("Trade")
        self.page.click("a:has-text(\"Trade\")")
        # assert page.url == "https://webtrading.tradestation.com/#"

        # Click [placeholder="Symbol"]
        self.page.click("[placeholder=\"Symbol\"]")
        # Fill [placeholder="Symbol"]
        self.page.fill("[placeholder=\"Symbol\"]", ticker)

        # Click [placeholder="Quantity"]
        self.page.click("[placeholder=\"Quantity\"]")
        # Fill [placeholder="Quantity"]
        self.page.fill("[placeholder=\"Quantity\"]", str(qty))

        # Choose our account
        self.page.click(".orderbarAccountNumber")

        scroller = self.page.query_selector('[data-test-id="nestedmenu-input-style-availableAccountsByAssetType"]')
        children = scroller.query_selector('.nestedmenu-scroller').query_selector_all('xpath=child::*')
        children[account_index].evaluate("node => node.click()")

        if side.lower() == 'buy':
            self.page.click("text=A:")
            # Click text=Buy
            self.page.click("text=Buy")
        elif side.lower() == 'sell':
            self.page.click("text=B:")
            try:
                # Click text=Sell
                self.page.click("text=Sell", timeout=1*1000)
            except:
                print("Unable to sell, maybe we don't own the stock?")
                self.page.reload(wait_until='networkidle')
                return
        else:
            print("Unclear whether we should buy or sell, doing nothing")
            return

        confirmation = self.page.query_selector("[data-testid=\"okModalButton\"]")
        if confirmation:
            # Click [data-testid="okModalButton"]
            self.page.click("[data-testid=\"okModalButton\"]")
        
        if screenshot:
            print(f"Saving confirmation to {side}-{ticker}-({qty})-account{account_index + 1}.png")
            self.page.screenshot(path=f"screenshots/{side}-{ticker}-({qty})-account{account_index + 1}.png")

        confirmation = self.page.query_selector("[data-testid=\"okModalButton\"]")
        if confirmation is not None:
            # Click [data-testid="cancelModalButton"]
            self.page.click("[data-testid=\"okModalButton\"]")
        self.page.reload(wait_until='networkidle')
        
        print("Looks like we have successfully completed our trade!")