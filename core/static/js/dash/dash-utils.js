/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/18/14
 * Time: 11:16 PM
 * To change this template use File | Settings | File Templates.
 */
var snapHeight = 800;
var snapWidth = 1100;

var checkDash = function() {
    var dashMain = $("#dash-main");
    if (!dashMain.length) {
        console.log(dashMain.length);
        $('#content').html('<div class="col-md-12"><h2>Hello '+ username +'!</h2><hr></div>\<' +
            'div class="row"><div class="col-md-2" id="dash-sidebar"><h4>Dash Sidebar</h4><div \c' +
            'lass="list-group"><a href="#teacher" class="list-group-item main-tab" id="teacher-list-tab">\<' +
            'i class="fa fa-leaf"></i> Teacher</a><a href="#student" class="list-group-item main-tab"\ ' +
            'id="student-list-tab"><i class="fa fa-compass"></i> Student</a><a href="#solo" \c' +
            'lass="list-group-item main-tab" id="lesson-list-tab"><i class="fa fa-list"></i> Individual</a></div>\<' +
            'div id="dash-sidebar-lower"></div></div><div class="col-md-8"><div id="dash-main"><h3>Lessons</h3>\<' +
            'div class="recommend"><p class="recommend-header"><b>Recommended</b></p></div><div id="lesson-list"></div>\<' +
            '/div></div><div class="col-md-2"><div id="dash-sidebar-right"></div></div></div>');

        return 1;
    }
    else{
        return 0;
    }
};

var checkCourseList = function(id) {
    var courseContainer = $('#dash-list-item-container-' + id)
    if (!courseContainer.length) {
        return 1;
    }
    else {
        return 0;
    }
};

var updateCourseForm = function(data) {
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

var updateLessonForm = function(data) {
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

var submitCourse = function() {
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
            updateCourseForm(data);
            generateTeacherList();
            $(self).removeProp("disabled");
        });
};

var submitLesson = function() {
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
            updateLessonForm(data);
            generateTeacherList();
            $(self).removeProp("disabled");
        });
};


var saveSnap = function(name, snapSerial, lessonId) {
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

var startSnap = function(lesson_id, student_id) {
    var snaps_promise = getSnaps(lesson_id, student_id);
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
        console.log(snaps_promise.responseText);
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

var loadSnap = function(lesson_id, student_id) {
    $.getScript('static/js/morphic.js').done(function() {
        $.getScript('static/js/widgets.js').done(function () {
            $.getScript('static/js/blocks.js').done(function() {
                $.getScript('static/js/threads.js').done(function() {
                    $.getScript('static/js/objects.js').done(function() {
                        $.getScript('static/js/gui.js').done(function() {
                            $.getScript('static/js/paint.js').done(function() {
                                $.getScript('static/js/lists.js').done(function() {
                                    $.getScript('static/js/byob.js').done(function() {
                                        $.getScript('static/js/xml.js').done(function() {
                                            $.getScript('static/js/store.js').done(function() {
                                                $.getScript('static/js/locale.js').done(function() {
                                                    $.getScript('static/js/cloud.js').done(function() {
                                                        $.getScript('static/js/sha512.js').done(function() {
                                                            $.getScript('static/js/codemirror1.js').done(function() {
                                                                $.getScript('static/js/codemirror2.js').done(function()
                                                                {
                                                                    $.getScript('static/js/executeVisualizer.js').done(
                                                                        function() {
                                                                        startSnap(lesson_id, student_id);
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

var addCourseToEnrollmentQueue = function(model) {
    var self = this;
    console.log("adding to queue");
    console.log(model);
    if ($(this).prop("disabled"))
        return false;
    $(this).prop("disabled", true);
    window.app.enrollmentQueueList.add(model);

    $(self).removeProp("disabled");
    generateStudentEnrollmentQueue();
};


var enrollCourses = function() {
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
        });
};


var generateTeacherList = function() {
    var self = window.app;
    self.teachingList = new TeacherCourseCollection();
    self.teachingList.fetch({
        success: function(collection) {
            self.teacherCourseListView = new TeacherCourseListView({model:self.teachingList});
            $('#teacher-class-list-container').html(self.teacherCourseListView.render().el);
            $("#teacher-register-class-btn").click(function() {
                console.log("new class");
                submitCourse();
            });
            $("#create-lesson-btn").click(function() {
                console.log("new lesson");
                submitLesson();
            });

            if (self.teacherCourseRequestedId) {
                console.log("back to detail");
                self.teacherCourseDetails(self.teacherCourseRequestedId);
                delete self.teacherCourseRequestedId;
            }
        }
    });
};

var generateTeacherCourseRegisterForm = function() {
    $('#teacher-register-form-container').html(new TeacherCourseRegisterView().render().el);

};


var generateStudentList = function() {
    var self = window.app;
    self.studentClassList = new StudentCourseCollection();
    self.studentClassList.fetch({
        success: function(collection) {
            generateStudentClassSearch();
            self.studentCourseListView = new StudentCourseListView({model:self.studentClassList});
            $('#student-class-list-container').html(self.studentCourseListView.render().el);
            $("#student-register-class-btn").click(function() {
                console.log("new class");
                submitCourse();
            });
            if (self.studentCourseRequestedId) {
                self.studentCourseDetails(self.studentCourseRequestedId);
                delete self.studentCourseRequestedId;
            }
        }
    });
};

var generateStudentClassSearch = function() {
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

var generateStudentEnrollmentQueue = function() {
    console.log("here2");
    var self = window.app;
    if (!self.enrollmentQueueList) {
        self.enrollmentQueueList = new EnrollmentQueueCollection();
    }
    $('#student-class-enrollment-container').html(new StudentClassEnrollmentQueueView(
        {model:self.enrollmentQueueList}).render().el
    );
};

var clearEnrollmentQueue = function() {
    console.log("here1");
    var self = window.app;
    self.enrollmentQueueList = new EnrollmentQueueCollection();
    $(".unenrolled_class").removeClass("queued_class");
    generateStudentEnrollmentQueue();
};

var getLessons = function(id) {
    return $.ajax({
        crossDomain: false,
        type: "POST",
        data: {course_id: id},
        url: "get_lessons"
    });
};

var getCourseAndStudents = function(id) {
    return $.ajax({
        crossDomain: false,
        type: "POST",
        data: {course_id: id},
        url: "lesson_get_course_and_students"
    });
};

var getSnaps = function(id, student_id) {
    console.log(id);
    return $.ajax({
        crossDomain: false,
        type: "POST",
        data: {
            lesson_id: id,
            student_id:student_id
        },
        url: "lesson_get_snaps"
    });
};

updateLessonsForCourse = function(course_id, remove_ids, add_ids) {
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
                generateTeacherList()
            });
        });

    return 0;
};
