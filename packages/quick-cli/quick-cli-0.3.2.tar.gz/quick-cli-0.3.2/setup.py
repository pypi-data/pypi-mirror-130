# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quick',
 'quick.commands',
 'quick_client',
 'quick_client.api',
 'quick_client.models']

package_data = \
{'': ['*'], 'quick_client': ['docs/*']}

install_requires = \
['PyYAML>=5.3,<6.0',
 'isodate>=0.6.0,<0.7.0',
 'python-dateutil>=2.5.0,<3.0.0',
 'requests>=2.0.0,<3.0.0',
 'six>=1.12.0,<2.0.0',
 'urllib3>=1.0,<2.0']

entry_points = \
{'console_scripts': ['quick = quick.__main__:main']}

setup_kwargs = {
    'name': 'quick-cli',
    'version': '0.3.2',
    'description': 'The CLI to control your quick cluster.',
    'long_description': '# Helm Charts\n\nThis repository contains helm charts for all CloudHut products. As of now there\'s only the Kowl helm chart which is documented below.\n\n## Installing the helm chart\n\n```\nhelm repo add cloudhut https://raw.githubusercontent.com/cloudhut/charts/master/archives\nhelm repo update\nhelm install -f values.yaml kowl cloudhut/kowl\n```\n\n## Chart configuration\n\n| Parameter | Description | Default |\n| --- | --- | --- |\n| `replicaCount` | Number of Kowl replicas | `1` |\n| `global.imageRegistry` | Global Image Registry | (none) |\n| `image.registry` | Image Registry | `quay.io` |\n| `image.repository` | Docker image repo | `/cloudhut/kowl` |\n| `image.pullPolicy` | Image pull policy | `IfNotPresent` |\n| `image.tag` | Image tag | `v1.2.2` (inherited) |\n| `imagePullSecrets` | Reference to one or more secrets to be used when pulling images | `s` |\n| `nameOverride` | Expand the name of the chart | (none) |\n| `fullnameOverride` | Create a default fully qualified app name | (none) |\n| `serviceAccount.create` | Create a new service account | `true` |\n| `serviceAccount.annotations` | Annotations for new service account | `{}` |\n| `serviceAccount.name` | Service Account Name | (none / generated if create is true) |\n| `podAnnotations` | Annotations to attach on Kowl pod | `{}` |\n| `podSecurityContext` | Pod Security Context | `{runAsUser: 99, fsGroup: 99}` |\n| `securityContext` | Container Security Context | `{runAsNonRoot: true}` |\n| `service.type` | Service type | `ClusterIP` |\n| `service.port` | Service port | `80` |\n| `service.type` | Annotations to attach to service | `{}` |\n| `ingress.enabled` | Whether or not to deploy an ingress | `false` |\n| `ingress.annotations` | Ingress annotations | `{}` |\n| `ingress.hosts[0].host` | Ingress hostname | `chart-example.local` |\n| `ingress.hosts[0].paths` | Path within the url structure | `[]` |\n| `ingress.tls` | TLS configuration for the ingress | `[]` |\n| `resources` | Resource configuration for deployment | `{}` |\n| `autoscaling.enabled` | Whether or not to deploy a horizontal pod autoscaler | `false` |\n| `autoscaling.minReplicas` | Minimum number of replicas | `1` |\n| `autoscaling.maxReplicas` | Maximum number of replicas | `100` |\n| `autoscaling.targetCPUUtilizationPercentage` | Target average utilization for CPU in % | `80` |\n| `autoscaling.targetMemoryUtilizationPercentage` | Target average utilization for RAM in % | (none) |\n| `nodeSelector` | Node selector used in deployment | `{}` |\n| `tolerations` | Tolerations for tainted nodes | `[]` |\n| `affinity` | Pod (anti)affinities | `{}` |\n| `extraVolumes` | Add additional volumes, e. g. for tls keys | `""` |\n| `extraVolumeMounts` | Add additional volumes mounts, e. g. for tls keys | `""` |\n| `extraEnv` | Additional environment variables for kowl | `""` |\n| `extraEnvFrom` | Additional environment variables for kowl mapped from Secret or ConfigMap | `""` |\n| `kowl.config` | Kowl config content | `{}` |\n| `kowl.roles` | Kowl roles config content (business) | (none) |\n| `kowl.roleBindings` | Kowl rolebindings config content (business) | (none) |\n| `secret.existingSecret` | Secret name of an existing secret (see notes below) | (none) |\n| `secret.kafka.saslPassword` | Kafka sasl password value | (none) |\n| `secret.kafka.tlsCa` | Kafka TLS ca file | (none) |\n| `secret.kafka.tlsCert` | Kafka TLS cert file | (none) |\n| `secret.kafka.tlsKey` | Kafka TLS key | (none) |\n| `secret.kafka.tlsPassphrase` | Kafka TLS passphrase | (none) |\n| `secret.cloudhut.licenseToken` | License token for Kowl business (business) | (none) |\n| `secret.keyname.cloudhut-license-token` | Secret key name for the cloudhut license token  | `cloudhut-license-token` |\n| `secret.keyname.kafka-tls-passphrase` | Secret key name for the TLS passphrase  | `kafka-tls-passphrase` |\n| `secret.keyname.kafka-sasl-password` | Secret key name for the SASL password  | `kafka-sasl-password` |\n| `login.google.clientSecret` | Google OAuth client secret (business) | (none) |\n| `login.github.clientSecret` | GitHub OAuth client secret (business) | (none) |\n| `login.github.personalAccessToken` | GitHub personal access token (business) | (none) |\n| `login.okta.clientSecret` | Okta OAuth client secret (business) | (none) |\n| `login.okta.directoryApiToken` | Okta api token for directory API (business) | (none) |\n\nFurther documentation can be found in the [examples](./examples).\n\n#### Usage of the tpl Function\nThe tpl function allows us to pass string values from values.yaml through the templating engine. It is used for the following values:\n\n* extraEnv\n* extraEnvFrom\n* extraVolumes\n* extraVolumeMounts\n\n### Kowl Config / Mounted secrets\n\nWith this chart you can specify the whole YAML config for Kowl (Business). This includes path to files which may be mounted by this chart. This is the list of static paths which you may need to specify in the config in case you use them:\n\n| Type | Path |\n| --- | --- |\n| Config | `/etc/kowl/configs/config.yaml` |\n| Roles | `/etc/kowl/configs/roles.yaml` |\n| Role Bindings | `/etc/kowl/configs/role-bindings.yaml` |\n| Kafka TLS CA | `/etc/kowl/secrets/kafka-tls-ca` |\n| Kafka TLS Cert | `/etc/kowl/secrets/kafka-tls-cert` |\n| Kafka TLS Key | `/etc/kowl/secrets/kafka-tls-key` |\n| Google Groups Service Account | `/etc/kowl/secrets/login-google-groups-service-account.json` |\n\n### Using an existing secret\n\nIf you prefer to use an existing secret rather than creating a new one with this chart you **must** specify all keys. Please take a look at the [sample manifest](./examples/secret.yaml).\n',
    'author': 'd9p',
    'author_email': 'contact@d9p.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://d9p.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
