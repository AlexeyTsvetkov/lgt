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
  },
  capitalise: function(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
};

module.exports = StringBuilder;