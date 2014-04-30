/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');
var Healthbar = require('./Healthbar.js');
var CardChoice = require('./CardChoice.js');
var Term = require('./Term.js');
var CardPopup = require('./CardPopup.js');

var PlayerSlot = React.createClass({
    render: function() {
        var slot = this.props.key;
        return (
            <div className="slot">
                <div className="info">
                    <Par text={this.props.slot.id}/>
                    <Healthbar value={this.props.slot.vitality}/>
                    <CardPopup slot={slot} type='left' cards={this.props.cards} />
                    <CardPopup slot={slot} type='right' cards={this.props.cards} />
                </div>
                <div className="lambda"><Term code={this.props.slot.term} /></div>

            </div>
        );
    }
});

module.exports = PlayerSlot;