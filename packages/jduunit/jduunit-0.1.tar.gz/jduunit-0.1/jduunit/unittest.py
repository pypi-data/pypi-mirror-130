from .testcase import TestCase
import inspect, time
from pathlib import Path
import sys, subprocess
from jduargs import ArgumentParser


class TestProgram:
    def __init__(self, module: str = "__main__"):
        if type(module) == type(""):
            self.module = __import__(module)
            for part in module.split(".")[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module

        if len(sys.argv) > 1:
            self.verbose = sys.argv[1] == "-d"
        else:
            self.verbose = 0

        self.prefix = "test_"
        self.classes = inspect.getmembers(self.module, inspect.isclass)
        self.filename = Path(self.module.__file__).name
        self.own_methods = [f for f in dir(TestCase) if callable(getattr(TestCase, f))]

        self._run_tests()

    def _run_tests(self):
        n_methods = 0
        n_fails = 0
        start_t = time.time()

        for c in self.classes:
            class_name = c[0]
            class_address = c[1]

            methods = self._get_class_methods(class_address)

            print(f"from {class_name} ({self.filename})")
            max_len = max([len(m) for m in methods]) - len(self.prefix)
            n_methods += len(methods)
            n_fails = 0

            for m in methods:
                try:
                    getattr(class_address(), m)()
                except AssertionError as err:
                    error_str = f"({err})"
                else:
                    error_str = ""

                res_str, short = self._handle_error(error_str)
                n_fails += error_str != ""

                if self.verbose:
                    print(f"    {m[5:]:{max_len}s} ... {res_str} {error_str}")
                else:
                    print(short, end="")

        end_t = time.time()

        if not self.verbose:
            print("")

        print("-" * 60)
        print(f"Ran {n_methods} tests in {end_t-start_t:.3f}s")
        if n_fails == 0:
            print("\033[32m\033[1mSUCCESS\033[0m\n")
        else:
            print(f"\033[31m\033[1mFAILED (failures={n_fails})\033[0m\n")

    def _get_class_methods(self, class_address):
        return [
            func
            for func in dir(class_address)
            if callable(getattr(class_address, func))
            and func.startswith(self.prefix)
            and func not in self.own_methods
        ]

    def _handle_error(self, err_str):
        if err_str != "":
            res_str = "fail"
            short = "x"
        else:
            res_str = "ok"
            short = "."

        return res_str, short


main = TestProgram

if __name__ == "__main__":
    parser = ArgumentParser("Performs unit tests inside test_*.py files.")
    parser.add("display", "d", bool, False, help="Increase level of verbosity")
    parser.add("path", "p", str, False, help="Folder containing test_*.py files")
    parser.compile(sys.argv[1:])

    p = Path(parser["path"]).glob("*.py")
    files = [x for x in p if x.is_file() and x.stem[:5] == "test_"]

    verbose_str = "-d" if parser["display"] else ""

    for file in files:
        subprocess.call(f"python {file} {verbose_str}")
