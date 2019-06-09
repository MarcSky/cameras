const path = require('path');
const webpack = require('webpack');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  entry: {
    bundle: './index.tsx'
  },
  output: {
    // path: '/home/tosha/work/web/cp/cameras/client_api/server/api/static',
    path: __dirname + '/../server/api/static',
    filename: 'index.js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'ts-loader',
          options: {
            transpileOnly: true,
            onlyCompileBundledFiles: true,
          }
        }
      },
//      {
//        test: /\.(scss)$/,
//        use: ExtractTextPlugin.extract({
//          fallback: 'style-loader',
//          use: ['css-loader', 'sass-loader']
//        })
//      },

       {
         test: /\.(less|css)$/,
         use: [{
           loader: 'style-loader',
         }, {
           loader: 'css-loader', // translates CSS into CommonJS
         }, {
           loader: 'less-loader', // compiles Less to CSS
           options: {
             modifyVars: {
               'primary-color': '#1DA57A',
               'link-color': '#1DA57A',
               'border-radius-base': '2px',
               // or
               // 'hack': `true; @import "your-less-file-path.less";`, // Override with less file
             },
             javascriptEnabled: true,
           },
         }],
       }
    ],
  },
  resolve: {
    extensions: ['*', '.tsx', '.ts', '.json', '.js', '.jsx',]
  },
  // mode: "production",
  mode: "development",
  devtool: 'source-map',
  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  },
  plugins: [
    new ExtractTextPlugin('styles.css'),
    // ["import", { "libraryName": "antd", "libraryDirectory": "es", "style": "css" }]
  ]
}
