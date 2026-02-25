const path = require('node:path')
const HtmlWebPackPlugin = require('html-webpack-plugin')
const {
  ModuleFederationPlugin,
} = require('@module-federation/enhanced/webpack')
const CopyPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

const exposes = require('./exposes.json')
const { dependencies: deps, name } = require('./package.json')

function generateShared(deps, list) {
  const fallbackVersions = {
    'react': '18.2.0',
    'react-dom': '18.2.0',
    '@mui/material': '5.17.1',
    '@mui/icons-material': '6.4.11',
    '@emotion/react': '11.14.0',
    '@emotion/styled': '11.14.0',
    'moment': '2.30.1',
    'supernova-core': '1.0.44',
  }

  return list.reduce((shared, pkg) => {
    const version = deps[pkg] || fallbackVersions[pkg]
    if (!version) {
      console.warn(`⚠️ No version found for ${pkg}, using "*"`)
    }

    shared[pkg] = {
      singleton: true,
      requiredVersion: version || '*',
      eager: false,
    }
    return shared
  }, {})
}

module.exports = (env, argv) => ({
  mode: argv.mode || 'development',
  devtool: argv.mode === 'development' ? 'source-map' : false,
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    publicPath: 'auto',
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],
    alias: {
      '@': path.resolve(__dirname, 'src/'),
    },
  },
  devServer: {
    port: 8086,
    historyApiFallback: true,
    hot: true,
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
  module: {
    rules: [
      {
        test: /\.m?js/,
        type: 'javascript/auto',
        resolve: {
          fullySpecified: false,
        },
      },
      {
        test: /\.(css|s[ac]ss)$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'style-loader',
          'css-loader',
          'postcss-loader',
        ],
      },
      {
        test: /\.json$/i,
        use: ['json-loader'],
      },
      {
        test: /\.(ts|tsx|js|jsx)$/,
        exclude: [/node_modules/, /templates/],
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true,
            presets: ['@babel/preset-env', '@babel/preset-react'],
            plugins: ['@babel/plugin-transform-runtime'],
          },
        },
      },
      {
        test: /\.(png|jpg|jpeg|svg|ico)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: 'static/media/[name].[hash].[ext]',
            },
          },
          {
            loader: 'image-webpack-loader',
            options: {
              mozjpeg: { progressive: true },
              optipng: { enabled: false },
              pngquant: { quality: [0.65, 0.9], speed: 4 },
              gifsicle: { interlaced: false },
              webp: { quality: 75 },
            },
          },
        ],
      },
    ],
  },

  ...(argv.mode === 'production' && {
    performance: {
      hints: 'warning',
      maxEntrypointSize: 512000,
      maxAssetSize: 3512000,
    },
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 20 * 1024, // ⬅️ Minimum size of a chunk: 20KB
        maxSize: 250 * 1024, // ⬅️ Max chunk size: 250KB — will split if larger
        maxAsyncRequests: 30,
        maxInitialRequests: 30,
        automaticNameDelimiter: '-',
      },
      runtimeChunk: false,
      minimize: true,
      minimizer: [new TerserPlugin(), new CssMinimizerPlugin()],
    },
  }),

  plugins: [
    new MiniCssExtractPlugin(),
    new CopyPlugin({
      patterns: [{ from: 'public', to: '' }],
    }),
    new ModuleFederationPlugin({
      name,
      filename: 'remoteEntry.js',
      exposes,
      remotes: {
        host: 'host_app@http://localhost:8080/remoteEntry.js',
      },
      shared: generateShared(deps, [
        'react',
        'react-dom',
        '@mui/material',
        '@mui/icons-material',
        '@emotion/react',
        '@emotion/styled',
        'supernova-core',
        'moment',
      ]),
    }),
    new HtmlWebPackPlugin({
      template: './src/index.html',
    }),
    new CompressionPlugin({
      algorithm: 'brotliCompress',
      filename: '[path][base].br',
      test: /\.(js|css|html|svg)$/,
      compressionOptions: { level: 11 },
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
      reportFilename: 'bundle-report.html',
    }),
  ],
})
