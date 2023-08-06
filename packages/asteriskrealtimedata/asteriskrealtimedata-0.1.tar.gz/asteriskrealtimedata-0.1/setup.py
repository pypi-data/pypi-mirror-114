from setuptools import setup, find_packages

setup(
    name="asteriskrealtimedata",
    version="0.1",
    packages=find_packages(),
    author="Juares Vermelho Diaz (CL3k)",
    author_email="jvermelho@cl3k.com",
    description="API for manage realtime data about asterisk status",
    keywords="Asterisk realtime ",
    install_requires=["python3-logstash", "python-json-logger"],
)
