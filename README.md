# ReadMe

Python script that makes an ebook in the `.epub` format out of the articles under the title "[_Building Products Using Data_](https://articles.sequoiacap.com/building-products-using-data)" on Sequoia Capital's website.

I do not provided the e-book itself, only the script to create it on your own.

# Context 

In 2018/2019, Sequoia Capital published a series of articles on the topic of product analytics with around 30 different articles.

I like to read long texts on an e-ink reader and decided to make a small ebook out of the articles.

This is what the Python script does:
- It create a table of contents at the beginning of the book,
- It preserves the images included in the articles and places them in the right place,
- It formats all of the above into a simple ebook and saves it on disk in the `output/` folder.

This script is hyper-specific to this article series and cannot be re-used for any other article without being modified beforehand. It does the job, but it isn't the most elegant or robust Python code you will see.

# How to use

1. You need to both files `get_urls.py` and `run_this.py`.
1. `get_urls.py` will fetch all the URLs of the articles under "[_Building Products Using Data_](https://articles.sequoiacap.com/building-products-using-data)". One of the articles ("[_Analyzing Metric Changes_](https://articles.sequoiacap.com/analyzing-metric-changes)" also includes its own list of sub-articles and it will fetch them too.
   - Install the libraries required `requests` and `bs4`
1. `run_this.py` is the script that you need to run.
    - Install the additional libraries required: `html`, `ebooklib`.
    - Run the script
  
# Results

<img width="238" height="324" alt="image" src="https://github.com/user-attachments/assets/ddd57a1f-f675-4ba4-babb-01c1840c08a2" />
<img width="1136" height="880" alt="images-script-ebook-1" src="https://github.com/user-attachments/assets/0f007701-6390-4087-83b0-9ac33aeaea0e" />
<img width="1136" height="880" alt="images-script-ebook-2" src="https://github.com/user-attachments/assets/7e71eeb4-362b-49d4-864c-a675f834bffa" />
<img width="1136" height="880" alt="images-script-ebook-3" src="https://github.com/user-attachments/assets/d09a9306-404c-4a9c-a1e5-f47edf2c8114" />
