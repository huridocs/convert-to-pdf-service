import mimetypes

MIMETYPES = [
    "text/html",
    "text/plain",
    "text/csv",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.oasis.opendocument.text-flat-xml",
    "application/rtf",
    "application/vnd.sun.xml.writer",
    "application/vnd.sun.xml.writer.template",
    "application/pdf",
    "application/vnd.oasis.opendocument.text",
    "application/x-iwork-pages-sffpages",
    "application/epub+zip",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/x-iwork-numbers-sffnumbers",
    "application/x-iwork-keynote-sffkey",
    "application/vnd.ms-powerpoint",
    "application/vnd.oasis.opendocument.presentation",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
]


class FileNotSupported(Exception):
    pass


def check_file_support(filename: str):
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype not in MIMETYPES:
        raise FileNotSupported(f"File not supported for file {filename}")
