/** @jsx React.DOM */

var Par = require('./Par.js');
var Row = require('./Row.js');
var CardChoice = require('./CardChoice.js');
var Term = require('./Term.js');
var CardPopup = require('./CardPopup.js');

var PlayerSlot = React.createClass({
    render: function() {
        var slot = this.props.key;
        var values = [
            <CardPopup slot={slot} type='left' cards={this.props.cards} />,
            //<CardChoice type='left' slot={this.props.key} cards={this.props.cards} otherSlots={this.props.otherSlots} />,
            <Par text={this.props.slot.id}/>,
            <Term code={this.props.slot.term} />,
            <Par text={this.props.slot.vitality}/>,
            //<CardChoice type='right' slot={this.props.key} cards={this.props.cards} otherSlots={this.props.otherSlots} />,
            <CardPopup slot={slot} type='right' cards={this.props.cards} />
        ];
        return (<Row values={values}/>);
    }
});

module.exports = PlayerSlot;