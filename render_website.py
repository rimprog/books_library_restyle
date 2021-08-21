import os
import json
from functools import partial

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload(env, books_description_chunks_per_pages):
    template = env.get_template('template.html')

    pages_count = len(books_description_chunks_per_pages)

    for page_index, books_description_chunks in enumerate(books_description_chunks_per_pages, 1):
        rendered_page = template.render(
            books_description_chunks=books_description_chunks,
            pages_count=pages_count,
            current_page_number = page_index
        )

        pages_folder_name = 'pages'
        page_name = f'index{page_index}.html'
        file_path = os.path.join(pages_folder_name, page_name)

        os.makedirs(pages_folder_name, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(rendered_page)


def main():
    books_description_path = os.path.join('media', 'books_description.json')

    with open(books_description_path, 'r') as my_file:
        books_description = json.load(my_file)

    books_description_chunks = list(chunked(books_description, 2))
    books_description_chunks_per_pages = list(chunked(books_description_chunks, 10))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    on_reload_with_args = partial(on_reload, env, books_description_chunks_per_pages)
    on_reload_with_args()

    server = Server()
    server.watch('template.html', on_reload_with_args)
    server.serve(root='.')


if __name__ == '__main__':
    main()
