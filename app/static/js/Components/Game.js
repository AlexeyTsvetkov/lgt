/** @jsx React.DOM */

var SlotList = require('./SlotList.js');
var GameApiRequests = require('../Utils/GameApiRequests.js');

var Game = React.createClass({
    getInitialState: function() {
        return {playerSlots: [], enemySlots: []};
    },
    componentDidMount: function() {
        GameApiRequests.createGame(this.createGame);
    },
    createGame: function(gameId) {
        GameApiRequests.getGameState(gameId, this.updateSlots);
    },
    updateSlots: function(playerSlots, enemySlots) {
        this.setState({playerSlots: playerSlots, enemySlots: enemySlots});
    },
    render: function() {
        return (
            <div>
                <div className="player"><SlotList isPlayer={true} slots={this.state.playerSlots} cards={this.props.cards} /></div>
                <div className="enemy"><SlotList isPlayer={false} slots={this.state.enemySlots} cards={this.props.cards} /></div>
            </div>
        );
    }
});

module.exports = Game;