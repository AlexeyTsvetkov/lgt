/** @jsx React.DOM */

var StringBuilder = require('../Utils/StringBuilder.js');

var CARDS = [
    {name: 'id', params: ['x'], ret: 'x', desc: 'Examine again it\'s always the same', icon: 'stork'}
];


var CardHeader = React.createClass({
    render: function() {
        return (<div className="header"><div className="text block">{this.props.text}</div></div>);
    }
});

var CardImage = React.createClass({
    render: function() {
        return (
            <div className="icon">
                <div className="text block">
                    <i className={this.props.icon}> </i>
                </div>
            </div>
        );
    }
});

var CardDescription = React.createClass({
    render: function() {
        return (
            <div className="description">
                <div className="text block">
                    <p>{this.props.returns}</p>
                </div>
            </div>
        );
    }
});

var Card = React.createClass({
    render: function() {
        var card = this.props.card;
        var cardData = _.find(CARDS, function (c) { return c.name === card; });

        if (cardData === undefined)
            return (<div></div>);

        var paramString = StringBuilder.join(cardData.params, ', ');
        var headerString = StringBuilder.capitalise(cardData.name) + ' ' + paramString;
        var icon = 'icon-' + cardData.icon;
        var description = cardData.desc;
        var returnString = 'return ' + cardData.ret;

        return (
        <div className="card">
                <CardHeader text={headerString} />
                <CardImage icon={icon} />
                <CardDescription returns={returnString} text={description} />
        </div>
        );
    }
});

var CardTable = React.createClass({
    render: function() {
        var cards = [];
        this.props.cards.forEach(function(card) {
            for (var i = 0; i < 10; i++)
            cards.push(<Card card={card} />);
        });
        return (<div>{cards}</div>);
    }
});

var CardPopup = React.createClass({
    handleClick: function(e) {
        React.renderComponent(<CardTable cards={this.props.cards} />, document.getElementById('cards'));
        $('#popup-holder').show();
    },
    render: function() {
        return (
            <a className="button" onClick={this.handleClick}>
                <i className="icon-card"></i>
            </a>
        );
    }
});

module.exports = CardPopup;