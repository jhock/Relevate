const path = require('path');
const fs = require('fs')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

// Gather all scss files from the components directory
const collectScss = function(dir, filelist) {
  files = fs.readdirSync(dir)
  filelist = filelist || []

  files.forEach(function (file) {
    if (fs.statSync(dir + '/' + file).isDirectory()) {
      filelist = collectScss(dir + '/' + file, filelist)
    } else {
      if (path.extname(file) === '.scss') {
        filelist.push(path.resolve(dir, file))
      }
    }
  })
  return filelist
}

// Use the scss files as the webpack entry
const scss = collectScss('./apps/components')
scss.push(path.resolve(__dirname, './scss/main.scss'))

module.exports = {
  entry: scss,
  output: {
    path: __dirname + '/static/css'
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'main.css'
    })
  ],
  module: {
    rules: [{
      test: /\.scss$/,
      use: [
        MiniCssExtractPlugin.loader,
        {
          loader: 'css-loader',
          options: {
            sourceMap: true,
            minimize: {
              safe: true
            }
          }
        },
        {
          loader: 'postcss-loader'
        },
        {
          loader: 'sass-loader',
          options: {
            sourceMap: true,
            // In order to avoid nasty relative imports in the component .scss files,
            // we prepend them with the paths to the variables and mixins
            data: '@import "' + path.resolve(__dirname, './scss/assets.scss') + '";'
          }
        }
      ]
    }]
  }
}
