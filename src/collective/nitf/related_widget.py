# -*- coding: utf-8 -*-

from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from zope.component import getMultiAdapter

from zope.interface import implementer

from plone.app.layout.navigation.interfaces import INavtreeStrategy

from collective.z3cform.widgets.multicontent_search_widget import \
                                    MultiContentSearchWidget as BaseWidget

from collective.z3cform.widgets.multicontent_search_widget import \
                                    RelatedSearch as BaseRelatedSearch


LIMIT = 10


class RelatedSearch(BaseRelatedSearch):
    display_template = ViewPageTemplateFile('templates/nitf_related_search.pt')

    def __call__(self):
        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()
        limit = LIMIT
        query = self.request.get('q', None)
        offset = int(self.request.get('offset', 0))
        self.show_more = True
        if not query:
            query=''
        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source
        # TODO: use limit?
        result = self.search(query, limit=limit, offset=offset)
        portal_state = getMultiAdapter((self.context, self.request),
                                          name=u'plone_portal_state')
        portal = portal_state.portal()

        strategy = getMultiAdapter((portal, self.context), INavtreeStrategy)

        data = []
        for node in result:
            term = strategy.decoratorFactory({'item':node})
            term['children'] = []
            term['genre'] = node.genre
            term['section'] = node.section
            data.append(term)

        if len(data) < LIMIT:
            self.show_more = False
        result = self.filterSelected(data)
        return self.display_template(children=result, level=1, offset=offset+limit)


class RelatedNITFWidget(BaseWidget):
    recurse_template = ViewPageTemplateFile('templates/nitf_related_recurse.pt')
    display_template = ViewPageTemplateFile('templates/nitf_related_display.pt')


    def brainsToTerms(self, brains):
        portal_state = getMultiAdapter((self.context, self.request),
                                          name=u'plone_portal_state')
        portal = portal_state.portal()

        strategy = getMultiAdapter((portal, self), INavtreeStrategy)
        result = []
        for node in brains:
            term = strategy.decoratorFactory({'item':node})
            term['children'] = []
            term['genre'] = node.genre
            term['section'] = node.section
            result.append(term)
        return {'children': result}


@implementer(IFieldWidget)
def RelatedNITFFieldWidget(field, request):
    return FieldWidget(field, RelatedNITFWidget(request))
