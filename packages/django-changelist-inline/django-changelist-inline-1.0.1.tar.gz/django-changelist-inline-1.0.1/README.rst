========================
django-changelist-inline
========================

Inline Changelists for Django

Overview
========

Django Admin comes with inlines_ which allows you to display forms to edit
related objects from the parent object's change form. While it's technically
possible to use this infrastructure to display list of related objects, it
gets hacky pretty fast.

Here's where *django-changelist-inline* comes into play. It allows you to embed
the standard list of objects as an inline on the parent object's change form.
Internally, it uses a subclass of ``ModelAdmin``, which means you can customize
the list as you'd normally do. Additionally, you can display links below the
list of objects.

Usage Example
=============

Let's assume you have a Django project with two models - ``Thing`` and
``RelatedThing`` and that you want to display list of ``RelatedThing`` objects
as an inline in ``Thing`` change form. The follwing snippet provides an example
of how to implement that using *django-changelist-inline*:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from urllib.parse import urlencode

    from django.contrib import admin
    from django.urls import reverse
    from django.utils.safestring import mark_safe
    from django_changelist_inline import (
        ChangelistInline,
        ChangelistInlineAdmin,
        ChangelistInlineModelAdmin,
    )

    from testing.models import RelatedThing, Thing


    @admin.register(RelatedThing)
    class RelatedThingModelAdmin(admin.ModelAdmin):
        list_display = ('pk', 'name')


    class RelatedThingChangelistInline(ChangelistInline):
        model = RelatedThing

        class ChangelistModelAdmin(ChangelistInlineModelAdmin):
            list_display = ('name', 'format_actions')
            list_display_links = None
            list_per_page = 5

            def get_queryset(self, request):
                return RelatedThing.objects.filter(thing=self.parent_instance)

            @mark_safe
            def format_actions(self, obj=None):
                if obj is None:
                    return self.empty_value_display

                change_link_url = reverse(
                    'admin:{app_label}_{model_name}_change'.format(
                        app_label=RelatedThing._meta.app_label,
                        model_name=RelatedThing._meta.model_name,
                    ),
                    args=[obj.pk],
                )

                return (
                    f'<a class="button" href="{change_link_url}">'
                        'Edit'
                    '</a>'
                )
            format_actions.short_description = 'Actions'

            @property
            def title(self):
                return 'Linked Related Things'

            @property
            def no_results_message(self):
                return 'No Related Things?'

            def get_add_url(self, request):
                result = super().get_add_url(request)
                if result is not None:
                    return result + '?' + urlencode({
                        'thing': self.parent_instance.pk,
                    })

                return result

            def get_show_all_url(self, request):
                result = super().get_show_all_url(request)
                if result is not None:
                    return result + '?' + urlencode({
                        'thing': self.parent_instance.pk,
                    })

                return result

            def get_toolbar_links(self, request):
                return (
                    '<a href="https://www.bthlabs.pl/">'
                        'BTHLabs'
                    '</a>'
                )


    @admin.register(Thing)
    class ThingModelAdmin(ChangelistInlineAdmin):
        inlines = (RelatedThingChangelistInline,)

API
===

``ChangelistInline`` objects
----------------------------

The ``ChangelistInline`` class is the center piece of the API. It's
designed to be used in a ``ModelAdmin``'s ``inlines``.

In order for it to work, you'll need to define the ``model`` property and
embed ``ChangelistModelAdmin`` class, which should be a subclass of
``ChangelistInlineModelAdmin``.

``ChangelistInlineModelAdmin`` objects
--------------------------------------

The ``ChangelistInlineModelAdmin`` is a customized ``ModelAdmin`` subclass
which provides sane defaults and additional functionality for inline
changelists.

**Changelist sanitization**

This subclass overrides the following attributes and methods of ``ModelAdmin``
to provide sane defaults:

* ``list_editable`` - set to empty tuple to disable editing of the list,
* ``list_filter`` - set to empty tuple to disable filtering of the list,
* ``search_fields`` - set to empty tuple to disable searching,
* ``date_hierarchy`` - set to ``None``,
* ``sortable_by`` - set to empty tuple to disable sorting,
* ``get_actions()`` - returns empty list to disable actions.

**Additional functionality**

To allow customization and to expose additional functionality,
``ChangelistInlineModelAdmin`` provides the following additional methods:

* ``title`` property - returns the model's *verbose name* by default.
* ``no_results_message`` property - returns text to display in place of the
  table if no objects are fetched from the DB.
* ``get_add_url(request)`` - returns URL for the model's add form, if the
  user has the add permission. Return ``None`` to hide the add link.
* ``get_show_all_url(request)`` - returns URL for the model's changelist, if
  the user has the view permission. Return ``None`` to hide the show all link.
* ``get_toolbar_links(request)`` - returns ``None`` by default. Override this
  to return string with additional ``<a/>`` elements to render in the toolbar.
  The return value is marked safe in the template.

``ChangelistInlineAdmin`` objects
---------------------------------

The ``ChangelistInlineAdmin`` class is a base class for ``ModelAdmin``
subclasses that use inline changelists.

``ChangelistInlineAdminMixin``
------------------------------

A mixin class that is used to properly configure changelist inlines in the
parent ``ModelAdmin``. Overrides ``get_inlines(request, obj=None)`` and
``get_inline_instances(request, obj=None)`` methods.

If you can't use ``ChangelistInlineAdmin`` as you base class, you can use this
mixin to enable inline changelists:

.. code-block:: python

    @admin.register(Thing)
    class ThingModelAdmin(ChangelistInlineAdminMixin, MyBaseModelAdmin):
        ...

Author
------

*django-changelist-inline* is developed by `Tomek Wójcik`_.

License
-------

*django-changelist-inline* is licensed under the MIT License.

.. _inlines: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
.. _Tomek Wójcik: https://www.bthlabs.pl/
