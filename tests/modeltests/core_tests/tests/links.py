from django.test import TestCase

from widgy.models.links import (
    get_all_linkable_classes, get_all_linker_classes,
    get_link_field_from_model
)

from modeltests.core_tests.models import (
    LinkableThing, ThingWithLink, AnotherLinkableThing,
    Bucket, VersionPageThrough
)


class TestLinkRelations(TestCase):
    def test_get_all_linkable_classes(self):
        self.assertIn(LinkableThing, get_all_linkable_classes())
        self.assertIn(AnotherLinkableThing, get_all_linkable_classes())

    def test_get_all_linker_classes(self):
        self.assertIn(ThingWithLink, get_all_linker_classes())
        self.assertNotIn(Bucket, get_all_linker_classes())
        self.assertNotIn(VersionPageThrough, get_all_linker_classes())

    def test_get_all_links_for_obj(self):
        linkable = LinkableThing.objects.create()

        self.assertEqual(len(list(linkable.get_links())), 0)

        thing = ThingWithLink.objects.create(
            link=linkable,
        )

        self.assertEqual(list(linkable.get_links()), [thing])

        linkable2 = AnotherLinkableThing.objects.create()

        thing2 = ThingWithLink.objects.create(
            link=linkable2,
        )

        self.assertEqual(list(linkable2.get_links()), [thing2])

    def test_get_all_possible_linkables(self):
        l1 = LinkableThing.objects.create()
        l2 = LinkableThing.objects.create()
        l3 = AnotherLinkableThing.objects.create()

        choices = get_link_field_from_model(ThingWithLink, 'link').get_choices()

        self.assertEqual(list(choices), [l1, l2, l3])
