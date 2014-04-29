/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');
var Term = require('./Term.js');

var EnemySlot = React.createClass({
    render: function() {
        var values = [
            <Par text={this.props.slot.id}/>,
            <Term code={this.props.slot.term} />,
            <Par text={this.props.slot.vitality}/>
        ];
        return (<Row values={values}/>);
    }
});

module.exports = EnemySlot;