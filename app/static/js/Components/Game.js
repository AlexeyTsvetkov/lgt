/** @jsx React.DOM */

var SlotList = require('./SlotList.js');
var GameApiRequests = require('../Utils/GameApiRequests.js');

var Game = React.createClass({
    getInitialState: function() {
        return {playerSlots: [], enemySlots: [], cards: []};
    },
    componentDidMount: function() {
        this.createGame($('.game-id').data('game-id'));
        GameApiRequests.loadCards(this.updateCards);
        GameApiRequests.setApplyTerm(this.updateSlots);
    },
    createGame: function(gameId) {
        GameApiRequests.setGameId(gameId);
        var _this = this;

        GameApiRequests.getGameState(gameId, _this.updateSlots);
        setInterval(function() {
            GameApiRequests.getGameState(gameId, _this.updateSlots);
        }, 5000);
    },
    updateSlots: function(playerSlots, enemySlots, isMyTurn) {
        this.setState({playerSlots: playerSlots, enemySlots: enemySlots, isMyTurn: isMyTurn});
    },
    updateCards: function(cards) {
        this.setState({cards: cards});
    },
    render: function() {
        var turn = this.state.isMyTurn ? "Your turn" : "Opponent's turn";
        return (
            <div>
                <div>{turn}</div>
                <div className="player"><SlotList isPlayer={true} slots={this.state.playerSlots} cards={this.state.cards} /></div>
                <div className="enemy"><SlotList isPlayer={false} slots={this.state.enemySlots} cards={this.state.cards} /></div>
            </div>
        );
    }
});

module.exports = Game;