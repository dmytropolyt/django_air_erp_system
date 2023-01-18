const path = require('path')
const webpack = require('webpack')

module.exports = {
    entry: './assets/scripts/index.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'airsite', 'static', 'js')
    },
    module: {
        rules: [
            {
            test: /\.(scss)$/,
            use: [
                {
                    loader: 'style-loader'
                },
                {
                    loader: 'css-loader'
                },
                {
                    loader: 'postcss-loader',
                    options: {
                        postcssOptions: {
                            plugins: () => [
                                require('autoprefixer')
                            ]
                        }
                    }
                },
                {
                    loader: 'sass-loader'
                }
                ]
            },
            {
                test: /\.woff($|\?)|\.woff2($|\?)|\.ttf($|\?)|\.eot($|\?)|\.svg($|\?)/i,
                type: 'asset/resource',
                    generator: {
                        //filename: 'fonts/[name]-[hash][ext][query]'
                        filename: 'fonts/[name][ext][query]'
                    }
                }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        })
    ]
}