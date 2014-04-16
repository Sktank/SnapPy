/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/13/14
 * Time: 11:52 AM
 * To change this template use File | Settings | File Templates.
 */

var SnappyHeader = '<h5 id="snappy-title">SnapPy: A Graphical Python Tutorial</h5>'

var AppRouter = Backbone.Router.extend({

    routes:{
        "":"lessonsList",
        "solo":"lessonsList",
        "solo/:id":"lessonDetails",
        "solo/:id/snap":"snap",
        "teacher":"teacherList",
        "teacher/:id":"teacherCourseDetails",
        "teacher/:id/lesson/:lid":"teacherLessonDetails",
        "teacher/:id/lesson/:lid/student/:sid":"teacherLessonStudentWork",
        "student":"studentList",
        "student/:id":"studentCourseDetails",
        "student/:id/lesson/:lid":"studentLessonDetails"
    },


    //===========================================================================================
    //                                         Lesson Tab
    //===========================================================================================

    lessonsList:function () {
        dashUtils.clearNavBtns();
        dashUtils.checkDash();
        $("#prev-btn").html(SnappyHeader);
        $('#dash-main').removeClass("hacky-hide");
        if (this.teachingList) {
            delete this.teachingList;
        }
        if (this.studentClassList) {
            delete this.studentClassList;
        }
        var self = this;
        $('#dash-main').empty();
        $('#dash-sidebar-lower').empty();
        this.lessonList = new LessonCollection();
        this.lessonList.fetch({
            success: function(collection){
                // This code block will be triggered only after receiving the data.
                self.lessonListView = new LessonListView({model:self.lessonList});
                $('#dash-main').html(self.lessonListView.render().el);
                if (self.lessonRequestedId) {
                    self.lessonDetails(self.lessonRequestedId);
                    delete self.lessonRequestedId;
                }
                else if (self.snapRequestedId) {
                    self.snap(self.snapRequestedId);
                    delete self.snapRequestedId;
                }
            }
        });
    },

    lessonDetails:function (id) {
        dashUtils.clearNavBtns();
        $("#prev-btn").html(SnappyHeader);
        $('#dash-main').removeClass("hacky-hide");
        var remake = dashUtils.checkDash();
        var self = this;
        if (this.lessonList && !remake) {
            this.lesson = this.lessonList.get(id);
            this.lessonView = new LessonView({model:this.lesson});
            $('.container-details').remove();
            $('.active-container').removeClass("active-container");
            $('#dash-list-item-container-' + id).addClass('active-container').append(self.lessonView.render().el);
        }
        else {
            this.lessonRequestedId = id;
            this.lessonsList();
        }
    },

    snap:function (id) {
        dashUtils.clearNavBtns();
        $('#dash-main').removeClass("hacky-hide");
        var self = this;
        // we want to get all the appropriate models loaded before we start
        if (this.lessonList) {
            this.lesson = this.lessonList.get(id);
            this.lessonIndex = this.lessonList.indexOf(this.lesson);
            this.nextLesson = this.lessonList.at(this.lessonIndex + 1);
            this.prevLesson = this.lessonList.at(this.lessonIndex - 1);
            this.snapView = new SnapView({model:this.lesson, nextModel: this.nextLesson, prevModel: this.prevLesson});
            $('#content').fadeOut(500).promise().done(function() {
                $('#content').html(self.snapView.render().el);
            });
        }
        else {
            this.snapRequestedId = id;
            this.lessonsList()
        }

    },

    //===========================================================================================
    //                                         Teacher Tab
    //===========================================================================================

    teacherList: function () {
        dashUtils.clearNavBtns();
        $('#dash-main').removeClass("hacky-hide");
        dashUtils.checkDash();
        $("#prev-btn").html(SnappyHeader);
        if (this.lessonList) {
            delete this.lessonList;
        }
        if (this.studentClassList) {
            delete this.studentClassList;
        }
        var self = this;
        $('#dash-main').empty();
        $('#dash-sidebar-lower').empty();
        $('#dash-main').append('<div id="teacher-class-list-container"></div>');
        $('#dash-main').append('<div id="teacher-register-form-container"></div>');
        dashUtils.generateTeacherList();
        dashUtils.generateTeacherCourseRegisterForm();
    },

    teacherCourseDetails: function(id) {
        dashUtils.clearNavBtns();
        $("#prev-btn").html(SnappyHeader);
        var remake = dashUtils.checkCourseList(id);
        $('#dash-main').removeClass("hacky-hide");
        var self = this;
        //console.log("YO");
        if (this.teachingList && !remake) {
            //console.log("has the teaching list");
            this.teacherCourse = this.teachingList.get(id);
            //console.log(this.teacherCourse);
            this.teacherCourseView = new TeacherCourseView({model:this.teacherCourse});
            $('.container-details').remove();
            $('.active-container').removeClass("active-container");
            $('#dash-list-item-container-' + id).addClass('active-container').append(self.teacherCourseView.render().el);

        }
        else {
            //console.log("does not have the teaching list");
            this.teacherCourseRequestedId = id;
            this.teacherList();
        }
    },

    teacherLessonDetails: function(id, lid) {
        dashUtils.clearNavBtns();
        dashUtils.checkDash();
        $("#prev-btn").html(SnappyHeader);
        var self = this;
        this.teacherLessonList = new CourseLessonCollection();
        $('#dash-main').removeClass("hacky-hide");

        $(".main-tab").removeClass("active");
        $("#teacher-list-tab").addClass("active");

        this.teacherLessonList.fetch({
            success: function(collection){
                //console.log("teacher lesson details" + id + "," + lid);
                self.teacherLesson = self.teacherLessonList.get(lid);
                self.teacherLessonView = new TeacherLessonView({model:self.teacherLesson, course_id:id});
                $('#dash-main').html(self.teacherLessonView.render().el);

                if (self.teacherStudentWorkRequestId) {
                    //console.log("back to student work");
                    self.teacherLessonStudentWork(id, lid, self.teacherStudentWorkRequestId)
                }
            }
        });

    },

    teacherLessonStudentWork: function(id, lid, sid) {
        dashUtils.clearNavBtns();
        $("#prev-btn").html(SnappyHeader);
        var self = this;
        $('#dash-main').removeClass("hacky-hide");
        if (self.teacherLesson) {
            if (self.teacherStudentWorkRequestId) {
                delete self.teacherStudentWorkRequestId;
            }
            //console.log("now I have a lesson");
            $(".student-tab").removeClass("active");
            $("#student-tab-" + sid).addClass("active");

            this.studentWork = new TeacherLessonStudentWork({model:this.teacherLesson, student_id:sid, course_id:id});
            $("#dash-main").html(self.studentWork.render().el);
        }
        else {
            //console.log("no lesson");
            self.teacherStudentWorkRequestId = sid;
            self.teacherLessonDetails(id, lid);
        }
    },

    //===========================================================================================
    //                                         Student Tab
    //===========================================================================================

    studentList: function () {
        dashUtils.clearNavBtns();
        dashUtils.checkDash();
        $("#prev-btn").html(SnappyHeader);
        if (this.teachingList) {
            delete this.teachingList;
        }
        if (this.lessonList) {
            delete this.lessonList;
        }
        var self = this;
        $('#dash-main').removeClass("hacky-hide");
        $('#dash-main').empty();
        $('#dash-sidebar-lower').empty();
        $('#dash-main').append('<div id="student-class-list-container"></div>');
        $('#dash-main').append('<div id="student-class-search-container"></div>');
        $('#dash-main').append('<div id="student-class-enrollment-container"></div>');
        dashUtils.generateStudentList();
        dashUtils.generateStudentEnrollmentQueue();
    },

    studentCourseDetails: function(id) {
        dashUtils.clearNavBtns();
        $("#prev-btn").html(SnappyHeader);
        var remake = dashUtils.checkDash();
        $('#dash-main').removeClass("hacky-hide");
        var self = this;
        if (this.studentClassList && !remake) {
            if (this.studentCourseRequestedId) {
                delete this.studentCourseRequestedId;
            }
            this.studentCourse = this.studentClassList.get(id);
            this.studentCourseView = new StudentCourseView({model:this.studentCourse});
            $('.container-details').remove();
            $('.active-container').removeClass("active-container");
            $('#dash-list-item-container-' + id).addClass('active-container').append(self.studentCourseView.render().el);
        }
        else {
            this.studentCourseRequestedId = id;
            this.studentList();
        }
    },


    studentLessonDetails: function(id, lid) {
        dashUtils.clearNavBtns();
        $("#prev-btn").html(SnappyHeader);
        var self = this;
        $('#dash-main').removeClass("hacky-hide");
        this.studentLessonList = new CourseLessonCollection();
        $(".main-tab").removeClass("active");
        $("#student-list-tab").addClass("active");
        //console.log("student lesson details" + id + "," + lid);
        this.studentLessonList.fetch({
            success: function(collection){
                //console.log("student lesson details" + id + "," + lid);
                self.studentLesson = self.studentLessonList.get(lid);
                //console.log(self.studentLessonList);
                self.studentLessonView = new StudentLessonView({model:self.studentLesson, course:id});
                $('#content').fadeOut(500).promise().done(function() {
                    $('#content').html(self.studentLessonView.render().el);
                });

            }
        });

    }


});

var app = new AppRouter();
Backbone.history.start();
