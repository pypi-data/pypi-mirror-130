import subprocess
import sys


class AutoInstall:

    @staticmethod
    def find_module(fullname, path=None):
        if path is None:
            try:
                if input(f'Should I install {fullname}? (y/n) - ').lower() not in ['y', 'yes']: 1 / 0
                subprocess.check_output([sys.executable, '-m', 'pip', 'install', fullname])
                print(f'Successfully installed {fullname}!!')
                return type('', (), {'load_module': __import__})
            except: ...


if not hasattr(sys, 'meta_path') or not isinstance(sys.meta_path, list) or not sys.meta_path:
    sys.meta_path = [AutoInstall()]
elif not hasattr(sys.meta_path[-1], '__name__') or sys.meta_path[-1].__name__ != 'AutoInstall':
    sys.meta_path.append(AutoInstall())
