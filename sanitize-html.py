# This script will take a raw HTML page as input and sanitize it to extract only
# meaningful information. The information we desire out of a news article is:
# 1- Date of publication
# 2- Author
# 3- Title
# 4- All the paragraphs
#
# Everything else, for the time being, will be ignored
# All this information, for ARY News, is available in the <article> tag of the
# index.html page. Need to extract that.
from bs4 import BeautifulSoup
import os

html_file_paths = []
for root, dirs, files in os.walk("/home/p4wn3r/test/arynews.tv/en/"):
	for name in files:
		if name == "index.html":
			html_file_paths.append(os.path.join(root, name))

# Count number of articles processed successfully
success_count = 0
total_count = 0
for each_file in html_file_paths:
	html_page = open(each_file, "r")
	page_content = html_page.read()
	html_page.close()
	total_count += 1

	soup = BeautifulSoup(page_content, 'html.parser')
	article = soup.find("article")
	try:
		# Extract image URL
		try:
			article_image_url = article.find("img")["data-src"]
		except (TypeError, KeyError):
			article_image_url = "No Image Available"
		finally:
			# print("Article Image at: {}".format(article_image_url))
			pass
		
		# Extract the article publication dates
		article_dates = []
		for each_time in article.find_all("time"):
			article_dates.append(each_time.get_text())
		# print("Article Dates: ", end="")
		# print(article_dates)

		# Extract the article author
		article_author = article.find("a", rel="author").get_text()
		# print("Article Author: ", end="")
		# print(article_author)

		# Extract the article title
		article_title = article.find("span", itemprop="headline").get_text()
		# print("Article Title: ", end="")
		# print(article_title)

		# Extract the article paragraphs
		article_text = ""
		for each_paragraph in article.find_all("p"):

			# ignore the comments and Read More paragraphs
			if "comments" in each_paragraph.get_text():
				continue
			elif "Read More:" in each_paragraph.get_text():
				continue
			else:
				article_text += each_paragraph.get_text() + "\n"
		# print("\nArticle Text: ")
		# print("*="*100)
		# print(article_text)
		# print("*="*100)
		print("An article was processed successfully!")
		success_count += 1
		print("Successfully processed articles: {}".format(success_count))
		print("Total articles: {}".format(total_count))

	except AttributeError:
		print("Parser doesn't work for this page!")
