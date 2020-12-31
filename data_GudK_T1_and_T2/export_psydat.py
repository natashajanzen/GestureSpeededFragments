"""
Re-export psydat files that did not get exported to CSV.
"""

from glob import glob

from psychopy.tools.filetools import fromFile


def psydat_to_csv(filename_in, filename_out=None):
    """Converts a psydat file to csv.
    """
    
    d = fromFile(filename_in)
    if filename_out is None:
        filename_out = filename_in.rsplit('.', maxsplit=1)[0] + '.csv'
    d.saveAsWideText(filename_out, fileCollisionMethod='overwrite', encoding='utf-8')


if __name__ == '__main__':
    
    psydat_ids = [x[:-7] for x in glob('*.psydat')]
    csv_ids = [x[:-4] for x in glob('*.csv')]

    missing_ids = set(psydat_ids) - set(csv_ids)

    for x in missing_ids:
        psydat_filename = x + '.psydat'
        psydat_to_csv(psydat_filename)
        print('exported', x)
