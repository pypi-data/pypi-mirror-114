environments = {
    'mainnet': {
        'smartdex': {
            'BOOTNODES': (
                'enode://fd3da177f9492a39d1e7ce036b05745512894df251399cb3ec565'
                '081cb8c6dfa1092af8fac27991e66b6af47e9cb42e02420cc89f8549de0ce'
                '513ee25ebffc3a@3.212.20.0:30303,enode://97f0ca95a653e3c44d'
                '5df2674e19e9324ea4bf4d47a46b1d8560f3ed4ea328f725acec3fcfcb37e'
                'b11706cf07da669e9688b091f1543f89b2425700a68bc8876@104.248.98.'
                '78:30301,enode://b72927f349f3a27b789d0ca615ffe3526f361665b496'
                'c80e7cc19dace78bd94785fdadc270054ab727dbb172d9e3113694600dd31'
                'b2558dd77ad85a869032dea@188.166.207.189:30301'
            ),
            'NETSTATS_HOST': 'wss://stats.swapdex.net',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '7879',
            'WS_SECRET': (
                'standard-wide-atlases-paint-distaff-early-xeroxes'
            )
        },
    },
    'testnet': {
        'smartdex': {
            'BOOTNODES': (
                'enode://ba966140e161ad416a7bd7c75dc695e0a41232723e2b19cbbf651'
                '883ef5e8f2528801b17b9d63152814d219a58a4fcc3e3c877486e64057523'
                'f6714092348efa@195.154.150.210:30301'
            ),
            'NETSTATS_HOST': 'stats.testnet.swapdex.net',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '7880',
            'WS_SECRET': (
                'hello'
            )
        },
    },
    'devnet': {
        'smartdex': {
            'BOOTNODES': (
                'enode://5bec42d41c9eb291c1d20c9ac92bd9c86a4954189b6592b0833e5'
                'c28e389b59e3992efed119a2782d9b95ba7aa78e7f71813067cd6734fadff'
                '322f7dd6fc3b3c@104.248.99.234:30301,enode://89028bc15e9dda643'
                'bc4b9a1a6352896dd3bce7411543b0b160a9eb95093ddbe1f5eda5999e38a'
                '4874bfa6a00fb3526cc2fb9b4feb2a3f7cc80ef8016e05c493@104.248.99'
                '.235:30301,enode://ea8f1eb1a2a695960bfa6df52094c635e173c65e5f'
                'c120501672c0d21900d826d6c1c5a07d64ad36509ec5e7306d7a2c3398398'
                'f34f3e279b91c487c2b3a9537@104.248.99.233:30301'
            ),
            'NETSTATS_HOST': 'stats.devnet.swapdex.net',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '90',
            'WS_SECRET': (
                'torn-fcc-caper-drool-jelly-zip-din-fraud-rater-darn'
            )
        },
    }
}
