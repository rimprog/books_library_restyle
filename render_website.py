import os
import json
from functools import partial

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload(env, books_description_chunks):
    template = env.get_template('template.html')
    rendered_page = template.render(books_description_chunks=books_description_chunks)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)


def main():
    books_description_path = os.path.join('media', 'books_description.json')

    with open(books_description_path, 'r') as my_file:
        books_description = json.load(my_file)

    books_description_chunks = list(chunked(books_description, 2))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    on_reload_with_args = partial(on_reload, env, books_description_chunks)
    on_reload_with_args()

    server = Server()
    server.watch('template.html', on_reload_with_args)
    server.serve(root='.')


if __name__ == '__main__':
    main()
