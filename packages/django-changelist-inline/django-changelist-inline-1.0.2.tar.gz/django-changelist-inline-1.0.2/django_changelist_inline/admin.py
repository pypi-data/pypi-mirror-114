# -*- coding: utf-8 -*-
# django-changelist-inline v1.0.2 | (c) 2021-present Tomek Wójcik | MIT License
import copy

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.http import QueryDict
from django.urls import reverse


class InlineChangeList(ChangeList):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.formset = None
        self.add_url = self.model_admin.get_add_url(request)
        self.show_all_url = self.model_admin.get_show_all_url(request)
        self.toolbar_links = self.model_admin.get_toolbar_links(request)

    @property
    def has_toolbar(self):
        return any([
            self.add_url is not None,
            self.show_all_url is not None,
            self.toolbar_links is not None,
        ])


class ChangelistInlineModelAdmin(admin.ModelAdmin):
    def __init__(self, parent_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_instance = parent_instance

        self.list_editable = ()
        self.list_filter = ()
        self.search_fields = ()
        self.date_hierarchy = None
        self.sortable_by = ()
        self.show_full_result_count = False

    def get_actions(self, request):
        return []

    def get_changelist(self, request, **kwargs):
        return InlineChangeList

    @property
    def title(self):
        return self.model._meta.verbose_name_plural

    @property
    def no_results_message(self):
        return f'0 {self.model._meta.verbose_name_plural}'

    def get_add_url(self, request):
        if self.has_add_permission(request):
            return reverse('admin:{app_label}_{model_name}_add'.format(
                app_label=self.model._meta.app_label,
                model_name=self.model._meta.model_name,
            ))

        return None

    def get_show_all_url(self, request):
        if self.has_view_permission(request, obj=None):
            return reverse('admin:{app_label}_{model_name}_changelist'.format(
                app_label=self.model._meta.app_label,
                model_name=self.model._meta.model_name,
            ))

        return None

    def get_toolbar_links(self, request):
        return None


class ChangelistInline(InlineModelAdmin):
    template = 'django_changelist_inline/changelist_inline.html'

    class Media:
        css = {
            'all': [
                'admin/css/changelists.css',
                'django_changelist_inline/css/changelist_inline.css',
            ],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None
        self.changelist_model_admin = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def bind(self, request, parent_instance):
        internal_request = copy.copy(request)
        internal_request.GET = QueryDict(mutable=False)
        internal_request.POST = QueryDict(mutable=False)
        self.request = internal_request

        self.changelist_model_admin = self.ChangelistModelAdmin(
            parent_instance,
            self.model,
            self.admin_site,
        )

    @property
    def changelist(self):
        can_view = self.changelist_model_admin.has_view_or_change_permission(
            self.request, obj=None,
        )
        if not can_view:
            return None

        result = self.changelist_model_admin.get_changelist_instance(
            self.request,
        )
        return result


class ChangelistInlineAdminMixin:
    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj=obj)

        if obj is None:
            return [
                inline_instance for inline_instance in inline_instances
                if not isinstance(inline_instance, ChangelistInline)
            ]
        else:
            for inline_instance in inline_instances:
                if isinstance(inline_instance, ChangelistInline):
                    inline_instance.bind(request, obj)

        return inline_instances


class ChangelistInlineAdmin(ChangelistInlineAdminMixin, admin.ModelAdmin):
    pass
