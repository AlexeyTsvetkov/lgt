var Logger = require('./Logger.js');
var StringBuilder = require('./StringBuilder.js')

var GameApiRequests = {
    createGame: function(callback) {
        $.get('/game/create', function(data) {
            Logger.logResponse('Create game', data);

            var id = data['result'];
            callback(id);
        });
    },
    loadCards: function(callback) {
        $.get('/game/cards/available_cards', function(data) {
            Logger.logResponse('Load cards', data);

            var cards = data['cards'];
            callback(cards);
        });
    },
    getGameState: function(id, callback) {
        $.get('/game/' + id + '/game_state', function(data) {
            data = data.data;
            Logger.logResponse('Game state', data);
            this.updateSlots(data, callback);

        }.bind(this));
    },
    setApplyTerm: function(callback) {
        this.applyTerm = function(card, termId, applyType) {
            var id = this.gameId;
            var url = StringBuilder.join(['/game', id, 'apply', termId, card, applyType], '/');

            $.get(url, function (data) {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                data = data.data;
                Logger.logResponse('Apply response', data);
                this.updateSlots(data, callback);
            }.bind(this));
        }
    },
    updateSlots: function(data, callback) {
        var playerTurn = data['is_your_turn'];
        var playerSlots = data['proponent_slots'];
        var enemySlots = data['opponent_slots'];
        callback(playerSlots, enemySlots, playerTurn);
    },
    setGameId: function(id) {
        this.gameId = id;
    }
};

module.exports = GameApiRequests;