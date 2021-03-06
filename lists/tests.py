from django.test import TestCase

from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        _list = List.objects.create()
        Item.objects.create(text="itemey 1", list=_list)
        Item.objects.create(text="itemey 2", list=_list)

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_uses__listtemplate(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "lists/list.html")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        _list = List()
        _list.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = _list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = _list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, _list)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, _list)
