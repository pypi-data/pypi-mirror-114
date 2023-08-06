import codefast as cf
import setuptools


def release():
    cf.utils.shell('python3 setup.py sdist bdist_wheel', print_str=True)
    cf.info('Package packed.')

    cf.utils.shell('python3 -m twine upload -r formal --skip-existing dist/*',
                   print_str=True)
    cf.info('Formal package released.')

    cf.utils.shell('python3 -m twine upload -r test --skip-existing dist/*',
                   print_str=True)
    cf.info('Test package released.')

    cf.utils.shell('rm -r dist')
    cf.utils.shell('rm -r build')
    cf.utils.shell('rm -r *egg-info*')
    cf.utils.shell('rm -r *__pycache__*')
    cf.info('Byproducts cleaned.')
    