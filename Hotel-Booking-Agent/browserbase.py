import os 
from crewai.tools import tool 
from playwright.sync_api import sync_playwright 
from html2text import html2text 
from time import sleep 

@tool("Browserbase tool")
def browserbase_tool(url: str):
    """
    Loads a URL using a headless webbrowser 
    :param url: The URL to load 
    :return: The text content of the page
    """ 
    
    with sync_playwright() as playwright: 
        browser = playwright.chromium.connect_over_cdp(
            "wss://connect.browserbase.com?apiKey=" + os.environ["BROWSERBASE_API_KEY"]
        )

        context = browser.contexts[0]

        #This line picks the first tab in that context.
        page = context.pages[0]

        #Tells Playwright to navigate that tab to the given url.
        page.goto(url)


        #It just freezes the script for 25 seconds before moving on.
        sleep(25)

        #converts that HTML into plain text / Markdown-ish text (so you can read it, search it, or feed it into an LLM).
        content = html2text(page.content())
        
        #Shuts down the remote Browserbase Chromium session.
        browser.close()
        
        
        return content 