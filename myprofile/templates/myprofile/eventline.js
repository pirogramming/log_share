function GetEvents() {
    return [
        {
            id: 1,
            title: "Catalyst 0",
            startDate: "2017-9-17",
            endDate: "2017-9-17",
            notes: "This is the last catalyst we shall be tracking in the year 2017. There are no interesting events occurring after this one."
        },
        {
            id: 2,
            title: "Catalyst 1",
            startDate: "2018-1-18",
            endDate: "2018-1-18",
            notes: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        },
        {
            id: 3,
            title: "Catalyst A",
            startDate: "2018-1-23",
            endDate: "2018-1-23",
            notes: "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
            id: 4,
            title: "Catalyst 2",
            startDate: "2018-3-7",
            endDate: "2018-3-9",
            notes: "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo."
        },
        {
            id: 5,
            title: "Catalyst 3",
            startDate: "2018-3-28"
        },
        {
            id: 6,
            title: "Catalyst 4",
            startDate: "2018-10-13"
        },
        {
            id: 7,
            title: "Catalyst B",
            startDate: "2018-11-12"
        },
        {
            id: 8,
            title: "Catalyst 5",
            startDate: "2019-3-2"
        },
        {
            id: 9,
            title: "Catalyst C",
            startDate: "2019-10-2"
        }
    ]
}

function CalculateEventPosition(earliestDate, startDate) {
    // Get number of months between the event's start date and ealiest event
    var date = new Date(startDate);
    var monthOffset = Math.floor((date - earliestDate) / (1000 * 60 * 60 * 24 * 30));

    // The position should be moved right 100px for each month offset
    // and a fraction of 100px in the ratio of number of days in 30
    return Math.floor(100 * (monthOffset + (date.getDate() / 30)));
}

function GetMonthDay(dateString) {
    var date = new Date(dateString);
    return date.getMonth()
}

function GetClosestEvent() {
    var events = GetEvents();
    var diff = Number.MAX_VALUE;
    var distanceFromToday;
    var previousEvent = events[0];

    $.each(events, function(i, e) {
        // Calculate distance of event start date from today
        distanceFromToday = Math.abs((new Date(e.startDate)) - (new Date()));
        if (distanceFromToday < diff) {
            diff = distanceFromToday;
            previousEvent = e;
        }
        else {
            return false;
        }
    });

    return previousEvent;
}

function InitializeTimeline() {
    var monthPixels = 100;
    var events = GetEvents();

    // If events are sorted the first and last should be earliest and latest
    var earliestDate = new Date(events[0].startDate);
    var latestDate = new Date(events[events.length - 1].startDate);

    // Calculate time difference in months from earliest to latest event
    var timelineMonthSpan = Math.floor((latestDate - earliestDate) / (1000 * 60 * 60 * 24 * 30));

    // Set timeline width based on number of months spanned adding one month for buffer
    $("#timeline").css("width", (timelineMonthSpan + 1) * monthPixels);

    // Add timeline ticks
    for (i = 0; i <= timelineMonthSpan + 1; i++) {
        $("#ticks").append(
            "<li class='timeline-tick' style='left: " + (i * 100) + "px'><span class='tick-label'>" + moment(earliestDate, 'YYYY-MM-DD').add(i, 'M').format('MMM YYYY').toUpperCase() + "</span></li>"
        );
    }

    // Get closest event to current date
    closestEvent = GetClosestEvent();

    // Add events to the timeline
    var eventMarker;
    var eventMarkerPosition;
    var closestEventPosition;
    $.each(events, function(i, event) {
        eventMarkerPosition = CalculateEventPosition(earliestDate, event.startDate);
        eventMarker = 
            "<li class='event-marker" +
            (event.id == closestEvent.id ? " selected" : "") +
            "' style='left: " +
            eventMarkerPosition +
            "px' title='" + 
            event.title +
            "' data-id='" +
            event.id +
            "'></li>";
        $("#eventList").append(eventMarker);

        if (event.id == closestEvent.id) {
            AddEventDetail(closestEvent);
            closestEventPosition = eventMarkerPosition
        }
    });

    // Set timeline position
    var timelineWrapperCenter = Math.round(document.getElementById('timelineWrapper').getBoundingClientRect().width / 2);
    $('#timeline').css('transform', 'translateX(' + (timelineWrapperCenter - closestEventPosition).toString() + 'px)')
}

function GetMatrixValue(matrix, pos) {
    var matrixValues = (matrix.substring(matrix.indexOf("(") + 1, matrix.length - 1)).split(",");
    if (pos < matrixValues.length) {
        return matrixValues[pos];
    }
    else return undefined;
}

function PastLeftBound() {
    // Check timeline bounds
    var timeline = document.getElementById("timeline").getBoundingClientRect();
    var navPast = document.getElementById("navPast").getBoundingClientRect();
    var navFuture = document.getElementById("navFuture").getBoundingClientRect();

    if (timeline.x > navPast.x + navPast.width) {
        return true;
    }
    else {
        return false;
    }
}

function PastRightBound() {
    // Check timeline bounds
    var timeline = document.getElementById("timeline").getBoundingClientRect();
    var navPast = document.getElementById("navPast").getBoundingClientRect();
    var navFuture = document.getElementById("navFuture").getBoundingClientRect();

    if (timeline.x + timeline.width < navFuture.x) {
        return true;
    }
    else {
        return false;
    }
}

function AddEventDetail(event) {
    $(".event-title").text(event.title);
    $(".event-start-date").text(moment(event.startDate).format('MMM D'));
    if (event.endDate) {
        if (event.endDate != event.startDate) {
            $(".event-end-date").text(moment(event.endDate).format('MMM D'));
            $(".separator").show();
            $(".event-end-date").show();
        }
        else {
            $(".separator").hide();
            $(".event-end-date").hide();
        }
    }
    else {
        $(".separator").hide();
        $(".event-end-date").hide();
    }
    if (event.notes) {
        $(".event-notes").html(event.notes);
    }
}

function AddEventHandlers() {
    $(".timeline-nav").click(function(e) {
        var monthsToMove = 1;
        var monthPixels = 100;
        var transformMatrix = $("#timeline").css("transform");
        var xTranslation;
        var newXTranslation;
        if (transformMatrix == "none") {
            xTranslation = 0;
        }
        else {
            xTranslation = GetMatrixValue(transformMatrix, 4);
        }
        newXTranslation = xTranslation;
        if ($(this).hasClass("nav-past")) {
            if (!PastLeftBound()) {
                newXTranslation = parseInt(xTranslation) + (monthsToMove * monthPixels);
            }
        }
        else {
            if (!PastRightBound()) {
                newXTranslation = parseInt(xTranslation) - (monthsToMove * monthPixels);
            }
        }
        if (newXTranslation != xTranslation) {
            $("#timeline").css("transform", "translateX(" +  newXTranslation + "px)");
        }
    });

    $(".event-marker").click(function() {
        // Change marker
        $(".event-marker").removeClass("selected");
        $(this).addClass("selected");

        // Show event detail
        var eventId = parseInt($(this).attr("data-id"));
        var events = GetEvents();
        var event = $.grep(events, function(e, i) {
            return e.id == eventId;
        })[0];

        console.log(event);

        // Show event detail
        AddEventDetail(event);
    });
}

$(document).ready(function() {
    InitializeTimeline();
    AddEventHandlers();
});