""" 
This will process the directory generated files by wget
and pull out all the required html files that include
an <article> tab in them. Rename them in a certain way
and store them.
Renaming will be md5(file.html).html
"""
from bs4 import BeautifulSoup
import logging
import os
import sys

# wget -r -nc arynews.tv --include-directories=/en/ --exclude-directories=/en/wp-json

# Check if cwd is writable for logging
if os.access(os.getcwd(), os.W_OK) == False:
	print("Logging can't be set. No write permissions on CWD.\
		Fix it and try again.")
	exit(1)

# If a log already exists, purge it
if os.access(__name__+".log", os.F_OK) == True:
	print("Purging existing log")
	os.remove(__name__+".log")

# Setup logging
logging.basicConfig(
	filename="{}.log".format(__name__),
	level=logging.INFO,
	format='[%(asctime)s: %(levelname)s from %(name)s]: %(message)s')

logger = logging.getLogger(__name__)


def check_dir_readable_exists(dir_name):
	if os.access(dir_name, os.F_OK) and os.access(dir_name, os.R_OK):
		logger.info("{} exists and is readable.".format(dir_name))
	else:
		logger.error("{} doesn't exist or is not readable!".format(dir_name))
		raise Exception("{} doesn't exist or is not readable!".format(dir_name))

wget_dir = ""

# First, try to get it from the ENV_VAR
if os.getenv("WGET_DIR") != None and os.getenv("WGET_DIR") != "":
	wget_dir = os.getenv("WGET_DIR")
	check_dir_readable_exists(wget_dir)
	logger.info("Using env var for wget_dir: {}".format(wget_dir))

# Secondly, try to get it from script arguments
elif len(sys.argv) > 1:

	wget_dir = sys.argv[1]
	check_dir_readable_exists(wget_dir)
	logger.info("Using CLI arg for wget_dir: {}".format(wget_dir))

# Raise exception, that directory wasn't specified
else:
	logger.error("No wget_dir specified!")
	raise Exception("No wget_dir specified!")


def has_article_tag(html_file):
	with open(html_file, "r") as html_file:
		html_data = html_file.read()
		soup = BeautifulSoup(html_data, 'html.parser')
		if soup.find("article"):
			return True


html_files_list = []
number_of_articles = 0

# Look up all the files that have "html" in their name
logger.info("Finding all HTML files...")
for root, dirs, files in os.walk(wget_dir):
	for each_file_name in files:
		if "html" in each_file_name:
			html_files_list.append(os.path.join(root, each_file_name))

logger.info("Read {} HTML files in wget_dir: {}".format(len(html_files_list), wget_dir))
logger.info("Finding article tags in {} files...".format(len(html_files_list)))

with open("article_files_list", "w") as article_files_list:
	with open("non_artile_html_files", "w") as non_article_files_list:
		# Check for article tag in the HTML file
		for each_file in html_files_list:
			if has_article_tag(each_file):
				article_files_list.write(each_file+"\n")
				print("Found an article in: {}".format(each_file))
				number_of_articles += 1
			else:
				non_article_files_list.write(each_file+"\n")
				print("HTML file has no <article> tag!")


logger.info("Found <article> tag in {} HTML files!".format(number_of_articles))
logger.info("No <article> tag in {} HTML files!".format(len(html_files_list)-number_of_articles))