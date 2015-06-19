from sudoku import Sudoku

levels = ['mild', 'difficult', 'fiendish']

pre =\
'''(function() {

    module.exports = {
'''
post =\
'''    };

}());
'''

def run():

    level_strings = []

    for level in levels:

        sudokus = Sudoku.load('../data/%s.txt' % (level))
        jsons = [s.to_json_string() for s in sudokus]

        level_strings.append('%s: [\n%s\n]' % (level, ',\n'.join(jsons)))

    content = ',\n'.join(level_strings)

    s = '%s%s%s' % (pre, content, post)

    with open('../data/sudokus.js', 'w') as fout:
        fout.write(s)


if __name__ == '__main__':

    run()
