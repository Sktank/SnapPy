/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 1/25/14
 * Time: 7:35 PM
 * To change this template use File | Settings | File Templates.
 */
function clock() {

    var self = this;
    self.days = ko.observable();
    self.hours = ko.observable();
    self.minutes = ko.observable();
    self.seconds = ko.observable();

    var current_date = new Date(),
        start_date = new Date(2014,5,12,20,0,0,0),
        days_to_second = 60 * 60 * 24,
        hours_to_second = 60 * 60,
        minutes_to_second = 60;

    function getDuration(now, later) {
        var seconds_remaining,
            xdays,
            xhours,
            xminutes,
            xseconds;
        var total_seconds = (later.getTime() - now.getTime()) / 1000;
        console.log(total_seconds);
        xdays = Math.floor(total_seconds / (days_to_second));
        seconds_remaining = total_seconds % days_to_second;
        xhours = Math.floor(seconds_remaining / (hours_to_second));
        seconds_remaining = seconds_remaining % hours_to_second;
        xminutes = Math.floor(seconds_remaining / (minutes_to_second));
        seconds_remaining = seconds_remaining % minutes_to_second;
        xseconds = Math.floor(seconds_remaining);
        return {
            "days": xdays,
            "hours": xhours,
            "minutes": xminutes,
            "seconds": xseconds
        };
    }

    function countDown(days, hours, minutes, seconds) {
        var xdays = days,
            xhours = hours,
            xminutes = minutes,
            xseconds = seconds;

        xseconds--;
        if (xseconds == -1) {
            xseconds = 59;
            xminutes--;
            if (xminutes == -1) {
                xminutes = 59;
                xhours--;
                if (xhours == -1) {
                    xhours = 23;
                    xdays--;
                    if (xdays == -1) {
                        return -1;
                    }
                }
            }
        }
        return {
            "days": xdays,
            "hours": xhours,
            "minutes": xminutes,
            "seconds": xseconds
        };
    }

    var time_left = getDuration(current_date, start_date);
    self.days(time_left.days);
    self.hours(time_left.hours);
    self.minutes(time_left.minutes);
    self.seconds(time_left.seconds);

    setInterval(function() {
            var new_time = countDown(self.days(), self.hours(), self.minutes(), self.seconds());
            self.days(new_time.days);
            self.hours(new_time.hours);
            self.minutes(new_time.minutes);
            self.seconds(new_time.seconds);
        }, 1000
    );
}

ko.applyBindings(new clock(), document.getElementById('ko-clock'));

