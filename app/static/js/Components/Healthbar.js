/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');
var CardChoice = require('./CardChoice.js');
var Term = require('./Term.js');
var CardPopup = require('./CardPopup.js');

var Healthbar = React.createClass({
    render: function() {
        var maxHealth = 100.;
        var minWidthPer = 10;
        var maxWidthPer = 60;
        var vita = this.props.value;
        vita = (vita >= 0) ? vita : 0;
        var width = minWidthPer + vita / maxHealth * (maxWidthPer - minWidthPer);
        var style = {width: width+'%'};
        return (
            <div className="health" style={style}>{this.props.value}/100</div>
        );
    }
});

module.exports = Healthbar;