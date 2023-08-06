import logging
from math import ceil
import os

from pelican import signals
from pelican.paginator import Page
from pelican.paginator import Paginator as _Paginator
from pelican.utils import (
    get_relative_path,
    is_selected_for_writing,
    path_to_url,
    sanitised_join,
)
from pelican.writers import Writer

logger = logging.getLogger(__name__)


class Paginator(_Paginator):
    def page(self, number):
        """Returns a Page object for the given 1-based page number.

        Accounts for having one featured article on the first index page.
        """
        bottom = (number - 1) * self.per_page
        if number > 1:
            bottom += 1
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        elif number == 1:
            top += 1
        logger.debug("Bottom: %s; Top: %s", bottom, top)
        return Page(
            self.name,
            self.url,
            self.object_list[bottom:top],
            number,
            self,
            self.settings,
        )

    @property
    def num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            # Account for 1 featured article on the first page
            hits = max(1, self.count - self.orphans - 1)
            self._num_pages = int(ceil(hits / (float(self.per_page) or 1)))
        return self._num_pages


class PaginatedWriter(Writer):
    def write_file(
        self,
        name,
        template,
        context,
        relative_urls=False,
        paginated=None,
        template_name=None,
        override_output=False,
        url=None,
        **kwargs
    ):
        """Render the template and write the file.

        Reimplemented from the default writer so that the Paginator can be overridden
        with the version defined here.

        :param name: name of the file to output
        :param template: template to use to generate the content
        :param context: dict to pass to the templates.
        :param relative_urls: use relative urls or absolutes ones
        :param paginated: dict of article list to paginate - must have the
            same length (same list in different orders)
        :param template_name: the template name, for pagination
        :param override_output: boolean telling if we can override previous
            output with the same name (and if next files written with the same
            name should be skipped to keep that one)
        :param url: url of the file (needed by the paginator)
        :param **kwargs: additional variables to pass to the templates
        """

        if (
            name is False
            or name == ""
            or not is_selected_for_writing(
                self.settings, os.path.join(self.output_path, name)
            )
        ):
            return
        elif not name:
            # other stuff, just return for now
            return

        def _write_file(template, localcontext, output_path, name, override):
            """Render the template write the file."""
            # set localsiteurl for context so that Contents can adjust links
            if localcontext["localsiteurl"]:
                context["localsiteurl"] = localcontext["localsiteurl"]
            output = template.render(localcontext)
            path = sanitised_join(output_path, name)

            try:
                os.makedirs(os.path.dirname(path))
            except Exception:
                pass

            with self._open_w(path, "utf-8", override=override) as f:
                f.write(output)
            logger.info("Writing %s", path)

            # Send a signal to say we're writing a file with some specific
            # local context.
            signals.content_written.send(path, context=localcontext)

        def _get_localcontext(context, name, kwargs, relative_urls):
            localcontext = context.copy()
            localcontext["localsiteurl"] = localcontext.get("localsiteurl", None)
            if relative_urls:
                relative_url = path_to_url(get_relative_path(name))
                localcontext["SITEURL"] = relative_url
                localcontext["localsiteurl"] = relative_url
            localcontext["output_file"] = name
            localcontext.update(kwargs)
            return localcontext

        if paginated is None:
            paginated = {
                key: val for key, val in kwargs.items() if key in {"articles", "dates"}
            }

        # pagination
        if paginated and template_name in self.settings["PAGINATED_TEMPLATES"]:
            # pagination needed
            per_page = (
                self.settings["PAGINATED_TEMPLATES"][template_name]
                or self.settings["DEFAULT_PAGINATION"]
            )

            # init paginators
            paginators = {
                key: Paginator(name, url, val, self.settings, per_page)
                for key, val in paginated.items()
            }

            # generated pages, and write
            for page_num in range(list(paginators.values())[0].num_pages):
                paginated_kwargs = kwargs.copy()
                for key in paginators.keys():
                    paginator = paginators[key]
                    previous_page = paginator.page(page_num) if page_num > 0 else None
                    page = paginator.page(page_num + 1)
                    next_page = (
                        paginator.page(page_num + 2)
                        if page_num + 1 < paginator.num_pages
                        else None
                    )
                    paginated_kwargs.update(
                        {
                            "%s_paginator" % key: paginator,
                            "%s_page" % key: page,
                            "%s_previous_page" % key: previous_page,
                            "%s_next_page" % key: next_page,
                        }
                    )

                localcontext = _get_localcontext(
                    context, page.save_as, paginated_kwargs, relative_urls
                )
                _write_file(
                    template,
                    localcontext,
                    self.output_path,
                    page.save_as,
                    override_output,
                )
        else:
            # no pagination
            localcontext = _get_localcontext(context, name, kwargs, relative_urls)
            _write_file(template, localcontext, self.output_path, name, override_output)


def get_writer(pelican_object):
    return PaginatedWriter


def register():
    signals.get_writer.connect(get_writer)
