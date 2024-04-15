from flask_appbuilder import IndexView


class AppIndexView(IndexView):
    """
    The AppIndexView class is a subclass of the IndexView class and is used for rendering the index page of the app.

    Attributes:
        index_template (str): The template file to use for rendering the index page.

    """
    index_template = 'index.html'
