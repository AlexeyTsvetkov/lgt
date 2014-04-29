var Logger = {
  logResponse: function(msg, data) {
    console.log(msg);
    console.debug(data);
  }
};

module.exports = Logger;