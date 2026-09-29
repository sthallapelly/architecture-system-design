"""Set external website link attributes in fully rendered MkDocs pages."""

from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit


class ExternalLinks(HTMLParser):
    def __init__(self, html, site_url):
        super().__init__(convert_charrefs=False)
        self.html = html
        self.site = urlsplit(site_url)
        self.offsets = [0]
        for line in html.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.edits = []

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        values = dict(attrs)
        href = values.get('href') or ''
        url = urlsplit(href)
        if not url.netloc or url.scheme.lower() not in ('', 'http', 'https'):
            return
        if url.hostname == 'architecture.sumanthallapelly.com':
            return
        # Recognize this site's configured deployment URL, not other sites
        # that happen to share its hosting domain.
        base = self.site.path.rstrip('/')
        if url.netloc == self.site.netloc and (
            url.path == base or url.path.startswith(base + '/')
        ):
            return
        rel = [token for token in (values.get('rel') or '').split()
               if token.lower() != 'opener']
        for token in ('noopener', 'noreferrer'):
            if token not in rel:
                rel.append(token)
        updated = [(key, value) for key, value in attrs
                   if key not in ('target', 'rel')]
        updated.extend([('target', '_blank'), ('rel', ' '.join(rel))])
        replacement = '<a' + ''.join(
            f' {key}' if value is None else f' {key}="{escape(value, quote=True)}"'
            for key, value in updated
        ) + '>'
        line, column = self.getpos()
        start = self.offsets[line - 1] + column
        self.edits.append((start, start + len(self.get_starttag_text()), replacement))

    def render(self):
        self.feed(self.html)
        result = self.html
        for start, end, replacement in reversed(self.edits):
            result = result[:start] + replacement + result[end:]
        return result


def on_post_page(output, *, page, config):
    # Includes theme-generated repository/footer links, not just article links.
    return ExternalLinks(output, config['site_url']).render()


def on_post_template(output, *, template_name, config):
    # Standalone theme pages such as 404.html do not trigger on_post_page.
    if template_name.endswith('.html'):
        return ExternalLinks(output, config['site_url']).render()
    return output
