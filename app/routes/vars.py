

from flask import Blueprint


vars_bp = Blueprint('vars', __name__)


@vars_bp.route('/vars')
def get_vars():
    file_path = './data2.csv'
    data = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    data = data.drop(data.iloc[:, 0 :13], axis = 1)
    data.rename({'annï¿½ï¿½':'AnneeDeNaissance'},axis=1,  inplace=True, errors='raise')
    print(data.columns.tolist())

    return jsonify(data.columns.tolist())

