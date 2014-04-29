var StringBuilder = {
  join: function(data, sep) {
    if (data.length === 0) {
        return '';
    }

    result = data[0].toString();

    for (var i = 1, l = data.length; i < l; i++) {
        result += sep + data[i].toString();
    }

    return result;
  }
};

module.exports = StringBuilder;