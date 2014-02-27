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
        $("#dash-sidebar-right").append("<h4 id='lesson-guide-preview-header'>Lesson Guide Preview</h4><div \i" +
            "d='lesson-guide-preview'><h4>Welcome!</h4><p id='lesson-guide-preview-text'></p></div>");
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

        $( document ).on( "focus", "#create-lesson-guide", function() {
            $("#lesson-guide-preview-header").css("display", "block");
            $("#lesson-guide-preview-header").css("margin-top", $("#create-lesson-guide").position()['top'] -
                200 + "px");
            $("#lesson-guide-preview").css("display", "block");
        });

        $( document ).on( "focusout", "#create-lesson-guide", function() {
            $("#lesson-guide-preview-header").css("display", "none");
            $("#lesson-guide-preview").css("display", "none");

        });

        $( document ).on( "keyup", "#create-lesson-guide", function() {
            $("#lesson-guide-preview-text").text($('#create-lesson-guide').val());
        });

        return this;
    }

});

window.TeacherCourseView = Backbone.View.extend({

    template:_.template($('#teacher-course-details').html()),

    render:function (eventName) {
        console.log("course view");
        var json = this.model.toJSON();
        var promise = dashUtils.getLessons(json.id);
        var self = this;
        var addLessonQueue = [];
        var removeLessonQueue = [];
        $(self.el).addClass("container-details");
//        $(self.el).append('<h5>Lessons</h5>');
        $(self.el).append(self.template(json));
        promise.success(function (data) {
            var lessons = $.parseJSON(data);
            var currentLessons = lessons[0];
            var separateLessons = lessons[1];
            console.log(lessons);


    //TODO: Current Lessons and Separate Lessons should really call the same function because so much duplicate code!
    //TODO: Shit looks gross right now.

            if (currentLessons.length > 0) {
                _.each(currentLessons, function (lesson) {
                    $(self.el).append('<a id="course-' + json.id + '-lesson-' + lesson['pk'] + '" href="#teacher/'
                        + json.id + '/lesson/' + lesson['pk'] + '">' + lesson['fields']['name'] + '</a><br>');

                    // This is for the lesson manager modal
                    $('#course-current-lessons').append('<a class="list-group-item clicker lessonListItem" \i' +
                        'd="current-lesson-' + json.id + "-" + lesson['pk'] + '"><p>' + lesson['fields']['name'] +
                        '</p></a>');
                    $('#lessonManagerModal-' + json.id).on("click", '#current-lesson-' + json.id + "-" + lesson['pk'],
                        function() {
                        console.log(lesson['pk']);
                        if ($('#current-lesson-' + json.id + "-" + lesson['pk']).hasClass('active')) {
                            var i = removeLessonQueue.indexOf(lesson['pk']);
                            if(i != -1) {
                                removeLessonQueue.splice(i, 1);
                            }
                            $('#current-lesson-' + json.id + "-" + lesson['pk']).removeClass('active');
                        }
                        else {
                            removeLessonQueue.push(lesson['pk']);
                            $('#current-lesson-' + json.id + "-" + lesson['pk']).addClass('active');
                        }
                    });
                }, this);
            }
            else {
                $(self.el).append('<p>Empty</p>');
                $('#course-current-lessons').append('<p>Empty</p>');
            }

            if (separateLessons.length > 0) {
                _.each(separateLessons, function (lesson) {
                    $('#course-separate-lessons').append('<a class="list-group-item clicker lessonListItem" \i' +
                        'd="seperate-lesson-' + json.id + "-" + lesson['pk'] + '"><p>' + lesson['fields']['name'] +
                        '</p></a>');
                    $('#lessonManagerModal-' + json.id).on("click", '#seperate-lesson-' + json.id + "-" + lesson['pk'],
                        function() {
                        console.log(lesson['pk']);
                        if ($('#seperate-lesson-' + json.id + "-" + lesson['pk']).hasClass('active')) {
                            var i = addLessonQueue.indexOf(lesson['pk']);
                            if(i != -1) {
                                addLessonQueue.splice(i, 1);
                            }
                            $('#seperate-lesson-' + json.id + "-" + lesson['pk']).removeClass('active');
                        }
                        else {
                            addLessonQueue.push(lesson['pk']);
                            $('#seperate-lesson-' + json.id + "-" + lesson['pk']).addClass('active');
                        }
                    });
                }, this);

            }
            else {
                $('#course-separate-lessons').append("<p>Empty</p>")
            }



            $('#lessonManagerModal-' + json.id).on("click", "#save-lesson-updates-" + json.id, function() {
                if ($("#save-lesson-updates-" + json.id).prop("disabled"))
                    return false;
                $("#save-lesson-updates-" + json.id).prop("disabled", true);
                dashUtils.updateLessonsForCourse(json.id, removeLessonQueue, addLessonQueue);
                removeLessonQueue = [];
                addLessonQueue = [];
                $('#lessonManagerModal-' + json.id).find(".active").removeClass("active");
            });

            $("#lessonManagerModal-" + json.id).on("hide.bs.modal", function() {
                removeLessonQueue = [];
                addLessonQueue = [];
                $('#lessonManagerModal-' + json.id).find(".active").removeClass("active");
            });


        });
        return this;
    }

});

window.TeacherLessonView = Backbone.View.extend({

    initialize:function (options) {
        this.model.bind("reset", this.render, this);
        this.options = options || {};
    },


//    template:_.template($('#teacher-lesson-details').html()),

    render:function (eventName) {

        // get the course and list of students for that course of the lesson.
        var json = this.model.toJSON();
        var self = this;
        var router = window.app;
        var course_id = self.options.course_id;
        console.log(json);

        console.log(this.model);
        var promise = dashUtils.getCourseAndStudents(course_id);

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

            var remake = dashUtils.checkStudentList();
            if (remake) {
                var append_promise = $('#dash-sidebar-lower').prepend('<div><h4>Students</h4></div><div \c' +
                    'lass="list-group"\ id="students-for-lesson"></div>');
                _.each(students, function (student) {
                    if (router.teacherStudentWorkRequestId && router.teacherStudentWorkRequestId ==
                        parseInt(student['fields']['userId'])) {
                        $('#students-for-lesson').append('<a href="#teacher/' + courseId + '/lesson/' + json.id +
                            '/student/' + student['fields']['userId'] +
                            '" class="list-group-item active student-tab" id="student-tab-' +
                            student['fields']['userId'] + '"></i>' + student['fields']['username'] + '</a>');
                    }
                    else {
                        $('#students-for-lesson').append('<a href="#teacher/' + courseId + '/lesson/' + json.id +
                            '/student/' + student['fields']['userId'] +
                            '" class="list-group-item student-tab" id="student-tab-' + student['fields']['userId'] +
                            '"></i>' + student['fields']['username'] + '</a>');
                    }
                }, this);
            }
        });

        return this;
    }

});



window.TeacherLessonStudentWork = Backbone.View.extend({

    initialize:function (options) {
        this.model.bind("reset", this.render, this);
        this.options = options || {};
    },

    template:_.template($('#teacher-student-lesson-template').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        var student_id = this.options.student_id;
        $('#current-lesson').text(json.name);
        $(this.el).html(this.template(json));
        $('#dash-main').show();
        dashUtils.loadSnap(json.id, student_id);
        return this;
    }
});