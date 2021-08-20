import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    books_description_path = os.path.join('media', 'books_description.json')

    with open(books_description_path, 'r') as my_file:
        books_description = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(books_description=books_description)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
