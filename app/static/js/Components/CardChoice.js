/** @jsx React.DOM */

var Logger = require('../Utils/Logger.js');
var GameApiRequests = require('../Utils/GameApiRequests.js');

var CardChoice = React.createClass({
    handleSelect: function(e) {
        var card = e.target.value;
        var slot = this.props.slot;
        var type = this.props.type;

        Logger.logResponse('Selected', {card: card, slot: slot, applyType: type});

        var toRight = (type === 'right')?1:0;
        GameApiRequests.applyTerm(card, slot, toRight);
    },
    getInitialState: function() {
        return {value: 'default'};
    },
    render: function() {
        var values = [];
        this.props.cards.forEach(function (card) {
            values.push(<option value={card} key={card}>{card}</option>);
        });


        this.props.otherSlots.forEach(function (slot) {
            values.push(<option value={slot['id']} key={slot['id']}>Slot {slot['id']}</option>);
        });

        return (
            <select onChange={this.handleSelect} value="{this.state.value}">
                <option value="default"> </option>
                {values}
            </select>
        );
    }
});

module.exports = CardChoice;