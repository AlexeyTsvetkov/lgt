/** @jsx React.DOM */

var Par = React.createClass({
   render: function() {
       return (<p>{this.props.text}</p>);
   }
});

module.exports = Par;