module.exports = {

    request: function (req, token) {
        console.log("REQUEST")
        this.options.http._setHeaders.call(this, req, {Authorization: 'Bearer ' + token});
        console.log("TEST")
    },

    response: function (res) {
        var headers = this.options.http._getHeaders.call(this, res)
        var token = headers.Authorization || headers.authorization;
        if (token) {
            token = token.split(/Bearer\:?\s?/i);

            return token[token.length > 1 ? 1 : 0].trim();
        }
    }
};
