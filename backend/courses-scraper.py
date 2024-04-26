import os
import requests
from bs4 import BeautifulSoup
import re
import csv

# URL of the UPenn course catalog
url = "https://catalog.upenn.edu/courses/"

# Make a GET request to the URL and get the response object
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
sitemap_section = soup.find("div", id="textcontainer")

# Find all the headers for the letters of the alphabet A-Z
headers = sitemap_section.find_all("h2", class_="letternav-head")

filename = "data/courses.csv"

# Check if the file already exists
if os.path.exists(filename):
    # If it does, find a new filename by incrementing a counter
    i = 1
    while os.path.exists(f"{filename.split('.')[0]}-{i}.csv"):
        i += 1
    filename = f"{filename.split('.')[0]}-{i}.csv"

# Open the CSV file for writing
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["Department Code", "Course Code", "Course Title", "Description", "ALL"])

    # Iterate over each header and find the corresponding list of departments
    for header in headers:
        # Get the letter of the alphabet for this header
        letter = header.text.strip()
        print(f"Scraping departments starting with letter {letter}...")

        # Find the corresponding list of departments
        department_list = header.find_next_sibling("ul")

        # Iterate over each department and scrape the course titles and descriptions
        for department in department_list.find_all("li"):
            # Get the URL of the department catalog
            catalog_url = "https://catalog.upenn.edu" + department.find("a")["href"]

            # Make a GET request to the catalog URL and get the response object
            catalog_response = requests.get(catalog_url)

            # Parse the HTML content of the catalog using BeautifulSoup
            catalog_soup = BeautifulSoup(catalog_response.content, "html.parser")

            # Find the "textcontainer" div in the catalog page
            text_container = catalog_soup.find("div", id="textcontainer")

            # Find the "sc_sccoursedescs" div inside the text container
            course_descs = text_container.find("div", class_="sc_sccoursedescs")

            if course_descs is None:
                # No courses on this page
                print("=" * 80)
                print(f"Skipping {catalog_url} - no courses found")
                print("=" * 80)
                continue

            # Find all the "courseblock" divs inside the sc_sccoursedescs div
            course_blocks = course_descs.find_all("div", class_="courseblock")

            # Iterate over each course block and extract the title and description
            for course_block in course_blocks:
                # Extract the course title from the "courseblocktitle" div
                title = course_block.find("p", class_="courseblocktitle").text.strip()

                # Split the course title into department code and course title
                match = re.search(r"^([A-Z]+)\s+(\d+)", title)
                if match:
                    dept_code = match.group(1)
                    course_code = match.group(2)
                    course_title = re.sub(r"^([A-Z]+)\s+(\d+)\s+", "", title)
                else:
                    dept_code = ""
                    course_code = ""
                    course_title = title

                # Extract the course description from the "courseblockextra" divs
                desc = "\n".join([d.text.strip() for d in course_block.find_all("p", class_="courseblockextra")])
                all_details = f"{dept_code} {course_code}: {course_title}, {desc}"
                writer.writerow([dept_code, course_code, course_title, desc, all_details])

                # Print the course department and code, course title, and description
                print(f"Department code: {dept_code}")
                print(f"Course code: {course_code}")
                print(f"Course title: {course_title}")
                print(f"Description: {desc}")
                print("=" * 80)


