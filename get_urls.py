import requests
from bs4 import BeautifulSoup, Tag

url1 = "https://articles.sequoiacap.com/building-products-using-data"
url2 = "https://articles.sequoiacap.com/analyzing-metric-changes"


def get_all_article_urls_sequoia_data_informed_product_building_pages() -> list[str]:
    def get_all_article_urls_sequoia_one_page(url: str) -> list[str]:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        # Extract content
        article_body: Tag | None = soup.find(
            "div", class_="page-content js-page-holder -home adjusted"
        )
        if not article_body:
            return []

        # Collect link URLs
        urls: list[str] = []
        for a_tag in article_body.find_all("a"):
            href = a_tag.get("href")
            if (
                href
                and isinstance(href, str)
                and href.startswith("https://www.sequoiacap.com/article/")
            ):
                urls.append(href)

        return urls

    list_from_url1 = get_all_article_urls_sequoia_one_page(url1)
    list_from_url2 = get_all_article_urls_sequoia_one_page(url2)

    urls = list_from_url1[:8] + list_from_url2 + list_from_url1[8:]

    return urls


if __name__ == "__main__":
    urls = get_all_article_urls_sequoia_data_informed_product_building_pages()
    for url in urls:
        print(url)
    print(f"Total URLs found: {len(urls)}")
