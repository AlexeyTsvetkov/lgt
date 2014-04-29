/** @jsx React.DOM */


var CardTable = React.createClass({
    render: function() {
        return (<div></div>);
    }
});

var CardPopup = React.createClass({
    handleClick: function(e) {
        React.renderComponent(<CardTable />, document.getElementById('cards'));
        $('#popup-holder').show();
    },
    render: function() {
        return (<a className="button" onClick={this.handleClick}></a>);
    }
});

module.exports = CardPopup;