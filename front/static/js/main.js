/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 1/26/14
 * Time: 3:09 PM
 * To change this template use File | Settings | File Templates.
 */

//function to clear all active navs

var navs = ['nav-news', 'nav-stream', 'nav-matches','nav-standings', 'nav-teams', 'nav-stadiums'];

var clearActiveNavs = function(navtabs) {
    _.each(navtabs, function (tab) {
        $('#' + tab).removeClass('active');
    })
};

var activateNav = function(tab) {
    clearActiveNavs(navs);
    $('#nav-' + tab).addClass('active');
};

// Router
var sideBarId = '#sidebar';
var contendId = '#content';

var AppRouter = Backbone.Router.extend({

    routes:{
        "":"news",
        "news":"news",
        "teams":"teamsList",
        "teams/:id":"teamDetails",
        "stadiums": "stadiumsList",
        "stadiums/:id":"stadiumDetails"
    },

    news:function() {
        activateNav('news');
        $(contendId).html('<h3>This is the News</h3>');
        $(sideBarId).html('');
    },

    teamsList:function () {
        var self = this;
        activateNav('teams');
        $('#sidebar-header').text('Teams');
        this.teamList = new TeamCollection();
        this.teamList.fetch({
            success: function(collection){
                // This code block will be triggered only after receiving the data.
                self.teamListSideView = new TeamListView({model:self.teamList});
                self.teamListMainView = new AllTeamsView({model:self.teamList});
                window.numTeams = self.teamList.length;
                $(sideBarId).html(self.teamListSideView.render().el);
                if (self.teamRequestedId) {
                    self.teamDetails(self.teamRequestedId);
                }
                else {
                    $(contendId).html(self.teamListMainView.render().el);
                }
            }
        });
    },

    teamDetails:function (id) {
        if (this.teamList) {
            this.team = this.teamList.get(id);
            this.teamView = new TeamView({model:this.team});
            activateTeam(id);
            $(contendId).html(this.teamView.render().el);
        }
        else {
            this.teamRequestedId = id;
            this.teamsList();
        }
    },

    stadiumsList:function() {
        var self = this;
        activateNav('stadiums');
        $('#sidebar-header').text('Stadiums');
        $(contendId).empty();
        this.stadiumList = new StadiumCollection();
        this.stadiumList.fetch({
            success: function(collection){
                // This code block will be triggered only after receiving the data.
                self.stadiumListSideView = new StadiumListView({model:self.stadiumList});
                self.stadiumListMainView = new AllStadiumsView({model:self.stadiumList});
                window.numStadiums = self.stadiumList.length;
                $(sideBarId).html(self.stadiumListSideView.render().el);
                if (self.stadiumRequestedId) {
                    self.stadiumDetails(self.stadiumRequestedId);
                }
                else {
                    self.stadiumListMainView.render();
                }
            }
        });

    },

    stadiumDetails:function (id) {
        if (this.stadiumList) {
            this.stadium = this.stadiumList.get(id);
            this.stadiumView = new StadiumView({model:this.stadium});
            activateStadium(id);
            $(contendId).html(this.stadiumView.render().el);
        }
        else {
            this.stadiumRequestedId = id;
            this.stadiumsList();
        }
    }
});

var app = new AppRouter();
Backbone.history.start();