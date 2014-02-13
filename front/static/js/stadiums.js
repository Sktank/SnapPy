/**
 * Created with PyCharm.
 * User: spencertank
 * Date: 2/1/14
 * Time: 10:47 PM
 * To change this template use File | Settings | File Templates.
 */
var numStadiums;

var clearActiveStadiums = function(numStadiums) {
    for (var i = 1; i <= numStadiums; i++) {
        $('#stadium-tab-' + i).removeClass('active');
    }
};

var activateStadium = function(id) {
    clearActiveStadiums(numStadiums);
    $('#stadium-tab-' + id).addClass('active');
};


// Models
window.Stadium = Backbone.Model.extend();

window.StadiumCollection = Backbone.Collection.extend({
    model:Stadium,
    url:"api/stadiums",
    parse: function(response) {
        return response.results;
    }
});

// Views
window.StadiumListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        console.log('rendering list');
        console.log(this.model.models);
        $(this.el).addClass('nav nav-tabs');
        _.each(this.model.models, function (stadium) {
            $(this.el).append(new StadiumListItemView({model:stadium}).render().el);
        }, this);
        return this;
    }

});

window.StadiumListItemView = Backbone.View.extend({

    tagName:"li",

    template:_.template($('#stadium-list-item').html()),

    render:function (eventName) {
        var json = this.model.toJSON();
        var id = json.id;
        $(this.el).attr('data-toggle', 'tab').attr('id','stadium-tab-' + id).html(this.template(json));
        return this;
    }

});

window.StadiumView = Backbone.View.extend({

    template:_.template($('#stadium-details').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});


window.AllStadiumsView = Backbone.View.extend({

    render: function(eventName) {
        $(contendId).append('<div id="map-canvas" style="width:85%; height: 500px;"></div>');
        var mapOptions = {
            center: new google.maps.LatLng(-18, -50),
            zoom: 4
        };
        var mapCanvas = document.getElementById("map-canvas");
        var map = new google.maps.Map(mapCanvas, mapOptions);
//        google.maps.event.addDomListener(window, 'load', initialize);

        _.each(this.model.models, function (stadium) {
            new StadiumMarkerView({model:stadium}).render(map);
        }, this);
        return this;
    }
});

window.StadiumMarkerView = Backbone.View.extend({
   render:function(map) {
       console.log('adding marker');
       var modelJSON = this.model.toJSON();
       console.log(modelJSON.latitude);
       console.log(modelJSON.longitude);
       console.log(modelJSON.name);
       var myLatlng = new google.maps.LatLng(modelJSON.latitude,modelJSON.longitude);
       var marker = new google.maps.Marker({
           position: myLatlng,
           map: map,
           title:modelJSON.name
       });

       google.maps.event.addListener(marker, 'click', function() {
           console.log('clicked ' + modelJSON.id);
           window.location.href = '#stadiums/' + modelJSON.id;
       });
   }
});

