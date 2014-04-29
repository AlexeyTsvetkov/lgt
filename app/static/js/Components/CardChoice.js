/** @jsx React.DOM */

var CardChoice = React.createClass({
    handleSelect: function(e) {
        console.debug(e.target.value);
        console.debug(this.props.type);
        console.debug(this.props.slot);
    },
    getInitialState: function() {
        return {value: 'default'};
    },
    render: function() {
        var values = [];
        this.props.cards.forEach(function (card) {
            values.push(<option value={card.name} key={card.name}>{card.name}</option>);
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