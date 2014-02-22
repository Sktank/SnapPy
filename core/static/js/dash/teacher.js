/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/18/14
 * Time: 5:37 PM
 * To change this template use File | Settings | File Templates.
 */


// Models
window.Course = Backbone.Model.extend();

window.TeacherCourseCollection = Backbone.Collection.extend({
    model:Course,
    url:"api/teachercourses",
    parse: function(response) {
        return response.results;
    }
});

window.CourseLesson = Backbone.Model.extend();

window.CourseLessonCollection = Backbone.Collection.extend({
    model:CourseLesson,
    url:"api/courselessons",
    parse: function(response) {
        return response.results;
    }
});


// Views
window.TeacherCourseListView = Backbone.View.extend({

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        console.log('rendering list');
        console.log(this.model.models);
        // render the lesson view headers
        $(".list-group-item").removeClass("active");
        $("#teacher-list-tab").addClass("active");

        if (this.model.models.length > 0) {
            $(this.el).append("<h3>Current Classes as Teacher</h3><div id='teacher-list'></div>");
            _.each(this.model.models, function (course) {
                $(this.el).append(new TeacherCourseListItemView({model:course}).render().el);
            }, this);
        }
        else {
            $(this.el).append("<h3>You Are Currently Teaching No Classes</h3>");
        }
        // Class Registration
        return this;
    }

});

window.TeacherCourseListItemView = Backbone.View.extend({

    template:_.template($('#teacher-list-item').html()),

    render:function (eventName) {
        var self = this;
        var json = this.model.toJSON();
        $(this.el).html(this.template(json));
        $(this.el).click(function() {
            window.location = "#teacher/" + json.id
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

window.TeacherCourseRegisterView = Backbone.View.extend({

    template:_.template($('#teacher-course-register').html()),

    render:function (eventName) {
        $(this.el).html(this.template());
        $( document ).on( "click", "#create-new-lesson-tab", function() {
            $("#teacher_additions_navs").children().removeClass("active");
            $(this).parent().addClass("active");
            $("#create-class").css("display", "none");
            $("#create-lesson").css("display", "inline");
        });
        $( document ).on( "click", "#create-new-class-tab", function() {
            $("#teacher_additions_navs").children().removeClass("active");
            $(this).parent().addClass("active");
            $("#create-lesson").css("display", "none");
            $("#create-class").css("display", "inline");
        });
        return this;
    }

});

window.TeacherCourseView = Backbone.View.extend({

    template:_.template($('#teacher-course-details').html()),

    render:function (eventName) {
        console.log("course view");
        var json = this.model.toJSON();
        var promise = getLessons(json.id);
        var self = this;
        $(self.el).addClass("container-details");
        $(self.el).append('<h5>Lessons</h5>')
//            .html(self.template(json));
        promise.success(function (data) {
            var lessons = $.parseJSON(data);
            console.log(data);
            _.each(lessons, function (lesson) {
                $(self.el).append('<a id="course-' + json.id + '-lesson-' + lesson['pk'] + '" href="#teacher/' + json.id + '/lesson/' + lesson['pk'] + '">' + lesson['fields']['name'] + '</a><br>');

            }, this);
        });
        return this;
    }

});

window.TeacherLessonView = Backbone.View.extend({

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

//    template:_.template($('#teacher-lesson-details').html()),

    render:function (eventName) {

        // get the course and list of students for that course of the lesson.
        var json = this.model.toJSON();
        var self = this;
        var router = window.app;
        console.log(json);

        console.log(this.model);
        var promise = getCourseAndStudents(json.id);

        promise.success(function (data) {
            var resp = $.parseJSON(data);
            var course = resp[0];
            var courseName = course[0]['fields']['name'];
            var courseId = course[0]['pk'];
            var students = resp[1];
            console.log(students);

            // add course name to top

            $(self.el).append('<div><h3>Course: ' + courseName + '</h3></div>');
            $(self.el).append('<div><h4>Lesson: ' + json.name + '</h4></div>');

            var append_promise = $('#dash-sidebar-lower').prepend('<div><h4>Students</h4></div><div class="list-group" id="students-for-lesson"></div>');
            _.each(students, function (student) {
                if (router.teacherStudentWorkRequestId && router.teacherStudentWorkRequestId == parseInt(student['fields']['userId'])) {
                    $('#students-for-lesson').append('<a href="#teacher/' + courseId + '/lesson/' + json.id + '/student/' + student['fields']['userId'] + '" class="list-group-item active student-tab" id="student-tab-' + student['fields']['userId'] + '"></i>' + student['fields']['username'] + '</a>');
                }
                else {
                    $('#students-for-lesson').append('<a href="#teacher/' + courseId + '/lesson/' + json.id + '/student/' + student['fields']['userId'] + '" class="list-group-item student-tab" id="student-tab-' + student['fields']['userId'] + '"></i>' + student['fields']['username'] + '</a>');
                }
            }, this);


            // add lesson name to top

            //create a list of students on the side
        });

        return this;
    }

});