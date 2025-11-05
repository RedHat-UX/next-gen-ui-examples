from setuptools import setup

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Custom HBC support for RHDS Extension for Next Gen UI Agent"

setup(
    name="rhds_hbc_example_renderer",
    version="0.1.0",
    author="Red Hat",
    description="Custom HBC support for RHDS Extension for Next Gen UI Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedHat-UX/next-gen-ui-examples",
    license="Apache-2.0",
    package_dir={"rhds_hbc_example_renderer": "."},
    packages=["rhds_hbc_example_renderer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.12",
    install_requires=[
        "next_gen_ui_agent",
        "next_gen_ui_rhds_renderer",
        "jinja2",
        "next_gen_ui_testing",  # For tests
    ],
    include_package_data=True,
    package_data={
        "rhds_hbc_example_renderer": ["templates/*.jinja"],
    },
    entry_points={
        "next_gen_ui.agent.renderer_factory": [
            "hbc-example-rhds = rhds_hbc_example_renderer:HbcExampleRhdsStrategyFactory"
        ],
    },
)

