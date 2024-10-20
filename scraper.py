# scraper.py

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import config

# Initialize Selenium WebDriver
def init_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Fetch and parse the video webpage
def get_video_links(url):
    driver = init_driver()
    driver.get(url)

    # Wait for videos to load (modify as per site structure)
    driver.implicitly_wait(5)

    # Example: Get all video links from the page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    video_elements = soup.find_all("video")

    # Extract video sources (Modify according to site's structure)
    video_links = [video.get("src") for video in video_elements]

    driver.quit()
    return video_links

# Download videos from the scraped URLs
def download_videos(video_links):
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.makedirs(config.DOWNLOAD_PATH)

    for index, link in enumerate(video_links):
        try:
            video_data = requests.get(link, stream=True)
            file_name = os.path.join(config.DOWNLOAD_PATH, f"video_{index + 1}.mp4")

            # Save the video to a file
            with open(file_name, "wb") as video_file:
                for chunk in video_data.iter_content(chunk_size=1024):
                    if chunk:
                        video_file.write(chunk)

            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    video_links = get_video_links(config.VIDEO_SITE_URL)
    if video_links:
        print(f"Found {len(video_links)} video(s). Starting download...")
        download_videos(video_links)
    else:
        print("No videos found.")
