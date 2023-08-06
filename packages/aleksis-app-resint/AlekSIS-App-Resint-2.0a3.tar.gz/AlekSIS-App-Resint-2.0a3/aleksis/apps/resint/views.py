from typing import Any, Dict

from django.db.models import QuerySet
from django.http import FileResponse, HttpRequest
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView

from guardian.shortcuts import get_objects_for_user
from rules.contrib.views import PermissionRequiredMixin

from aleksis.core.mixins import AdvancedCreateView, AdvancedDeleteView, AdvancedEditView

from .forms import PosterGroupForm, PosterUploadForm
from .models import Poster, PosterGroup


class PosterGroupListView(PermissionRequiredMixin, ListView):
    """Show a list of all poster groups."""

    template_name = "resint/group/list.html"
    model = PosterGroup
    permission_required = "resint.view_postergroups_rule"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if self.request.user.has_perm("resint.view_postergroup"):
            return qs
        return get_objects_for_user(self.request.user, "resint.view_postergroup", qs)


class PosterGroupCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create a new poster group."""

    model = PosterGroup
    success_url = reverse_lazy("poster_group_list")
    template_name = "resint/group/create.html"
    success_message = _("The poster group has been saved.")
    form_class = PosterGroupForm
    permission_required = "resint.create_postergroup_rule"


class PosterGroupEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit an existing poster group."""

    model = PosterGroup
    success_url = reverse_lazy("poster_group_list")
    template_name = "resint/group/edit.html"
    success_message = _("The poster group has been saved.")
    form_class = PosterGroupForm
    permission_required = "resint.edit_postergroup_rule"


class PosterGroupDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete a poster group."""

    model = PosterGroup
    success_url = reverse_lazy("poster_group_list")
    success_message = _("The poster group has been deleted.")
    template_name = "core/pages/delete.html"
    permission_required = "resint.delete_postergroup_rule"


class PosterListView(PermissionRequiredMixin, ListView):
    """Show a list of all uploaded posters."""

    template_name = "resint/poster/list.html"
    model = Poster
    permission_required = "resint.view_posters_rule"

    def get_queryset(self) -> QuerySet:
        qs = Poster.objects.all().order_by("-year", "-week")

        if self.request.user.has_perm("resint.view_poster"):
            return qs

        allowed_groups = get_objects_for_user(
            self.request.user, "resint.view_poster_of_group", PosterGroup
        )
        posters = get_objects_for_user(self.request.user, "resint.view_poster", qs)
        return qs.filter(group__in=allowed_groups) | posters

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["poster_groups"] = PosterGroup.objects.all().order_by("name")
        return context


class PosterUploadView(PermissionRequiredMixin, AdvancedCreateView):
    """Upload a new poster."""

    model = Poster
    success_url = reverse_lazy("poster_index")
    template_name = "resint/poster/upload.html"
    success_message = _("The poster has been uploaded.")
    form_class = PosterUploadForm
    permission_required = "resint.upload_poster_rule"

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"request": self.request}


class PosterEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit an uploaded poster."""

    model = Poster
    success_url = reverse_lazy("poster_index")
    template_name = "resint/poster/edit.html"
    success_message = _("The poster has been changed.")
    form_class = PosterUploadForm
    permission_required = "resint.edit_poster_rule"

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"request": self.request}


class PosterDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete an uploaded poster."""

    model = Poster
    success_url = reverse_lazy("poster_index")
    success_message = _("The poster has been deleted.")
    template_name = "core/pages/delete.html"
    permission_required = "resint.delete_poster_rule"


class PosterCurrentView(PermissionRequiredMixin, SingleObjectMixin, View):
    """Show the poster which is currently valid."""

    model = PosterGroup
    permission_required = "resint.view_poster_pdf"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> FileResponse:
        group = self.get_object()
        current_poster = group.current_poster
        file = current_poster.pdf if current_poster else group.default_pdf
        return FileResponse(file, content_type="application/pdf")
