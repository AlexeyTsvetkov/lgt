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
            <Par text={this.props.slot.id}/>,
            <Par text={this.props.slot.term}/>,
            <Par text={this.props.slot.value}/>
        ];
        return (<Row values={values}/>);
    }
});

var SlotWithCards = React.createClass({
    render: function() {
        var values = [
            <CardChoice type='left' slot={this.props.key} cards={this.props.cards} />,
            <Par text={this.props.slot.id}/>,
            <Par text={this.props.slot.term}/>,
            <Par text={this.props.slot.value}/>,
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
                rows.push(<SlotWithCards slot={slot} cards={cards} key={key} />);
            } else {
                rows.push(<Slot slot={slot} key={key} />);
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

var Game = React.createClass({
    getInitialState: function() {
        return {slots: [{id: 'succ', term: 'λ x. x + 1', value: 100}]};
    },
    componentDidMount: function() {
        $.get('/game/535e8b8aa2cc653a27e02b6f/list/', function(data) { this.setState({slots: data.slots});}.bind(this));
    },
    render: function() {
        return (
            <div>
                <div className="player"><SlotList isPlayer={true} slots={this.state.slots} cards={this.props.cards} /></div>
                <div className="enemy"><SlotList isPlayer={false} slots={this.state.slots} cards={this.props.cards} /></div>
            </div>
        );
    }
});

var CARDS =
    [
        {name: 'succ', term: 'λ x. x + 1'},
        {name: 'zero', term: 'λ. 0'},
        {name: 'id',   term: 'λ x. x'}
    ];

React.renderComponent(<Game cards={CARDS} />, document.getElementById('game'));


