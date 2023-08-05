from setuptools import setup

ld = \
"""
```python
import mapexcept

# Basic usage
for i in mapexcept(['1', '2', '3', 'FOOBAR', '4'])[ValueError](int):
    print(i)

# 1
# 2
# 3
# 4

print('\n\n\n')

# With default values
for i in mapexcept(['1', '2', '3', 'FOOBAR', '4'])[ValueError:0](int):
    print(i)

# 1
# 2
# 3
# 0
# 4

print('\n\n\n')

# As a decorator
@mapexcept(['1', '2', '3', 'FOOBAR', '4'])[ValueError:0]
def conversion(val:str):
    return int(val)

for i in conversion:
    print(i)

# 1
# 2
# 3
# 0
# 4
```
"""

setup(
    name='mapexcept',
    packages=["mapexcept"],
    version='1.0.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    description="Exception? Just keep mapping.",
    install_requires=["onetrick~=2.1"],
    long_description=ld,
    long_description_content_type="text/markdown",
)