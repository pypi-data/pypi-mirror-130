import subprocess
import numpy as np
import os
import pathlib
import sys

def test_vspace_linear():
    #gets current path
    path = pathlib.Path(__file__).parents[0].absolute()
    sys.path.insert(1, str(path.parents[0]))
    # Run vspace
    if not (path / "Linear_Test").exists():
        subprocess.check_output(["vspace", "vspace.in"], cwd=path)
    # Grab the output
    folders = sorted([f.path for f in os.scandir(path / "Linear_Test") if f.is_dir()])
    semi = []
    for i in range(len(folders)):
        os.chdir(folders[i])
        with open('earth.in', 'r') as f:
            for newline in f:
                if newline.startswith("dSemi"):
                    newline = newline.strip().split()
                    semi.append(newline[1])
        os.chdir('../')
    for i in range(len(semi)):
        semi[i] = float(semi[i])

    assert np.isclose(semi[0], 1.0)
    assert np.isclose(semi[1], 1.1)
    assert np.isclose(semi[2], 1.2)
    assert np.isclose(semi[3], 1.3)
    assert np.isclose(semi[4], 1.4)
    assert np.isclose(semi[5], 1.5)
    assert np.isclose(semi[6], 1.6)
    assert np.isclose(semi[7], 1.7)
    assert np.isclose(semi[8], 1.8)
    assert np.isclose(semi[9], 1.9)
    assert np.isclose(semi[10], 2.0)


if __name__ == "__main__":
    test_vspace_linear()
