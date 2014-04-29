/** @jsx React.DOM */

var Term = React.createClass({
   render: function() {
        var _this = this;
        setTimeout( function() {
            Prism.highlightElement(_this.refs.code.getDOMNode(), false);
        }, 100);
       return (<pre><code ref="code" className="language-lambda">{this.props.code}</code></pre>);
   }
});

module.exports = Term;