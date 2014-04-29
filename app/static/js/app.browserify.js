/** @jsx React.DOM */

var Game = require('./Components/Game.js');

var CARDS =
    [
        {name: 'succ', term: 'λ x. x + 1'},
        {name: 'zero', term: 'λ. 0'},
        {name: 'id',   term: 'λ x. x'}
    ];

React.renderComponent(<Game cards={CARDS} />, document.getElementById('game'));