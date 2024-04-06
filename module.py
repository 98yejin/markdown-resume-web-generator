import os
import markdown2


def get_summary_content(filename):
    """
    Extracts the content of the 'Summary' section from a markdown file,
    excluding the title and continuing until the next section title.

    :param filename: Path to the markdown file.
    :return: The content under the 'Summary' section, excluding the title.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        capture = False
        content = []
        for line in lines:
            if line.startswith("# Summary"):
                capture = True
                continue
            if capture and line.startswith("#"):
                break
            if capture:
                content.append(line)

        # Join captured content into a single string, and strip to remove leading/trailing whitespace
        return "".join(content).strip()
    except FileNotFoundError:
        return "The specified file was not found."


def find_title_from_filename(filename):
    return filename.split("-", 1)[1].rsplit(".", 1)[0]


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def text_to_markdown(text):
    return markdown2.markdown(text)


def read_markdown(filepath, root="content"):
    fullpath = os.path.join(root, filepath)
    return text_to_markdown(read_file(fullpath))


def summary_under_direcoty(dirpath):
    summaries = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                summary = get_summary_content(filename=filepath)
                html_content = text_to_markdown(summary)
                summaries.append(
                    {
                        "file": file[:-3],
                        "title": find_title_from_filename(file),
                        "content": html_content,
                    }
                )
    return summaries
