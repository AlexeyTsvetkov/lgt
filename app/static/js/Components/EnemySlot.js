/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');
var Term = require('./Term.js');
var Healthbar = require('./Healthbar.js');

var EnemySlot = React.createClass({
    render: function() {
        return (
            <div className="slot">
                <div className="info">
                    <Par text={this.props.slot.id}/>
                    <Healthbar value={this.props.slot.vitality}/>
                </div>
                <div className="lambda"><Term code={this.props.slot.term} /></div>
            </div>
        );
    }
});

module.exports = EnemySlot;