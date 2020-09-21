from notion.client import NotionClient


class Interpreter():
    def __init__(self, site):
        self.token_v2 = raise(AttributeError("You need to supply your own auth token for notion"))
        self.site = site
        self.client = NotionClient(token_v2=self.token_v2)
        self.page = self.client.get_block(self.site)

    def render(self, page=None, depth=1):
        product = ""
        if page is None:
            page = self.page
        try:
            product += page.title + '<br>'
        except AttributeError:
            try:
                if page.source is not None:
                    product += f"\n<iframe src='{page.source}' frameborder='0' allow='autoplay; encrypted-media'" \
                               f" allowfullscreen title='video'></iframe>"
            except TypeError:
                pass
            except AttributeError:
                pass
        for p in page.children:
            product += self.render(p, depth=depth+1)
        return product


foo = Interpreter(
    site="https://www.notion.so/Getting-Started-73e110f3e83245ec8b5e1a2462442fc7"
)
