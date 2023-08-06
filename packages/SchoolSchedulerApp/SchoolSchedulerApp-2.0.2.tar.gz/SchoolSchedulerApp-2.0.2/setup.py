import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SchoolSchedulerApp",
    version="2.0.2",
    author="Julian Berrio, Megan Quinn, Navid Ali, Justin Miller, Michael Berry",
    author_email="miller.j@ufl.edu",
    packages=['schoolschedulerapp'],
    package_data={'schoolschedulerapp': ['*', 'venv/*', 'scheduler/*', 'import/*', "export/*"]},
    description="Python School Scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaberrio/SchoolScheduler",
    project_urls={
        "Source": "https://github.com/jaberrio/SchoolScheduler",
        "Bug Tracker": "https://trello.com/b/G1f61mAc/school-scheduler",
    },
    install_requires=["PyQt5", "reportlab", "sqlalchemy", "openpyxl", "xlsxwriter"],
    entry_points={"console_scripts":
                    [
                        "play_scheduler = schoolschedulerapp:main.main",
                    ]
                  }
)
