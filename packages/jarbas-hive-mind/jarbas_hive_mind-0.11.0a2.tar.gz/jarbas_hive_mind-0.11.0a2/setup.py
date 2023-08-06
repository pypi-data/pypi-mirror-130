from setuptools import setup

setup(
    name='jarbas_hive_mind',
    version='0.11.0a2',
    packages=['jarbas_hive_mind',
              'jarbas_hive_mind.backends',
              'jarbas_hive_mind.nodes',
              'jarbas_hive_mind.configuration',
              'jarbas_hive_mind.database',
              'jarbas_hive_mind.utils'],
    include_package_data=True,
    install_requires=["pyopenssl",
                      "service_identity",
                      "autobahn",
                      "mycroft-messagebus-client>=0.9.1",
                      "ovos_utils>=0.0.6",
                      "json_database>=0.2.6",
                      "pycryptodomex",
                      "HiveMind_presence~=0.0.2a2"],
    url='https://github.com/JarbasHiveMind/HiveMind-core',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='Mesh Networking utilities for mycroft core'
)
