/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/18/14
 * Time: 11:15 PM
 * To change this template use File | Settings | File Templates.
 */

// Models
window.Course = Backbone.Model.extend();

window.StudentCourseCollection = Backbone.Collection.extend({
    model:Course,
    url:"api/studentcourses",
    parse: function(response) {
        return response.results;
    }
});

window.CourseCollection = Backbone.Collection.extend({
    model:Course,
    url:"api/courses",
    parse: function(response) {
        return response.results;
    }
});

window.EnrollmentQueueCollection = Backbone.Collection.extend({
    model:Course
});


// Views
window.StudentCourseListView = Backbone.View.extend({

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        console.log('rendering list');
        console.log(this.model.models);
        // render the lesson view headers
        $(".list-group-item").removeClass("active");
        $("#student-list-tab").addClass("active");

        if (this.model.models.length > 0) {
            $(this.el).append("<h3>Current Classes as Student</h3><div id='student-list'></div>");
            _.each(this.model.models, function (course) {
                $(this.el).append(new StudentCourseListItemView({model:course}).render().el);
            }, this);
        }
        else {
            $(this.el).append("<h3>You Are Not Currently Enrolled In Any Classes</h3>");
        }
        // Class Registration
        return this;
    }

});

window.StudentCourseListItemView = Backbone.View.extend({

    template:_.template($('#student-list-item').html()),

    render:function (eventName) {
        var self = this;
        var json = this.model.toJSON();
        $(this.el).html(this.template(json));
        $(this.el).click(function() {
            window.location = "#student/" + json.id
        });
        $(this.el)
            .mouseenter(function() {
                $(self.el).addClass("container-focus")
            })
            .mouseleave(function() {
                $(self.el).removeClass("container-focus")
            });
        return this;
    }

});

window.StudentClassSearchView = Backbone.View.extend({

    template:_.template($('#student-class-search').html()),

    render:function (eventName) {
        $(this.el).html(this.template());

        _.each(this.model.models, function (course) {
            $(this.el).append(new StudentClassSearchItemView({model:course}).render().el);
        }, this);

        return this;
    }

});

window.StudentClassSearchItemView = Backbone.View.extend({

    template:_.template($('#student-class-search-item').html()),

    render:function (eventName) {
        var self = this;
        var json = this.model.toJSON();
        $(this.el).addClass("col-md-3").html(this.template(json));
        console.log(window.app.studentClassList);
        $(this.el).addClass('class-search-item');
        if (window.app.studentClassList.findWhere({ id: json.id })) {
            $(this.el).addClass("enrolled_class");
        }
        else {
            $(this.el).addClass("unenrolled_class");
            $(this.el).click(function() {
                addCourseToEnrollmentQueue(self.model);
                $(self.el).addClass("queued_class");
            });
        }
        return this;
    }
});

window.StudentClassEnrollmentQueueView = Backbone.View.extend({

    template:_.template($('#student-class-enrollment-queue').html()),

    render:function (eventName) {
        $(this.el).html(this.template());
        _.each(this.model.models, function (course) {
            $(this.el).append(new StudentClassEnrollmentQueueItemView({model:course}).render().el);
        }, this);


        if (this.model.models.length > 0) {
            $(this.el).append('<div class="btn btn-danger btn-lg class-clear-btn queue_btn">Clear</div>');
            $( document ).on( "click", ".class-clear-btn", function() {
                clearEnrollmentQueue();
            });
            $(this.el).append('<div class="btn btn-success btn-lg enroll-btn class-enroll-btn queue_btn">Enroll\<' +
                '/div> <span id="class-enroll-message"></span>');

            $( document ).on( "click", ".class-enroll-btn", function() {
                enrollCourses()
            });
        }
        else {
            $(this.el).append('<h5>Empty</h5>');
        }
        return this;
    }

});

window.StudentClassEnrollmentQueueItemView = Backbone.View.extend({

    template:_.template($('#student-class-enrollment-queue-item').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        $(this.el).html(this.template(json));

        return this;
    }
});

window.StudentCourseView = Backbone.View.extend({

    template:_.template($('#student-course-details').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        var promise = getLessons(json.id);
        var self = this;
        $(self.el).addClass("container-details");
        $(self.el).append('<h5>Lessons</h5>');
//            .html(self.template(json));
        promise.success(function (data) {
            var lessons = $.parseJSON(data)[0];
            console.log(data);
            _.each(lessons, function (lesson) {
                $(self.el).append('<a id="course-' + json.id + '-lesson-' + lesson['pk'] + '" href="#student/' +
                    json.id + '/lesson/' + lesson['pk'] + '">' + lesson['fields']['name'] + '</a><br>');

            }, this);
        });
        $(this.el).addClass("container-details").html(this.template(json));
        return this;
    }

});

window.StudentLessonView = Backbone.View.extend({

    initialize : function (options) {
        this.options = options || {};
    },

    template:_.template($('#snap-template').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        console.log(this);
        var course_id = this.options.course;
        var self = this;
        $(self.el).append('<h5>Lessons</h5>');
//            .html(self.template(json));
        console.log(course_id);
        $('#current-lesson').text("Course: " + course_id + ", Lesson: " + json.name);
        $(self.el).html(self.template(json));
        $('#content').show();
        loadSnap(json.id);
        return this;
    }
});