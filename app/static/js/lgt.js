/** @jsx React.DOM */

var Par = React.createClass({
   render: function() {
       return (<p>{this.props.text}</p>);
   }
});

var Row = React.createClass({
    render: function() {
        var cells = [];
        for (var i = 0; i < this.props.values.length; i++) {
            cells.push(<td>{this.props.values[i]}</td>);
        }
        return (<tr>{cells}</tr>);
    }
});

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

var Slot = React.createClass({
    render: function() {
        var values = [
            <Par text={this.props.card.name}/>,
            <Par text={this.props.card.text}/>,
            <Par text={this.props.health}/>
        ];
        return (<Row values={values}/>);
    }
});

var SlotWithCards = React.createClass({
    render: function() {
        var values = [
            <CardChoice type='left' slot={this.props.key} cards={this.props.cards} />,
            <Par text={this.props.card.name}/>,
            <Par text={this.props.card.text}/>,
            <Par text={this.props.health}/>,
            <CardChoice type='right' slot={this.props.key} cards={this.props.cards} />,
        ];
        return (<Row values={values}/>);
    }
});

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
                rows.push(<SlotWithCards card={slot.card} health={slot.health} cards={cards} key={key} />);
            } else {
                rows.push(<Slot card={slot.card} health={slot.health} key={key} />);
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

var CARDS =
    [
        {name: 'succ', text: 'λ x. x + 1'},
        {name: 'zero', text: 'λ. 0'},
        {name: 'id',   text: 'λ x. x'}
    ];

var SLOTS = [];

var ID_CARD = _.find(CARDS, function(c) { return c.name === 'id'; });
for (var i = 0; i < 10; i++) {
    SLOTS.push({ card: ID_CARD, health: 10000 });
}

React.renderComponent(<SlotList isPlayer={true} slots={SLOTS} cards={CARDS} />, document.getElementById('player'));
React.renderComponent(<SlotList isPlayer={false} slots={SLOTS} cards={CARDS} />, document.getElementById('enemy'));