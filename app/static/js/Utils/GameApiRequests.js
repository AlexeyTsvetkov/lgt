var Logger = require('./Logger.js');

var GameApiRequests = {
    createGame: function(callback) {
        $.get('/game/create', function(data) {
            Logger.logResponse('Create game', data);

            var id = data['result'];
            callback(id);
        });
    },
    getGameState: function(id, callback) {
        $.get('/game/' + id + '/game_state', function(data) {
            data = data.data;
            Logger.logResponse('Game state', data);

            var playerTurn = data['is_it_your_turn'];
            var playerSlots = data['proponent_slots'];
            var enemySlots = data['opponent_slots'];
            callback(playerSlots, enemySlots);
        });
    },
    loadCards: function(callback) {
        $.get('/game/cards/available_cards', function(data) {
            Logger.logResponse('Load cards', data);

            var cards = data['cards'];
            callback(cards);
        });
    }
};

module.exports = GameApiRequests;