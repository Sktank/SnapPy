/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/1/14
 * Time: 10:47 PM
 * To change this template use File | Settings | File Templates.
 */
var numTeams;

var clearActiveTeams = function(numTeams) {
    for (var i = 1; i <= numTeams; i++) {
        $('#team-tab-' + i).removeClass('active');
    }
};

var activateTeam = function(id) {
    clearActiveTeams(numTeams);
    $('#team-tab-' + id).addClass('active');
};


// Models
window.Team = Backbone.Model.extend();

window.TeamCollection = Backbone.Collection.extend({
    model:Team,
    url:"api/teams",
    parse: function(response) {
        return response.results;
    }
});


// Views
window.TeamListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        console.log('rendering list');
        console.log(this.model.models);
        $(this.el).addClass('nav nav-tabs');
        _.each(this.model.models, function (team) {
            $(this.el).append(new TeamListItemView({model:team}).render().el);
        }, this);
        return this;
    }

});

window.TeamListItemView = Backbone.View.extend({

    tagName:"li",

    template:_.template($('#team-list-item').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        var id = json.id;
        $(this.el).attr('data-toggle', 'tab').attr('id','team-tab-' + id).html(this.template(json));
        return this;
    }

});

window.TeamView = Backbone.View.extend({

    template:_.template($('#team-details').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});


window.AllTeamsView = Backbone.View.extend({

    render: function(eventName) {
        _.each(this.model.models, function (team, index) {
            console.log(index % 3 == 0);
            if (index % 3 == 0) {
                var row = document.createElement("div");
                row.className = "team-row row";
                row = $(row);
                $(this.el).append(row)
            }
            $(this.el).children().last().append(new AllTeamsSingleView({model:team}).render().el);
        }, this);
        return this;
    }
});



window.AllTeamsSingleView = Backbone.View.extend({

    template:_.template($('#team-summary').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});