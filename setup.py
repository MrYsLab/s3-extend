from setuptools import setup

with open('pypi_desc.md') as f:
    long_description = f.read()

setup(
    name='s3-extend',
    version='1.15',
    packages=[
      's3_extend',
      's3_extend.gateways'
    ],
    install_requires=[
        'python-banyan>=3.9',
        'pymata-express>=1.11',
        'pymata_rh',
        'pymata-cpx',
        'tmx-pico-aio',
        'telemetrix-aio'
    ],

    entry_points={
        'console_scripts': [
            's3a = s3_extend.s3a:s3ax',
            's3c = s3_extend.s3c:s3cx',
            's3e = s3_extend.s3e:s3ex',
            's3p = s3_extend.s3p:s3px',
            's3r = s3_extend.s3r:s3rx',
            's3rh = s3_extend.s3rh:s3rhx',
            's3rp = s3_extend.s3rp:s3rpx',
            'ardgw = s3_extend.gateways.arduino_gateway:arduino_gateway',
            'cpxgw = s3_extend.gateways.cpx_gateway:cpx_gateway',
            'espgw = s3_extend.gateways.esp8266_gateway:esp8266_gateway',
            'pbgw = s3_extend.gateways.picoboard_gateway:picoboard_gateway',
            'rpigw = s3_extend.gateways.rpi_gateway:rpi_gateway',
            'rhgw = s3_extend.gateways.robohat_gateway:robohat_gateway',
            'rpgw = s3_extend.gateways.rpi_pico_gateway:rpi_pico_gateway',
            'wsgw = s3_extend.gateways.ws_gateway:ws_gateway',
        ]
    },

    url='https://github.com/MrYsLab/s3-extend',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    description='A Non-Blocking Event Driven Applications Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Scratch3', 'Arduino', 'ESP-8266', 'Raspberry Pi'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: System :: Hardware'
    ],
)
