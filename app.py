import requests
import csv
from bs4 import BeautifulSoup
from flask import Flask, request, send_file, jsonify, send_from_directory, render_template
import os.path

app = Flask(__name__)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route("/scrape", methods=["POST"])
def scrape():
    print("inside fetch")
    # Send a GET request to the webpage and get its content
    url = request.json["link"]
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the comments in the webpage
    comment_block = soup.find_all('div', {'class': 'MessageView lia-message-view-forum-message lia-message-view-display lia-row-standard-unread lia-thread-reply'})
    # Open a CSV file for writing
    with open('comments.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row to the CSV file
        writer.writerow(['ID', 'User Name', 'Comment'])
        print(comment_block)
        # Loop through each comment and write it to the CSV file
        for i, content in enumerate(comment_block):
            print(i)
            username_element = content.find('div', {'class': 'lia-message-author-with-avatar'})
            if username_element.find('span', {'class': 'login-bold'}): # These are Autodesk Product Support 
                user_name = username_element.find('span', {'class': 'login-bold'}).text.strip()
            else:
                user_name = username_element.find('span',{'class': ''}).text.strip() # These are users
            print(user_name)

            comment_text = ''
            paragraphs = content.find_all('p')
            for paragraph in paragraphs:
                comment_text = paragraph.text.strip() + ''
            print(user_name, comment_text)
            writer.writerow([i+1, user_name, comment_text])

    with open("comments.csv", "r", newline="", encoding="utf-8") as f:
        csv_data = f.read()
        return csv_data

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

if __name__ == "__main__":
    app.run(debug=True)