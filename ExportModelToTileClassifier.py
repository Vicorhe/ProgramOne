import shelve


def add_model_to_series(series, model):
    tiles_db_path = '../TileClassifier/tiles'
    with shelve.open(tiles_db_path) as db:
        num_shades = db[series]['num_shades']
        batch_number = db[series]['batch_number']
        db[series] = {
            'num_shades': num_shades,
            'batch_number': batch_number,
            'model': model
        }
