var CARDS = [
    {
        name: 'attack',
        params: ['i', 'j', 'n'],
        sideEffect: 'no side effect',
		ret: 'Id',
        desc: 'It costs more than expected',
        icon: 'sword'
    },
    {
        name: 'copy',
        params: ['i'],
        sideEffect: 'no side effect',
		ret: 'enemy[i]',
        desc: 'The monster fully digested the intent of victim',
        icon: 'clone'
    },
    {
        name: 'dbl',
        params: ['n'],
        sideEffect: 'no side effect',
		ret: 'n*2',
        desc: 'More the income, more expense',
        icon: 'trees'
    },
    {
        name: 'dec',
        params: ['i'],
        sideEffect: 'v\'[i] <- v\'[i] - 1',
		ret: 'Id',
        desc: 'A cloud of mosquitoes covers the sky',
        icon: 'poison'
    },
    {
        name: 'get',
        params: ['i'],
		sideEffect: 'no side effect',
		ret: 'slot[i]',
        desc: 'Memoise all the knowledge you have',
        icon: 'get'
    },
    {
        name: 'id',
        params: ['x'],
		sideEffect: 'no side effect',
		ret: 'x',
        desc: 'Examine again it\'s always the same',
        icon: 'stork'
    },
    {
        name: 'inc',
        params: ['i'],
        sideEffect: 'v[i] <- v[i] + 1',
		ret: 'Id',
        desc: 'A drop of water saves all day',
        icon: 'medicine'
    },
    {
        name: 'kcomb',
        params: ['x', 'y'],
        sideEffect: 'no side effect',
		ret: 'x',
        desc: 'Stay constant whatever you receive',
        icon: 'leaf-cycle'
    },
    {
        name: 'scomb',
        params: ['f', 'g', 'x'],
        sideEffect: 'no side effect',
		ret: 'f x (g x)',
        desc: 'Composition of small facts reveal the truth',
        icon: 'birds'
    },
    {
        name: 'succ',
        params: ['n'],
        sideEffect: 'no side effect',
		ret: 'n + 1',
        desc: 'Increase one by one all the way to the top',
        icon: 'hatching'
    },
    {
        name: 'zero',
        params: [],
        sideEffect: 'no side effect',
		ret: '0',
        desc: 'Everything starts from zero',
        icon: 'egg'
    }
];

module.exports = CARDS;