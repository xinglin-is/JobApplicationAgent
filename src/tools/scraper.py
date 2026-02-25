import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def scrape_job_url(url: str) -> str:
    """
    Scrapes the text content from a given job posting URL.
    Returns the cleaned text containing the job description.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error scraping URL: {e}"

if __name__ == "__main__":
    # Test simple scrape
    test_url = "https://example.com"
    print(scrape_job_url.invoke({"url": test_url}))
