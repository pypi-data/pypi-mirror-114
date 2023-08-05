# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import logging
import re
from pathlib import Path

import click
import markdown
from ebooklib import epub

from txt2ebook import __version__

logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True)
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--title", "-t", default=None, show_default=True, help="Set the title of the ebook."
)
@click.option(
    "--language",
    "-l",
    default="en",
    show_default=True,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    show_default=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value=logging.DEBUG,
    show_default=True,
    help="Enable debugging log.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
def main(filename, title, language, author, debug):
    """
    Console tool to convert txt file to different ebook format.
    """

    logging.basicConfig(level=debug, format="[%(levelname)s] %(message)s")

    try:
        logger.debug("Processing txt file: '%s'.", filename)
        chapters = split_chapters(filename)

        if title:
            output_filename = title + ".epub"
        else:
            output_filename = Path(filename).stem + ".epub"

        build_epub(output_filename, chapters, title, language, author)

    except RuntimeError as error:
        click.echo(f"Error: {str(error)}!", err=True)


def split_chapters(filename):
    """
    Split the content of txt file into chapters by chapter header.
    """

    with open(filename, "r") as file:
        content = file.read()

        if not content:
            raise RuntimeError(f"Empty file content in '{filename}'.")

        pattern = re.compile(r"^第\d+章\s.*$", re.MULTILINE)
        headers = re.findall(pattern, content)

        if not headers:
            raise RuntimeError(f"No chapter headers found in '{filename}'.")

        bodies = re.split(pattern, content)
        chapters = list(zip(headers, bodies[1:]))

    return chapters


def build_epub(output_filename, chapters, title, language, author):
    """
    Generate epub from the parsed chapters from txt file.
    """

    book = epub.EpubBook()

    if title:
        book.set_title(title)

    if language:
        book.set_language(language)

    if author:
        book.add_author(author)

    toc = []
    for chapter_title, body in chapters:
        chapter_title = chapter_title.strip()
        body = body.strip()
        match = re.search(r"第\d+章", chapter_title)
        if match:
            filename = match.group()
        else:
            filename = chapter_title

        logger.debug(chapter_title)
        html_chapter = epub.EpubHtml(title=chapter_title, file_name=filename + ".xhtml")

        chapter = "# " + chapter_title + "\n\n" + body
        html = markdown.markdown(chapter)
        html_chapter.content = html
        book.add_item(html_chapter)
        toc.append(html_chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.toc = toc
    book.spine = ["nav"] + toc

    logger.debug("Generating epub file: '%s'.", output_filename)
    epub.write_epub(output_filename, book, {})


if __name__ == "__main__":
    main()
