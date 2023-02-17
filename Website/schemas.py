class BookSchema:
    def __init__(self, book):
        self.title=book.title
        self.authors=','.join([str(author) for author in book.authors])
        self.available=book.available
        self.user=book.user
        