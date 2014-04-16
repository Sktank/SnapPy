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
        //console.log('rendering list');
        //console.log(this.model.models);
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
        var self = this;
        $(self.el).html(self.template());

        $(self.el).on('click', '#search-by-teacher-tab', function() {
            //console.log("here");
            dashUtils.clearStudentSearch();
            dashUtils.refreshList('courses-by-teacher-list');
            $(self.el).find('#search-by-teacher-tab').parent().addClass("active");
            $("#courses-by-teacher").css('display', 'inline');

        });
        $(self.el).on('click', '#search-by-name-tab', function() {
            //console.log("here");
            dashUtils.clearStudentSearch();
            dashUtils.refreshList('courses-by-name-list');
            $(self.el).find('#search-by-name-tab').parent().addClass("active");
            $("#courses-by-name").css('display', 'inline');

        });
        $(self.el).on('click', '#browse-all-tab', function() {
            //console.log("here");
            dashUtils.clearStudentSearch();
            dashUtils.refreshList('all-courses');
            $(self.el).find('#browse-all-tab').parent().addClass("active");
            $("#all-courses").css('display', 'inline');
        });

        $(self.el).on('click', '#search-courses-btn', function() {
            $('#courses-by-name-list').empty();
            var promise = dashUtils.getCoursesByName($('#srch-term-course').val());
            promise.success(function (data) {
                dashUtils.updateSearchNameList(data);
            });

        });

        $(self.el).on('click', '#search-teachers-btn', function() {
            $('#courses-by-teacher-list').empty();
            var promise = dashUtils.getCoursesByTeacher($('#srch-term-teacher').val());
            promise.success(function (data) {
                dashUtils.updateSearchTeacherList(data);
            });
        });


        _.each(this.model.models, function (course) {
            $(this.el).find("#all-courses").append(new StudentClassSearchItemView({model:course}).render().el);
        }, this);

        return this;
    }

});

window.StudentClassSearchItemView = Backbone.View.extend({

    initialize : function (options) {
        this.options = options || {};
    },

    template:_.template($('#student-class-search-item').html()),

    render:function (eventName) {
        var self = this;
        var json;
        if (this.model.attributes) {
            json = this.model.toJSON();
        }
        else {
            this.model.id = this.options.id;
            json = _.clone(this.model)
        }
        //console.log(json);
        $(self.el).addClass("col-md-4").html(self.template(json));
        $(self.el).find("#search-course-" + json.id).addClass('class-search-item');
        if (window.app.studentClassList.findWhere({ id: json.id })) {
            $(self.el).find("#search-course-" + json.id).addClass("enrolled_class");
        }
        else {
            $(self.el).find("#search-course-" + json.id).addClass("unenrolled_class");
            if (window.app.enrollmentQueueList.findWhere({id: json.id})) {
                $(self.el).find("#search-course-" + json.id).addClass("queued_class");
            }
            $(self.el).on('click', "#search-course-" + json.id, function() {
                if (!$(self.el).find("#search-course-" + json.id).hasClass("queued_class")) {
                    dashUtils.addCourseToEnrollmentQueue(self.model);
                    $(self.el).find("#search-course-" + json.id).addClass("queued_class");
                }
                else {
                    dashUtils.removeCourseFromEnrollmentQueue(self.model);
                    $(self.el).find("#search-course-" + json.id).removeClass("queued_class");
                }
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
                dashUtils.clearEnrollmentQueue();
            });
            $(this.el).append('<div class="btn btn-success btn-lg enroll-btn class-enroll-btn queue_btn">Enroll\<' +
                '/div> <span id="class-enroll-message"></span>');

            $( document ).on( "click", ".class-enroll-btn", function() {
                dashUtils.enrollCourses()
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
        var promise = dashUtils.getLessons(json.id);
        var self = this;
        $(self.el).addClass("container-details");
        $(self.el).append('<h5>Lessons</h5>');
        promise.success(function (data) {
            var lessons = $.parseJSON(data)[0];
            //console.log(data);
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
        //console.log(this);
        var course_id = this.options.course;
        var self = this;
        $('#home-btn').html('<a href="#student/' + course_id + '"><div class="btn btn-default">Class List</div></a>');
        $(self.el).append('<h5>Lessons</h5>');
        //console.log(course_id);
        $('#current-lesson').text("Course: " + course_id + ", Lesson: " + json.name);
        $(self.el).html(self.template(json));
        $('#content').show();
        dashUtils.loadSnap(json.id);
        return this;
    }
});