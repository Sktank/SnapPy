/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/18/14
 * Time: 11:16 PM
 * To change this template use File | Settings | File Templates.
 */
var snapHeight = 800;
var snapWidth = 1100;

(function( dashUtils, $, undefined ) {

    //===========================================================================================
    //    Functions to check if we need to render specific elements before rendering view
    //===========================================================================================

    dashUtils.checkDash = function() {
        var dashMain = $("#dash-main");
        if (!dashMain.length) {
            console.log(dashMain.length);
            $('#content').html('<hr id="header-line"></div>\<' +
                'div class="row"><div class="col-md-2" id="dash-sidebar"><h4>Dash Sidebar</h4><div \c' +
                'lass="list-group"><a href="#teacher" class="list-group-item main-tab" id="teacher-list-tab">\<' +
                'i class="fa fa-leaf"></i> Teacher</a><a href="#student" class="list-group-item main-tab"\ ' +
                'id="student-list-tab"><i class="fa fa-compass"></i> Student</a><a href="#solo" \c' +
                'lass="list-group-item main-tab" id="lesson-list-tab"><i class="fa fa-user"></i> Individual</a></div>\<' +
                'div id="dash-sidebar-lower"></div></div><div class="col-md-8"><div id="dash-main"><h3>Lessons</h3>\<' +
                'div class="recommend"><p class="recommend-header"><b>Recommended</b></p></div><div id="lesson-list"></div>\<' +
                '/div></div><div class="col-md-2"><div id="dash-sidebar-right"></div></div></div>');
            return 1;
        }
        else{
            return 0;
        }
    };

    dashUtils.checkCourseList = function(id) {
        var courseContainer = $('#dash-list-item-container-' + id);
        if (!courseContainer.length) {
            return 1;
        }
        else {
            return 0;
        }
    };

    dashUtils.checkStudentList = function() {
        var studentList = $('#students-for-lesson');
        if (!studentList.length) {
            return 1;
        }
        else {
            return 0;
        }
    };

    dashUtils.clearNavBtns = function() {
        $("#home-btn").empty();
        $("#next-btn").empty();
        $("#prev-btn").empty();
        $("#current-lesson").empty();
    };

    //===========================================================================================
    //              Functions for updating forms with errors or success messages
    //===========================================================================================

    dashUtils.updateCourseForm = function(data) {
        $('#course-name-group').removeClass('has-error');
        $('#course-name-error').empty();
        $('#update-form-message').empty();
        console.log("here6");
        if (data == "Enrollment Successful!") {
            console.log("here7");
            $('#update-form-message').text(data);
            $('#course-name').val("");
        }
        else {
            console.log("here8");
            $('#course-name-group').addClass('has-error');
            $('#course-name-error').append('<li>' + data + '</li>');
        }
    };

    dashUtils.updateLessonForm = function(data) {
        $('#lesson-name-group').removeClass('has-error');
        $('#lesson-guide-group').removeClass('has-error');
        $('#lesson-name-error').empty();
        $('#lesson-guide-error').empty();
        $('#lesson-success-message').empty();
        console.log(data);
        if ($.isEmptyObject(data)) {
            console.log("created");
            $('#lesson-name').val("");
            $('#create-lesson-guide').val("");
            $('#lesson-description').val("");
            $('#lesson-guide-preview-text').empty();
            $('#lesson-difficulty-group').find("input").prop("checked", false);
            $('#lesson-success-message').text("Lesson Created!");
        }
        if (data['name']) {
            console.log(data['name']);
            $('#lesson-name-group').addClass('has-error');
            $('#lesson-name-error').text(data['name']);
        }
        if (data['guide']) {
            console.log(data['guide']);
            $('#lesson-guide-group').addClass('has-error');
            $('#lesson-guide-error').text(data['guide']);
        }

    };

    dashUtils.updateSearchTeacherList = function(data) {
        console.log(data);
        var json = $.parseJSON(data);
        if (json == -1) {
            $("#courses-by-teacher-list").append('<h4 class="search-error">Please Enter A Username</h4>');
        }
        else if (json == -2) {
            $("#courses-by-teacher-list").append('<h4 class="search-error">That Username Does Not Exist</h4>');
        }
        else if (json.length == 0) {
            $("#courses-by-teacher-list").append('<h4 class="search-error">That User Is Not Teaching Any Classes</h4>');
        }
        else {
            _.each(json, function (course) {
                $("#courses-by-teacher-list").append(new StudentClassSearchItemView({model:course['fields'], id:course['pk']}).render().el);
            }, this);
        }
    };

    dashUtils.updateSearchNameList = function(data) {
        console.log(data);
        var json = $.parseJSON(data);
        if (json == -1) {
            $("#courses-by-name-list").append('<h4 class="search-error">Please Enter A Search</h4>');
        }
        else if (json.length == 0) {
            $("#courses-by-name-list").append('<h4 class="search-error">No Courses Matched Your Search</h4>');
        }
        else {
            _.each(json, function (course) {
                $("#courses-by-name-list").append(new StudentClassSearchItemView({model:course['fields'], id:course['pk']}).render().el);
            }, this);
        }
    };

    dashUtils.refreshList = function(listId) {
        var list = $('#' + listId);
        _.each(list.find('.class-search-item'), function(child) {
            console.log(child);
            var jChild = $(child);
            var id = parseInt(child.id.split("-")[2]);
            console.log(id);
            console.log(window.app.enrollmentQueueList);
            if (jChild.hasClass('queued_class') && !(window.app.enrollmentQueueList.findWhere({ id: id }))) {
                jChild.removeClass('queued_class');
            }
            else if (!jChild.hasClass('queued_class') && (window.app.enrollmentQueueList.findWhere({ id: id }))) {
                jChild.addClass('queued_class');
            }
        });
    };

    //===========================================================================================
    //              Functions for creating new models or updating models
    //===========================================================================================

    dashUtils.submitCourse = function() {
        console.log("here5");
        var self = this;
        if ($(this).prop("disabled"))
            return false;
        $(this).prop("disabled", true);
        $.ajax({
            crossDomain: false,
            type: "POST",
            data: {name: $('#course-name').val()},
            url: "register_course"
        }).success(function(data) {
                console.log(data);
                dashUtils.updateCourseForm(data);
                dashUtils.generateTeacherList();
                $(self).removeProp("disabled");
            });
    };

    dashUtils.submitLesson = function() {
        var self = this;
        if ($(this).prop("disabled"))
            return false;
        $(this).prop("disabled", true);
        $.ajax({
            crossDomain: false,
            type: "POST",
            data: {
                name: $('#lesson-name').val(),
                description: $('#lesson-description').val(),
                difficulty: $('input[name=lesson-difficulty]:checked', '#create-lesson-form').val(),
                guide: $('#create-lesson-guide').val()
            },
            url: "create_lesson"
        }).success(function(data) {
                var data = $.parseJSON(data);
                dashUtils.updateLessonForm(data);
                dashUtils.generateTeacherList();
                window.location.href = "#teacher";
                $(self).removeProp("disabled");
            });
    };

    dashUtils.clearStudentSearch = function() {
        $('#student_search_navs').children('li').removeClass("active");
        $("#courses-by-name").css('display', 'none');
        $("#all-courses").css('display', 'none');
        $("#courses-by-teacher").css('display', 'none');
    };

    dashUtils.addCourseToEnrollmentQueue = function(model) {
        var self = this;
        console.log("adding to queue");
        console.log(model);
        if ($(this).prop("disabled"))
            return false;
        $(this).prop("disabled", true);
        window.app.enrollmentQueueList.add(model);

        $(self).removeProp("disabled");
        dashUtils.generateStudentEnrollmentQueue();
    };

    dashUtils.removeCourseFromEnrollmentQueue = function(model) {
        var self = this;
        console.log("removing from queue");
        console.log(model);
        if ($(this).prop("disabled"))
            return false;
        $(this).prop("disabled", true);
        window.app.enrollmentQueueList.remove(model);

        $(self).removeProp("disabled");
        dashUtils.generateStudentEnrollmentQueue();
    };

    dashUtils.clearEnrollmentQueue = function() {
        console.log("here1");
        var self = window.app;
        self.enrollmentQueueList = new EnrollmentQueueCollection();
        $(".unenrolled_class").removeClass("queued_class");
        dashUtils.generateStudentEnrollmentQueue();
    };

    dashUtils.enrollCourses = function() {
        console.log("enrolling");
        var ids = [];
        _.each(window.app.enrollmentQueueList.models, function(course) {
            ids.push(course.toJSON().id)
        });
        var self = this;
        console.log(ids);
        if ($(this).prop("disabled"))
            return false;
        $(this).prop("disabled", true);
        $.ajax({
            crossDomain: false,
            type: "POST",
            data: {ids: ids},
            url: "enroll_courses"
        }).success(function(data) {
                var code = $.parseJSON(data)['code'];
                if (code == 0) {

                }
                else {

                }
                // remove from queue
                window.app.enrollmentQueueList = new EnrollmentQueueCollection();
                $(self).removeProp("disabled");
                window.app.studentList();
                window.location.href = "#student"

            });
    };

    dashUtils.updateLessonsForCourse = function(course_id, remove_ids, add_ids) {
        console.log(course_id);
        console.log(remove_ids);
        console.log(add_ids);
        console.log("updating lessons");
        var self = this;
        $.ajax({
            crossDomain: false,
            type: "POST",
            data: {
                course_id: course_id,
                remove_ids: remove_ids,
                add_ids: add_ids
            },
            url: "manage_course_lessons"
        }).success(function(data) {
                $("#save-lesson-updates-" + course_id).removeProp("disabled");
                $("#lessonManagerModal-" + course_id).modal('hide');
                $("#lessonManagerModal-" + course_id).on("hidden.bs.modal", function(){
                    window.app.teacherCourseRequestedId = course_id;
                    dashUtils.generateTeacherList()
                });
            });

        return 0;
    };

    dashUtils.saveSnap = function(name, snapSerial, lessonId) {
        $.ajax({
            crossDomain: false,
            type: "POST",
            data: {
                name: name,
                lesson_id: lessonId,
                serial: snapSerial
            },
            url: "save_snap"
        }).success(function(data) {
                console.log(data);
                window.ide.showMessage('Saved!', 1);
            });
    };

    //===========================================================================================
    //              Functions specifically dealing with loading the snap app
    //===========================================================================================

    dashUtils.startSnap = function(lesson_id, student_id) {
        var snaps_promise = dashUtils.getSnaps(lesson_id, student_id);
        snaps_promise.success(function() {
            console.log(snaps_promise);
            var editorContainer = document.createElement("iframe");
            editorContainer.id = "codeEditor";
            editorContainer.src = "vis";
            editorContainer.style.display = "none";
            $('#snap-app')[0].appendChild(editorContainer);
            var worldCanvas = document.getElementById('world');
            worldCanvas.width = snapWidth;
            worldCanvas.height = snapHeight;
            if (student_id) {
                window.world = new WorldMorph(document.getElementById('world'), false, true);
            }
            else {
                window.world = new WorldMorph(document.getElementById('world'), false, false);

            }
            window.ide = new IDE_Morph();
            window.lessonId = lesson_id;
            ide.codemirror = editorContainer;
            ide.openIn(world);
            setInterval(loop, 1);

            //load if we have previous snaps
//            console.log(snaps_promise.responseText);
            if (snaps_promise.responseText != "0")
            {
                var resp = $.parseJSON(snaps_promise.responseText);
                var str = resp[0]['fields']['serial'];
                console.log("loading...");
                ide.openProjectString(str);
            }
            else {
                console.log("done");
            }
        });
    };

    dashUtils.loadSnap = function(lesson_id, student_id) {
        $.getScript('static/js/snap/morphic.js').done(function() {
            $.getScript('static/js/snap/widgets.js').done(function () {
                $.getScript('static/js/snap/blocks.js').done(function() {
                    $.getScript('static/js/snap/threads.js').done(function() {
                        $.getScript('static/js/snap/objects.js').done(function() {
                            $.getScript('static/js/snap/gui.js').done(function() {
                                $.getScript('static/js/snap/paint.js').done(function() {
                                    $.getScript('static/js/snap/lists.js').done(function() {
                                        $.getScript('static/js/snap/byob.js').done(function() {
                                            $.getScript('static/js/snap/xml.js').done(function() {
                                                $.getScript('static/js/snap/store.js').done(function() {
                                                    $.getScript('static/js/snap/locale.js').done(function() {
                                                        $.getScript('static/js/snap/cloud.js').done(function() {
                                                            $.getScript('static/js/snap/sha512.js').done(function() {
                                                                $.getScript('static/js/snap/codemirror1.js').done(function() {
                                                                    $.getScript('static/js/snap/codemirror2.js').done(function()
                                                                    {
                                                                        $.getScript('static/js/snap/executeVisualizer.js').done(
                                                                            function() {
                                                                                dashUtils.startSnap(lesson_id, student_id);
                                                                            });
                                                                    });
                                                                });
                                                            });
                                                        });
                                                    });
                                                });
                                            });
                                        });
                                    });
                                });
                            });
                        });
                    });
                });
            });
        });
    };

    function loop() {
        world.doOneCycle();
    }

    //===========================================================================================
    //              Functions for rendering dashboard subviews
    //===========================================================================================

    dashUtils.generateTeacherList = function() {
        var self = window.app;
        self.teachingList = new TeacherCourseCollection();
        self.teachingList.fetch({
            success: function(collection) {
                self.teacherCourseListView = new TeacherCourseListView({model:self.teachingList});
                $('#teacher-class-list-container').html(self.teacherCourseListView.render().el);
                $("#teacher-register-class-btn").click(function() {
                    console.log("new class");
                    dashUtils.submitCourse();
                });
                $("#create-lesson-btn").click(function() {
                    console.log("new lesson");
                    dashUtils.submitLesson();
                });

                if (self.teacherCourseRequestedId) {
                    console.log("back to detail");
                    self.teacherCourseDetails(self.teacherCourseRequestedId);
                    delete self.teacherCourseRequestedId;
                }
            }
        });
    };

    dashUtils.generateTeacherCourseRegisterForm = function() {
        $('#teacher-register-form-container').html(new TeacherCourseRegisterView().render().el);

    };


    dashUtils.generateStudentList = function() {
        var self = window.app;
        self.studentClassList = new StudentCourseCollection();
        self.studentClassList.fetch({
            success: function(collection) {
                dashUtils.generateStudentClassSearch();
                self.studentCourseListView = new StudentCourseListView({model:self.studentClassList});
                $('#student-class-list-container').html(self.studentCourseListView.render().el);
                $("#student-register-class-btn").click(function() {
                    console.log("new class");
                    dashUtils.submitCourse();
                });
                if (self.studentCourseRequestedId) {
                    self.studentCourseDetails(self.studentCourseRequestedId);
                    delete self.studentCourseRequestedId;
                }
            }
        });
    };

    dashUtils.generateStudentClassSearch = function() {
        var self = window.app;
        self.allClassList = new CourseCollection();
        self.allClassList.fetch({
            success: function(collection) {
                $('#student-class-search-container').html(new StudentClassSearchView(
                    {model:self.allClassList}).render().el
                );
            }
        })

    };

    dashUtils.generateStudentEnrollmentQueue = function() {
        console.log("here2");
        var self = window.app;
        if (!self.enrollmentQueueList) {
            self.enrollmentQueueList = new EnrollmentQueueCollection();
        }
        $('#student-class-enrollment-container').html(new StudentClassEnrollmentQueueView(
            {model:self.enrollmentQueueList}).render().el
        );
    };

    //===========================================================================================
    //                       Functions to access models with ajax calls
    //===========================================================================================

    dashUtils.getCoursesByName = function(name) {
        return $.ajax({
            crossDomain: false,
            type: "GET",
            data: {name: name},
            url: "get_courses_by_name"
        });
    };

    dashUtils.getCoursesByTeacher = function(name) {
        return $.ajax({
            crossDomain: false,
            type: "GET",
            data: {name: name},
            url: "get_courses_by_teacher"
        });
    };

    dashUtils.getLessons = function(id) {
        return $.ajax({
            crossDomain: false,
            type: "GET",
            data: {course_id: id},
            url: "get_lessons"
        });
    };

    dashUtils.getCourseAndStudents = function(id) {
        return $.ajax({
            crossDomain: false,
            type: "GET",
            data: {course_id: id},
            url: "lesson_get_course_and_students"
        });
    };

    dashUtils.getSnaps = function(id, student_id) {
        console.log(id);
        return $.ajax({
            crossDomain: false,
            type: "GET",
            data: {
                lesson_id: id,
                student_id:student_id
            },
            url: "lesson_get_snaps"
        });
    };

}( window.dashUtils = window.dashUtils || {}, jQuery ));
