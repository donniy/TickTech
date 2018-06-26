module.exports = {
    request: function (req, token) {
        this.options.http._setHeaders.call(this, req, {Authorization: 'Bearer ' + token});
    },

    response: function (res) {
        var body = this.options.http._httpData.call(this, res),
            headers = this.options.http._getHeaders.call(this, res),
            token = headers.Authorization || headers.authorization
                    || body.access_token || body.json_data.access_token;

        if (token) {
            token = token.split(/Bearer\:?\s?/i);

            return token[token.length > 1 ? 1 : 0].trim();
        }
    }
};
