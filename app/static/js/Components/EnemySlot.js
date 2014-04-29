/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');

var EnemySlot = React.createClass({
    render: function() {
        var values = [
            <Par text={this.props.slot.id}/>,
            <Par text={this.props.slot.term}/>,
            <Par text={this.props.slot.vitality}/>
        ];
        return (<Row values={values}/>);
    }
});

module.exports = EnemySlot;