/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/13/14
 * Time: 8:31 PM
 * To change this template use File | Settings | File Templates.
 */
var numLessons;


// Models
window.Lesson = Backbone.Model.extend();

window.LessonCollection = Backbone.Collection.extend({
    model:Lesson,
    url:"api/lessons",
    parse: function(response) {
        return response.results;
    }
});


// Views
window.LessonListView = Backbone.View.extend({

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        console.log('rendering list');
        console.log(this.model.models);
        // render the lesson view headers
        $(".list-group-item").removeClass("active");
        $("#lesson-list-tab").addClass("active");
        $(this.el).append("<h3>Lessons</h3><div class='recommend'><p class='recommend-header'><b>Recommended</b></p>\<" +
            "/div><div id='lesson-list'></div>");
        _.each(this.model.models, function (lesson) {
            $(this.el).append(new LessonListItemView({model:lesson}).render().el);
        }, this);
        return this;
    }

});

window.LessonListItemView = Backbone.View.extend({

    template:_.template($('#lesson-list-item').html()),

    render:function (eventName) {
        var self = this;
        var json = this.model.toJSON();
        $(this.el).html(this.template(json));
        $(this.el).click(function() {
            window.location = "#solo/" + json.id
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

window.LessonView = Backbone.View.extend({

    template:_.template($('#lesson-details').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        $(this.el).addClass("container-details").html(this.template(json));
        return this;
    }

});

window.SnapView = Backbone.View.extend({
    template:_.template($('#snap-template').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        $('#current-lesson').text(json.name);
        $(this.el).html(this.template(json));
        $('#content').show();
        dashUtils.loadSnap(json.id);
        return this;
    }
});

