from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from django.views.generic import (
    DeleteView,
)
from .models import Event
from .forms import EventForm
from nepalicalendar.nepcal import NepCal
from nepalicalendar.nepdate import NepDate
from .utils.DateConverter import _bs_to_ad
from datetime import datetime, timezone
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .utils.utilities import get_nepali_digit


class MonthlyCalendarBaseView(object):
    """MonthlyCalendarBaseViewis the base view for any view showing calendar.
    It prepares the necessary information for displaying a nepali calendar
    """

    def set_date(self, year, month):
        """
        Sets the calendar to show the monthly calendar of given month and
        year. It prepares other information required to show the calendar
        """
        self.year = int(year)
        self.month = int(month)
        # Make sure month and year are within limits
        if self.year < 2000 or (self.year == 2000 and self.month == 1):
            raise Http404
        if self.year > 2090:
            raise Http404
        self.calendar = NepCal.monthdatescalendar(self.year, self.month)
        self.firstdate = NepDate(self.year, self.month, 1)

        self.prevmonth = self.firstdate
        self.nextmonth = self.firstdate

        try:
            self.prevmonth = NepDate(
                self.year - 1 if self.month == 1 else self.year,
                12 if self.month == 1 else self.month - 1,
                1,
            )
        except BaseException:
            pass  # Do nothing on overflow

        try:
            self.nextmonth = NepDate(
                self.year + 1 if self.month == 12 else self.year,
                1 if self.month == 12 else self.month + 1,
                1,
            )
        except BaseException:
            pass

        # Either to show tithi or not
        self.showtithi = False

        """ TODO: This is hardcoded for now. replace it with actual values"""
        if self.year >= 2040 and self.year <= 2071:
            self.showtithi = True

    def get_context(self, **kwargs):
        """
        Returns all the required context for any template showing a
        calendar
        """
        context = {
            "firstdate": self.firstdate,
            "prevmonth": self.prevmonth,
            "nextmonth": self.nextmonth,
            "monthlycalendar": self.calendar,
            "showtithi": self.showtithi,
        }
        return context


class MonthlyCalendar(TemplateView, MonthlyCalendarBaseView):
    """
    Show the monthly Calendar
    """

    template_name = "calendar/nepalicalendar.html"

    def get_context_data(self, **kwargs):
        context = super(MonthlyCalendar, self).get_context_data(**kwargs)
        # Get the current year and month
        today = NepDate.today()
        if "year" in self.kwargs:
            year = self.kwargs["year"]
        else:
            year = today.year
        if "month" in self.kwargs:
            month = self.kwargs["month"]
        else:
            month = today.month

        self.set_date(year, month)
        context.update(self.get_context())

        context["title"] = "Nepali Calendar:  %s , वि.सं.  %s  - नेपाली पात्रो " % (
            self.firstdate.month_name(), self.firstdate.ne_year, )
        context["custom_event"] = Event.objects.filter(
            category="Event", english_date__gt=datetime.today()
        )[:5]
        context["holiday_event"] = Event.objects.filter(
            category="Holiday", english_date__gt=datetime.today()
        )[:5]
        context["today_event"] = Event.objects.filter(
            event_day=NepDate.today())[:5]
        return context


class EventCreateView(View, PermissionRequiredMixin):
    permission_required = "events.add_event"

    def get(self, request):
        form = EventForm()
        context = {"form": form, "title": "Event"}
        return render(request, "calendar/add_event.html", context)

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            saved = form.save()
            id = saved.id
            user = self.request.user
            # priorityType = checkPriority('Event')

        return redirect("calendar:home")


@permission_required("events.view_event", raise_exception=True)
def event_detail(request, date):
    event_detail = Event.objects.filter(
        category="Event", event_day=date).first()
    context = {"event": event_detail, "title": "Event"}
    return render(request, "calendar/event_detail.html", context)


@permission_required("events.view_event", raise_exception=True)
def holiday_detail(request, date):
    holiday_detail = Event.objects.filter(
        category="Holiday", event_day=date).first()
    context = {"holiday": holiday_detail, "title": "Holiday"}
    return render(request, "calendar/event_detail.html", context)


@permission_required("events.view_event", raise_exception=True)
def today_event(request):
    today_events = Event.objects.filter(event_day=NepDate.today())
    context = {
        "title": "Today Events",
        "today_events": today_events,
    }
    return render(request, "calendar/today_event.html", context)


@permission_required("events.vview_event", raise_exception=True)
def event_list_only(request):
    event_detail = Event.objects.filter(category="Event")
    context = {"holiday": event_detail, "title": "Event"}
    return render(request, "calendar/eventonly.html", context)


@permission_required("events.view_event", raise_exception=True)
def holiday_list_only(request):
    holiday_details = Event.objects.filter(category="Holiday")
    context = {"holiday": holiday_details, "title": "Holiday"}
    return render(request, "calendar/holidayonly.html", context)


class EventListView(View, PermissionRequiredMixin):
    permission_required = "events.view_event"

    def get(self, request):
        # events = Event.objects.all()

        context = {
            # 'events': events,
            "title": "Event",
            "active_menu": "event",
        }
        return render(request, "calendar/event_list.html", context)


class EventEditView(View, PermissionRequiredMixin):
    permission_required = "events.change_event"

    def get(self, request, pk):
        event_instance = get_object_or_404(Event, pk=pk)

        form = EventForm(instance=event_instance)
        context = {
            "form": form,
            "title": "Event",
            "active_menu": "event",
        }
        return render(request, "calendar/edit_event.html", context)

    def post(self, request, pk):
        event_instance = get_object_or_404(Event, pk=pk)
        form = EventForm(request.POST, instance=event_instance)

        if form.is_valid():
            instance = form.save(commit=False)
            nepali_event_day = instance.event_day
            nep_date = nepali_event_day.split("-")
            (
                english_year_digit,
                english_month_digit,
                english_day_digit,
            ) = get_nepali_digit(nep_date[0], nep_date[1], nep_date[2])
            year, month, day = _bs_to_ad(
                english_year_digit, english_month_digit, english_day_digit
            )
            eng = f"{year}-{month}-{day}"
            eng_date = "".join(eng)
            parse_date = datetime.strptime(eng_date, "%Y-%m-%d").date()
            instance.english_date = parse_date
            instance.save()

        return redirect("calendar:home")


class EventDeleteView(
        SuccessMessageMixin,
        DeleteView,
        PermissionRequiredMixin):
    permission_required = "events.delete_event"

    model = Event
    success_url = reverse_lazy("calendar:event_index")
    success_message = "Event Deleted Successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


# @permission_required('student_management_app:view_event_sidebar', raise_exception=True)
# def event_home(request):
#     context = {
#         'title':'Event Management',
#                  }

#     return render(request, 'admin_templates/dashboard.html', context)

# #for popup event
# def event_detail_view(request):#, year, month, day):
#     event_date = request.GET
#     event_test = dict(event_date)['event_date'][0]
#     print(type(event_test))
#     # date_parse = json.loads(dict(event_date))

#     # year,month,day = event_date.split('-')
#     # testeddate = '-'.join([year, month, day])
#     # ev_date = f'{year}-{month}-{day}'

#     # e_date = datetime.datetime(2077,12,29, tzinfo= 'Asia/Kathmandu'),
#     event = Event.objects.filter(event_day = '2077-12-29').values()
#     print(event)
#     event_json = list(event)
#     print(event_json)
#     return JsonResponse(event_json, safe = False)
