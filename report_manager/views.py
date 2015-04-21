from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error
from map.models import Place
from event_manager.models import Event
import datetime, calendar

def home(request, place_pk):
    # Getting the place
    place = get_object_or_404(Place, pk=place_pk)
    context = {'place': place}

    return render(request, 'form.html', context)


def events_in_date_range(request, place_pk):
    # Scenario 1 is validated displaying a message when have no results!
    # Scenario 2 is validated displaying all events in a place between a date range! (Ideal scenario)
    # Scenario 3 and 4 are validated via js, indicating dates are required fields!

    start_year = 0
    end_year = 0
    if request.method == 'POST':
        # Validating if dates are in valid format!
        try:
            start_year = datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d").year
        except ValueError:
            error(request, "The start date must be with valid format.")
            return redirect('report_home', place_pk=place_pk)

        try:
            end_year = datetime.datetime.strptime(request.POST['end_date'], "%Y/%m/%d").year
        except ValueError:
            error(request, "The end date must be with valid format.")
            return redirect('report_home', place_pk=place_pk)

    else:
        return redirect('report_home', place_pk=place_pk)

    # Scenario 5 is validated redirecting to form page and indicating that
    # end date must be greater than start date
    if datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d") > \
            datetime.datetime.strptime(request.POST['end_date'], "%Y/%m/%d"):
        error(request, "The end date must be greater than the start date.")
        return redirect('report_home', place_pk=place_pk)


    if not start_year > 1900:
        error(request, "The year in the start date must be greater than 1900.")
        return redirect('report_home', place_pk=place_pk)

    if not end_year > 1900:
        error(request, "The year in the end date must be greater than 1900.")
        return redirect('report_home', place_pk=place_pk)


    start_month = datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d").month
    end_month = datetime.datetime.strptime(request.POST['end_date'], "%Y/%m/%d").month

    if not start_month in range(1, 13):
        error(request, "The month in the start date must be between 1 and 12.")
        return redirect('report_home', place_pk=place_pk)

    if not end_month in range(1, 13):
        error(request, "The month in the end date must be between 1 and 12.")
        return redirect('report_home', place_pk=place_pk)


    start_day = datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d").day
    end_day = datetime.datetime.strptime(request.POST['start_date'], "%Y/%m/%d").day

    if start_day <= 0 or start_day >= 30:
        start_day = 1

    if end_day <= 0 or end_day >= 30:
        end_day = calendar.monthrange(end_year, end_month)[1]


    # Getting the place to filter events
    place = get_object_or_404(Place, pk=place_pk)

    # Filtering events in a place and a in a date range
    events = Event.objects.filter(sensor__floor__place=place)\
                            .filter(timestamp__gt=datetime.date(start_year, start_month, start_day),
                                    timestamp__lt=datetime.date(end_year, end_month, end_day))


    context = {'place': place, 'events': events,
               'start_date': request.POST['start_date'], 'end_date': request.POST['end_date']}
    return render(request, 'events_in_date_range.html', context)