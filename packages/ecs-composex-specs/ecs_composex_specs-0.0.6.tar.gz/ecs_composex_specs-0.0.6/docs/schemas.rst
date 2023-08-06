.. meta::
    :description: ECS Compose-X
    :keywords: AWS, AWS ECS, Docker, Containers, Compose, docker-compose

Compose-X Specifications Schemas
===================================

Top level resources
---------------------

.. jsonschema:: ../ecs_composex_specs/x-vpc.spec.json

.. jsonschema:: ../ecs_composex_specs/x-elbv2.spec.json

.. jsonschema:: ../ecs_composex_specs/x-ecs.spec.json

.. jsonschema:: ../ecs_composex_specs/x-dns.spec.json

.. jsonschema:: ../ecs_composex_specs/x-efs.spec.json


Services level extensions
----------------------------

.. jsonschema:: ../ecs_composex_specs/services.x-alarms.spec.json

.. jsonschema:: ../ecs_composex_specs/services.x-codeguru_profiler.spec.json

.. jsonschema:: ../ecs_composex_specs/services.x-iam.spec.json

.. jsonschema:: ../ecs_composex_specs/services.x-logging.spec.json

.. jsonschema:: ../ecs_composex_specs/services.x-network.spec.json

.. jsonschema:: ../ecs_composex_specs/services.x-scaling.spec.json

Common
-------

.. jsonschema:: ../ecs_composex_specs/ingress.spec.json

.. jsonschema:: ../ecs_composex_specs/x-resources.common.spec.json
