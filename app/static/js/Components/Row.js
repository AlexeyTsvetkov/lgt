/** @jsx React.DOM */

var Row = React.createClass({
    render: function() {
        var cells = [];
        for (var i = 0; i < this.props.values.length; i++) {
            cells.push(<td>{this.props.values[i]}</td>);
        }
        return (<tr>{cells}</tr>);
    }
});

module.exports = Row;