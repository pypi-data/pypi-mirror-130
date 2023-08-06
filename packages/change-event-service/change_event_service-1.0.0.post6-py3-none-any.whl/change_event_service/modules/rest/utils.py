def _render_status_code(s):
    if s == 200:
        return "OK-200"
    elif s == 201:
        return "CREATED-201"
    elif s >= 400:
        return f"EX-{s}"


class ResponseObject:
    def __init__(self, data={}, message=None, status=None, exceptionDetail=None, page={}):
        self.data = data
        self.message = message
        self.statusCode = _render_status_code(status) if status else None
        self.exceptionDetail = exceptionDetail
        self.page = page



class PaginationObject:
    def __init__(self, page, total, total_pages):
        self.page = page
        self.total = total
        self.total_pages = total_pages
