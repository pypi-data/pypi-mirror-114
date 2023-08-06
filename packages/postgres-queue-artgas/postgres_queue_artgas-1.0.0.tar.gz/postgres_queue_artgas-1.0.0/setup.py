from setuptools import setup, find_packages

setup(name="postgres_queue_artgas",
      version="1.0.0",
      packages=find_packages(exclude=['tests']),
      description="Custom PostgreSQL Queue",
      author_email="kek@mail.ru",
      zip_safe=False)
