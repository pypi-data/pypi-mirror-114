import copy, glob, os

from nbformat import read as nb_read
from nbconvert import PythonExporter
from nbconvert.preprocessors import TagRemovePreprocessor


def nb_to_py(nb_path, py_path):
    with open(nb_path, 'r', encoding="utf-8") as nb_file:
        nb = nb_read(nb_file, as_version=4)
    with open(py_path, 'w', encoding="utf-8") as py_file:
        nb, _ = TagRemovePreprocessor(remove_cell_tags=['notebook_only']).preprocess(copy.deepcopy(nb), None)
        python_exporter = PythonExporter(exclude_markdown=True)
        py_source, resources = python_exporter.from_notebook_node(nb)
        py_file.write(py_source)


def import_nb(nb_path):
    import tempfile, sys
    py_path = tempfile.mktemp(suffix='.py')
    module_name = nb_path.split('.')[0]

    nb_to_py(nb_path, py_path)
    if module_name in sys.modules:
        del sys.modules[module_name]

    import importlib.util, sys
    spec = importlib.util.spec_from_file_location(module_name, py_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Convert the input notebook to python script')
    parser.add_argument('nb', type=str, default='', nargs='?',
                        help="path to the notebook to be convert. default to be project*_solution.ipynb")
    parser.add_argument('-o', '--out', default='', type=str,
                        help='path to the output python script. default to be project*_solution.py')
    args = parser.parse_args()

    nb_path = args.nb
    if nb_path == '':
        paths = glob.glob('./project*_solution.ipynb')
        nb_path = paths[0] if len(paths) > 0 else ''
    if not os.path.exists(nb_path):
        raise RuntimeError('Path to notebook is invalid: ' + nb_path)

    py_path = args.out
    if py_path == '':
        py_path = nb_path.replace('.ipynb', '.py')

    nb_to_py(nb_path, py_path)
