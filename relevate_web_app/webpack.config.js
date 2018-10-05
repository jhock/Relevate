const path = require('path');

module.exports = {
  entry: './static/scss/main.scss',
  output: {
    path: __dirname + '/static/scss'
  },
  module: {
    rules: [{
      test: /\.scss$/,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: 'main.css',
          }
        },
        {
          loader: 'extract-loader'
        },
        {
          loader: 'css-loader'
        },
        {
          loader: 'postcss-loader'
        },
        {
          loader: 'sass-loader'
        }
      ]
    }]
  }
};