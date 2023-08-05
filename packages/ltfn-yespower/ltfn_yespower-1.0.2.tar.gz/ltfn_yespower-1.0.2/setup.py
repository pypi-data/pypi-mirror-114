from setuptools import setup, Extension

ltfn_yespower_module = Extension('ltfn_yespower',
                            sources = ['yespower-module.c',
                                       'yespower.c',
                                       'yespower-opt.c',
                                       'sha256.c'
                                       ],
                            extra_compile_args=['-O2', '-funroll-loops', '-fomit-frame-pointer'],
                            include_dirs=['.'])

setup (name = 'ltfn_yespower',
       version = '1.0.2',
       author_email = 'mraksoll4@gmail.com',
       author = 'mraksoll',
       url = 'https://github.com/mraksoll4/ltfn_yespower_python3',
       description = 'Bindings for yespower-1.0 proof of work used by ltfn',
       ext_modules = [ltfn_yespower_module])
