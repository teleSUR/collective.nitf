from zope.interface import alsoProvides

from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset

from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form

from collective.nitf.related_widget import RelatedNITFFieldWidget
try:
    from plone.app.dexterity import MessageFactory as _
except ImportError:
    _ = unicode


class IRelatedItems(form.Schema):
    """Behavior interface to make a Dexterity type support related items.
    """

    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ObjPathSourceBinder()),
        required=False,
        )
    form.widget(relatedItems=RelatedNITFFieldWidget)
    
fieldset = Fieldset('categorization',
                    label=_(u'Categorization'),
                    fields=['relatedItems'])

IRelatedItems.setTaggedValue(FIELDSETS_KEY, [fieldset])

alsoProvides(IRelatedItems, IFormFieldProvider)