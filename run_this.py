import os
import requests
import html
from bs4 import BeautifulSoup
from ebooklib import epub
from get_urls import get_all_article_urls_sequoia_data_informed_product_building_pages


def fetch_and_clean(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        # Extract title from <h1>
        title_tag = soup.find("h1")
        title = html.unescape(title_tag.get_text()) if title_tag else url

        # Extract content from specific div
        article_body = soup.find(
            "div", class_="page-content js-page-holder -home adjusted"
        )
        if not article_body:
            raise ValueError("Could not find article body.")

        # Remove unwanted elements
        for element in article_body(["script", "style", "nav", "footer", "aside"]):
            element.decompose()

        # Fix encoding for all text elements
        for element in article_body.find_all(text=True):
            element.replace_with(html.unescape(str(element)))

        # Collect image URLs and mark their positions
        image_urls = []
        for img in article_body.find_all("img"):
            img_src = img.get("src")
            img_src_str = str(img_src)
            if img_src_str:
                if img_src_str.startswith("//"):
                    img_src_str = "https:" + img_src_str
                image_urls.append(img_src_str)

        # Store the HTML with placeholders for images
        text = str(article_body)

        return {"title": title, "text": text, "image_urls": image_urls, "url": url}
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


def create_epub(articles, output_path="output/Building_Products_using_Data.epub"):
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title("Building Products using Data")
    book.set_language("en")
    book.add_author("Data Science Team – Sequoia Capital")

    toc = []
    chapters = []

    for idx, article in enumerate(articles):
        if not article:
            continue

        soup = BeautifulSoup(article["text"], "lxml")
        image_index = 0

        # Replace each image tag with a reference to the EPUB image
        for img in soup.find_all("img"):
            img_url = article["image_urls"][image_index]
            try:
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
                img_filename = f"image_{idx}_{image_index}.png"
                img_item = epub.EpubImage()
                img_item.file_name = f"images/{img_filename}"
                img_item.content = img_response.content
                book.add_item(img_item)
                img["src"] = f"images/{img_filename}"
                image_index += 1
            except Exception as e:
                print(f"Error processing image {img_url}: {e}")
                img.decompose()

        content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>{article["title"]}</title>
</head>
<body>
    <h1>{article["title"]}</h1>
    <p><em>Source: <a href="{article["url"]}">{article["url"]}</a></em></p>
    {soup}
</body>
</html>
        """

        chapter = epub.EpubHtml(
            title=article["title"], file_name=f"chap_{idx}.xhtml", lang="en"
        )
        chapter.content = content.encode("utf-8")

        book.add_item(chapter)
        chapters.append(chapter)
        toc.append(epub.Link(f"chap_{idx}.xhtml", article["title"], f"chap_{idx}"))

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + chapters

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    epub.write_epub(output_path, book, {})
    print(f"Ebook saved to {output_path}")


def main(urls, output_path="output/Building_Products_using_Data.epub"):
    articles = []
    for url in urls:
        article = fetch_and_clean(url)
        if article:
            articles.append(article)

    if articles:
        create_epub(articles, output_path)
    else:
        print("No articles were processed.")


# Example usage
if __name__ == "__main__":
    urls = get_all_article_urls_sequoia_data_informed_product_building_pages()

    main(urls)
