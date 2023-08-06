import subprocess
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

install_requirements = ['numpy', 'trio', 'pytypes; python_version < "3.8.0"', 'qtrio', 'PySide2']
test_requirements = ['pytest', 'pytest', 'pytest-cov', 'pytest-trio', 'coverage<5', 'numpy']
puliscope_requirements = ['graphviz', 'pyqtgraph']
puliconf_requirements = ['tomlkit', 'Click']
tools_requirements = puliscope_requirements + puliconf_requirements
all_requirements = install_requirements + test_requirements + puliscope_requirements + puliconf_requirements


def generate_message_files():
    command = "zcm-gen -p --ppath src --package-prefix pulicast_messages".split()
    message_type_files = list(map(str, Path("./extern/messages/").glob("*.zcm")))
    subprocess.call(command + message_type_files)

    generated_files = [Path(str(p, encoding="utf8")) for p in subprocess.Popen(command + message_type_files + ["--output-files"], stdout=subprocess.PIPE).stdout.read().split()]
    with open("./src/pulicast_messages/.gitignore", "w") as fh:
        fh.write(".gitignore\n")
        fh.write("__init__.py\n")
        fh.write("\n".join(f.name for f in generated_files))


class Build(build_py):
    def run(self):
        generate_message_files()
        build_py.run(self)


class Develop(develop):
    def run(self):
        generate_message_files()
        develop.run(self)


setup(
    name='pulicast',
    # this is redundant with `[tool.setuptools_scm]` and `requires = [ ...` in pyproject.toml
    # since the python packaging mechanism is in a transitioning phase right now
    setup_requires=['setuptools_scm', 'setuptools'],
    use_scm_version=True,
    install_requires=install_requirements,
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=find_packages("src") + ["pulicast_messages"],
    url="https://code.kiteswarms.com/kiteswarms/pulicast-python",
    license="GPLv3",
    author='Maximilian Ernestus',
    author_email='maximilian@kiteswarms.com',
    description='Publish Listen Multicast',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'puliscope = pulicast_tools.puliscope.__main__:main [puliscope]',
            'puliconf = pulicast_tools.puliconf.cli:cli [puliconf]',
        ],
    },
    extras_require={
        'puliscope': puliscope_requirements,
        'puliconf': puliconf_requirements,
        'tools': tools_requirements,
        'test': test_requirements,
        'all': all_requirements
    },
    cmdclass={"build_py": Build, "develop": Develop}
)
