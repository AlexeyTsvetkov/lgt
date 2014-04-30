/** @jsx React.DOM */

var PlayerSlot = require('./PlayerSlot.js');
var EnemySlot = require('./EnemySlot.js');

var SlotList = React.createClass({
    renderSlots: function() {
        var isPlayer = this.props.isPlayer;
        var cards = this.props.cards;
        var slots = this.props.slots;

        var i = 1;
        var rows = [];

        slots.forEach(function(slot) {
            var key = i++;

            var otherSlots = slots.filter(
                function(sl) {
                    return sl['id'] != slot['id'];
            });

            if (isPlayer) {
                rows.push(<PlayerSlot slot={slot} cards={cards} key={key} otherSlots={otherSlots} />);
            } else {
                rows.push(<EnemySlot slot={slot} key={key} />);
            }
        });

        return rows;
    },

    render: function() {
        var isPlayer = this.props.isPlayer;
        var rows = this.renderSlots();

        return (
             <div>
                <h2>{isPlayer ? 'Yours' : 'Enemy`s'} slots</h2>
                <table className="game-table">
                    {rows}
                </table>
            </div>
        );
    }
});

module.exports = SlotList;