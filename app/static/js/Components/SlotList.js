/** @jsx React.DOM */

var PlayerSlot = require('./PlayerSlot.js');
var EnemySlot = require('./EnemySlot.js');

var SlotList = React.createClass({
    renderHeader: function() {
        var isPlayer = this.props.isPlayer;
        var header = ['Name', 'Text', 'Health'];

        if (isPlayer) {
            header.unshift('Left Apply');
            header.push('Right Apply');
        }

        return _.map(header, function (c) { return (<th>{c}</th>);})
    },

    renderSlots: function() {
        var isPlayer = this.props.isPlayer;
        var cards = this.props.cards;

        var i = 1;
        var rows = [];

        this.props.slots.forEach(function(slot) {
            var key = i++;
            if (isPlayer) {
                rows.push(<PlayerSlot slot={slot} cards={cards} key={key} />);
            } else {
                rows.push(<EnemySlot slot={slot} key={key} />);
            }
        });

        return rows;
    },

    render: function() {
        var isPlayer = this.props.isPlayer;

        var header = this.renderHeader();
        var rows = this.renderSlots();

        return (
             <div>
                <h2>{isPlayer ? 'Yours' : 'Enemy`s'} slots</h2>
                <table className="game-table">
                    <thead>
                        <tr>{header}</tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        );
    }
});

module.exports = SlotList;