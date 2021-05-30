import jinja2
import tempfile
import subprocess as sp
import shutil
import os

class TikZFigure:
    def __init__(self, template_filename, packages_dir="serverFilesQuestion"):
        # the filename of the template file that will be processed by Jinja
        self.template_filename = template_filename
        # the name of the directory where LaTeX packages are kept; serverFilesQuestion by default
        self.packages_dir = packages_dir
    def processed_template(self, **kwargs):
        # open the template file, sub in the provided values, then return the rendered version
        with open(self.template_filename, "r") as f:
            template = jinja2.Template(f.read())
            return template.render(kwargs)
    def image(self, **kwargs):
        # create a temporary directory for doing LaTeX stuff
        tempdir = tempfile.TemporaryDirectory()
        # write the processed template with values subbed in to tempdir/figure.tex
        with open(f"{tempdir.name}/figure.tex", "w") as f:
            f.write(self.processed_template(**kwargs))
        # if there is a directory named self.packages_dir, copy every file in it to tempdir
        if os.path.exists(self.packages_dir):
            for package in os.listdir(self.packages_dir):
                shutil.copy(f"{self.packages_dir}/{package}", tempdir.name)
        # compile the latex from within tempdir, and send STDOUT to /dev/null (must be done for PL)
        sp.run(["pdflatex", "-shell-escape", "figure.tex"], cwd=f"{tempdir.name}", stdout=sp.DEVNULL)
        # return a buffer of the generated png file
        return open(f"{tempdir.name}/figure.png", "rb")
