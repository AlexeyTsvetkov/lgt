/** @jsx React.DOM */

var StringBuilder = require('../Utils/StringBuilder.js');
var Logger = require('../Utils/Logger.js');
var GameApiRequests = require('../Utils/GameApiRequests.js');


var CARDS = require('./Cards.js')

var CardTextBlock = React.createClass({
    render: function() {
        return (<div><div className="text block">{this.props.text}</div></div>);
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

var Card = React.createClass({
    handleClick: function(e) {
        var card = this.props.card;
        var slot = this.props.slot;
        var type = this.props.type;

        Logger.logResponse('Clicked card', {card: card, slot: slot, applyType: type});

        var toRight = (type === 'right')?1:0;
        GameApiRequests.applyTerm(card, slot, toRight);
        $('#popup-holder').hide();
    },
    render: function() {
        var cardName = this.props.card;
        var card = _.find(CARDS, function (c) { return c.name === cardName; });

        if (card === undefined) {
            Logger.warn('Unknown card:' + cardName);
            return (<div></div>);
        }

        var paramString = StringBuilder.join(card.params, ', ');
        var headerString = StringBuilder.capitalise(card.name) + ' ' + paramString;
        var icon = 'icon-' + card.icon;
        var description = card.desc;
        var sideEffect = card.sideEffect;
        var returnString = 'return ' + card.ret;

        return (
        <div className="card" title={description}>
                <a onClick={this.handleClick}></a>
                <CardTextBlock text={headerString} />
                <CardImage icon={icon} />
                <CardTextBlock text={sideEffect} />
                <CardTextBlock text={returnString} />
        </div>
        );
    }
});

var CardTable = React.createClass({
    render: function() {
        var type  = this.props.type;
        var slot  = this.props.slot;
        var cards = [];
        _
        .sortBy(this.props.cards, function (card) {return card;})
        .forEach(function(card) {
            cards.push(<Card card={card}  type={type} slot={slot} />);
        });
        return (<div>{cards}</div>);
    }
});

var CardPopup = React.createClass({
    handleClick: function(e) {
        var cards = this.props.cards;
        var type  = this.props.type;
        var slot  = this.props.slot;
        React.renderComponent(
            <CardTable cards={cards} type={type} slot={slot} />,
            document.getElementById('cards')
        );
        $('#popup-holder').show();
    },
    render: function() {
        var tip = 'Apply a card to the ' + this.props.type;
        return (
            <a className="button" onClick={this.handleClick} title={tip}>
                <i className="icon-card"></i>
            </a>
        );
    }
});

module.exports = CardPopup;