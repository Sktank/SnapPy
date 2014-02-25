/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/18/14
 * Time: 11:16 PM
 * To change this template use File | Settings | File Templates.
 */
var snapHeight = 800;
var snapWidth = 1100;

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
        window.world = new WorldMorph(document.getElementById('world'), false);
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
                                                                $.getScript('static/js/codemirror2.js').done(function() {
                                                                    $.getScript('static/js/executeVisualizer.js').done(function() {
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
            $('#student-class-search-container').html(new StudentClassSearchView({model:self.allClassList}).render().el);
        }
    })

};

var generateStudentEnrollmentQueue = function() {
    console.log("here2");
    var self = window.app;
    if (!self.enrollmentQueueList) {
        self.enrollmentQueueList = new EnrollmentQueueCollection();
    }
    $('#student-class-enrollment-container').html(new StudentClassEnrollmentQueueView({model:self.enrollmentQueueList}).render().el);
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



//#open:<project name="Untitled" app="Snap! 4.0, http://snap.berkeley.edu" version="1"><notes></notes><thumbnail>data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAAB4CAYAAAB1ovlvAAADCElEQVR4Xu3VMW5aARRE0e992L1ZDgUbcuMNeT14IRRJ5CJy4yQaRhnJOr+F9544XMHDj1/P4SEwEngQ4Eje2Q8BAQphKiDAKb/jAtTAVECAU37HBaiBqYAAp/yOC1ADUwEBTvkdF6AGpgICnPI7LkANTAUEOOV3XIAamAoIcMrvuAA1MBUQ4JTfcQFqYCogwCm/4wLUwFRAgFN+xwWogamAAKf8jgtQA1MBAU75HRegBqYCApzyOy5ADUwFBDjld1yAGpgKCHDK77gANTAVEOCU33EBamAqIMApv+MC1MBUQIBTfscFqIGpgACn/I4LUANTAQFO+R0XoAamAgKc8jsuQA1MBQQ45XdcgBqYCghwyu+4ADUwFRDglN9xAWpgKiDAKb/jAtTAVECAU37HBaiBqYAAp/yOC1ADUwEBfsF/Op2Ol5eX43K5TL+g735cgH/4hs/n8+9Xr9fr8fb2djw9PX33Jv7r5xPgX7g/R/j5rbfb7SNIz30CAhTgfQXdOS3Af/wLfn9///jFe3x8vJPc+GcBAX7Rw/Pz8/H6+np89Rcso46AADuOtoQCAgzhjHUEBNhxtCUUEGAIZ6wjIMCOoy2hgABDOGMdAQF2HG0JBQQYwhnrCAiw42hLKCDAEM5YR0CAHUdbQgEBhnDGOgIC7DjaEgoIMIQz1hEQYMfRllBAgCGcsY6AADuOtoQCAgzhjHUEBNhxtCUUEGAIZ6wjIMCOoy2hgABDOGMdAQF2HG0JBQQYwhnrCAiw42hLKCDAEM5YR0CAHUdbQgEBhnDGOgIC7DjaEgoIMIQz1hEQYMfRllBAgCGcsY6AADuOtoQCAgzhjHUEBNhxtCUUEGAIZ6wjIMCOoy2hgABDOGMdAQF2HG0JBQQYwhnrCAiw42hLKCDAEM5YR0CAHUdbQgEBhnDGOgIC7DjaEgoIMIQz1hEQYMfRllBAgCGcsY6AADuOtoQCAgzhjHUEBNhxtCUUEGAIZ6wjIMCOoy2hgABDOGMdAQF2HG0JBQQYwhnrCAiw42hLKPAT12n8qPmYkCQAAAAASUVORK5CYII=</thumbnail><stage name="Stage" costume="0" tempo="60" threadsafe="false" codify="false" scheduled="false" id="1"><pentrails>data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAeAAAAFoCAYAAACPNyggAAAOhUlEQVR4Xu3VwQkAAAjEMN1/abewn7jAQRC64wgQIECAAIF3gX1fNEiAAAECBAiMAHsCAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQICLAfIECAAAECgYAAB+gmCRAgQICAAPsBAgQIECAQCAhwgG6SAAECBAgIsB8gQIAAAQKBgAAH6CYJECBAgIAA+wECBAgQIBAICHCAbpIAAQIECAiwHyBAgAABAoGAAAfoJgkQIECAgAD7AQIECBAgEAgIcIBukgABAgQIHLFxAWmhEwHPAAAAAElFTkSuQmCC</pentrails><costumes><list id="2"></list></costumes><sounds><list id="3"></list></sounds><variables></variables><blocks></blocks><scripts></scripts><sprites><sprite name="Sprite" idx="1" x="0" y="0" heading="90" scale="1" rotation="1" draggable="true" costume="0" color="80,80,80" pen="tip" id="8"><costumes><list id="9"></list></costumes><sounds><list id="10"></list></sounds><variables></variables><blocks></blocks><scripts></scripts></sprite></sprites></stage><hidden></hidden><headers></headers><code></code><blocks></blocks><variables></variables></project>