var Logger = require('./Logger.js');

var GameApiRequests = {
    createGame: function(callback) {
        $.get('/game/create', function(data) {
            Logger.logResponse('Create game', data);

            var id = data.result;
            callback(id);
        });
    },
    listCards: function(id, callback) {
        $.get('/game/' + id + '/list/', function (data) {
            Logger.logResponse('List cards', data);

            var slots = data.slots;
            callback(slots);
        });
    }
};

module.exports = GameApiRequests;