var Logger = {
  logResponse: function(msg, data) {
    console.log(msg);
    console.debug(data);
  },
  warn: function(msg) {
    console.warn(msg);
  }
};

module.exports = Logger;