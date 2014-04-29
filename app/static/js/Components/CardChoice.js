/** @jsx React.DOM */

var Logger = require('../Utils/Logger.js')

var CardChoice = React.createClass({
    handleSelect: function(e) {
        var card = e.target.value;
        var apply = this.props.type;
        var slot = this.props.slot;
        Logger.logResponse('Selected', {card: card, apply: apply, slot: slot});
    },
    getInitialState: function() {
        return {value: 'default'};
    },
    render: function() {
        var values = [];
        this.props.cards.forEach(function (card) {
            values.push(<option value={card} key={card}>{card}</option>);
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