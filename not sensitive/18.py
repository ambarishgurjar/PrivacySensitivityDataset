assignments = []
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def get_boxes(A, B):    
    return [s+t for s in A for t in B]

boxes = get_boxes(ROWS, COLS)

ROW_UNITS = [get_boxes(r, COLS) for r in ROWS]
COLUMN_UNITS = [get_boxes(ROWS, c) for c in COLS]
SQUARE_UNITS = [get_boxes(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid_string, blanks='.'):
 
    values = []
    all_digits = '123456789'
    for c in grid_string:
        if c == '.':
            values.append(blanks)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes, values))