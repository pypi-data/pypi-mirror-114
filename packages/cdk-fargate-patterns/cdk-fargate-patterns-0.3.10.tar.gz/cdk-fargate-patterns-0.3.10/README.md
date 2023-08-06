[![NPM version](https://badge.fury.io/js/cdk-fargate-patterns.svg)](https://badge.fury.io/js/cdk-fargate-patterns)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-patterns.svg)](https://badge.fury.io/py/cdk-fargate-patterns)
[![Release](https://github.com/pahud/cdk-fargate-patterns/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-fargate-patterns/actions/workflows/release.yml)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

# cdk-fargate-patterns

CDK patterns for serverless container with AWS Fargate

# `DualAlbFargateService`

![](images/DualAlbFargateService.svg)

Inspired by *Vijay Menon* from the [AWS blog post](https://aws.amazon.com/blogs/containers/how-to-use-multiple-load-balancer-target-group-support-for-amazon-ecs-to-access-internal-and-external-service-endpoint-using-the-same-dns-name/) introduced in 2019, `DualAlbFargateService` allows you to create one or many fargate services with both internet-facing ALB and internal ALB associated with all services. With this pattern, fargate services will be allowed to intercommunicat via internal ALB while external inbound traffic will be spread across the same service tasks through internet-facing ALB.

The sample below will create 3 fargate services associated with both external and internal ALBs. The internal ALB will have an alias(`internal.svc.local`) auto-configured from Route 53 so services can interconnect through the private ALB endpoint.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    spot=True, # FARGATE_SPOT only cluster
    tasks=[{
        "task": order_task,
        "desired_count": 2,
        "external": {"port": 443, "certificate": certificate},
        "internal": {"port": 80},
        # customize the service autoscaling policy
        "scaling_policy": {
            "max_capacity": 20,
            "request_per_target": 1000,
            "target_cpu_utilization": 50
        }
    }, {"task": customer_task, "desired_count": 2, "internal": {"port": 8080}}, {"task": product_task, "desired_count": 2, "internal": {"port": 9090}}, {
        "task": task,
        "desired_count": 1,
        "internal": {"port": 50051, "certificate": [cert]},
        "external": {"port": 50051, "certificate": [cert]},
        "protocol_version": elbv2.ApplicationProtocolVersion.GRPC,
        "health_check": {
            "healthy_grpc_codes": "12"
        }
    }
    ],
    route53_ops={
        "zone_name": "svc.local",
        "external_elb_record_name": "external",
        "internal_elb_record_name": "internal"
    }
)
```

# `DualNlbFargateService`

Similar to `DualAlbFargateService`, you are allowed to deploy multiple container services with AWS Fargate as well as external NLB and internal NLB.

To allowed ingress traffic, you will need to explicitly add ingress rules on the `connections`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
nlb_service = DualNlbFargateService(stack, "NLBService",
    tasks=[...]
)

# we need this to allow ingress traffic from public internet only for the order service
nlbService.service[0].connections.allow_from_any_ipv4(ec2.Port.tcp(8080))
# allow from VPC
nlb_service.service.for_each(s => {
      s.connections.allowFrom(ec2.Peer.ipv4(nlbService.vpc.vpcCidrBlock), ec2.Port.tcp(8080));
    })
```

## Fargate Spot Support

By enabling the `spot` property, 100% fargate spot tasks will be provisioned to help you save up to 70%. Check more details about [Fargate Spot](https://aws.amazon.com/about-aws/whats-new/2019/12/aws-launches-fargate-spot-save-up-to-70-for-fault-tolerant-applications/?nc1=h_ls). This is a handy catch-all flag to force all tasks to be `FARGATE_SPOT` only.

To specify mixed strategy with partial `FARGATE` and partial `FARGATE_SPOT`, specify the `capacityProviderStrategy` for individual tasks like.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    tasks=[{
        "task": customer_task,
        "internal": {"port": 8080},
        "desired_count": 2,
        "capacity_provider_strategy": [{
            "capacity_provider": "FARGATE",
            "base": 1,
            "weight": 1
        }, {
            "capacity_provider": "FARGATE_SPOT",
            "base": 0,
            "weight": 3
        }
        ]
    }
    ]
)
```

The custom capacity provider strategy will be applied if `capacityProviderStretegy` is specified, otherwise, 100% spot will be used when `spot: true`. The default policy is 100% Fargate on-demand.

### Fargate Spot Termination Handling

By default, if fargate spot capacity is available in the cluster, a fargate spot termination handler Lambda function will be created with proper IAM role policies to handle the termination event to ensure we deregister the fargate spot task from target groups gracefully. While it's a recommended feature, you may opt out with `spotTerminationHandler: false`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    spot=True, # FARGATE_SPOT only cluster
    spot_termination_handler=False, ...
)
```

## ECS Exec

Simply turn on the `enableExecuteCommand` property to enable the [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) support for all services.

## ECS deployment circuit breaker

ECS deployment circuit breaker automatically rolls back unhealthy service deployments without the need for manual intervention. By default this feature is enabled, you can opt out with `circuitBreaker: false`. Read the [docummentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html) or [blog post](https://aws.amazon.com/tw/blogs/containers/announcing-amazon-ecs-deployment-circuit-breaker/) for more details.

## Internal, External or Both

Specify the `internal` or `external` property to expose your service internally, externally or both.

The `certificate` property implies `HTTPS` protocol.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    tasks=[{"task": task1, "internal": {"port": 8080}}, {"task": task2, "external": {"port": 8081}}, {
        "task": task3,
        "external": {"port": 443, "certificate": my_acm_cert},
        "internal": {"port": 8888}
    }
    ]
)
```

## VPC Subnets

By default, all tasks will be deployed in the private subnets. You will need the NAT gateway for the default route associated with the private subnets to ensure the task can successfully pull the container images.

However, you are allowed to specify `vpcSubnets` to customize the subnet selection.

To deploy all tasks in public subnets, one per AZ:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    vpc_subnets={
        "subnet_type": ec2.SubnetType.PUBLIC,
        "one_per_az": True
    }, ...
)
```

This will implicitly enable the `auto assign public IP` for each fargate task so the task can successfully pull the container images from external registry. However, the ingress traffic will still be balanced via the external ALB.

To deploy all tasks in specific subnets:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    vpc_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "sub-1a", "subnet-0e9460dbcfc4cf6ee"),
            ec2.Subnet.from_subnet_id(stack, "sub-1b", "subnet-0562f666bdf5c29af"),
            ec2.Subnet.from_subnet_id(stack, "sub-1c", "subnet-00ab15c0022872f06")
        ]
    }, ...
)
```

### Import an existing Cluster

!!! Before using an existing `ECS Cluster`, please make sure you have the following:

* see : [Adding Fargate capacity providers to an existing cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-capacity-providers.html#fargate-capacity-providers-existing-cluster)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc.from_lookup(stack, "defVpc", is_default=True)
sg = ec2.SecurityGroup(stack, "demo-sg",
    vpc=vpc
)
exist_cluster = ecs.Cluster.from_cluster_attributes(stack, "existCluster",
    security_groups=[sg],
    cluster_name="existCluster",
    vpc=vpc
)

DualAlbFargateService(stack, "Service",
    enable_execute_command=True,
    cluster=exist_cluster,
    tasks=[{
        "task": nginx,
        "desired_count": 1,
        "external": {"port": 80},
        "capacity_provider_strategy": [{
            "capacity_provider": "FARGATE_SPOT",
            "weight": 1
        }]
    }
    ]
)
```

## Sample Application

This repository comes with a sample applicaiton with 3 services in Golang. On deployment, the `Order` service will be exposed externally on external ALB port `80` and all requests to the `Order` service will trigger sub-requests internally to another other two services(`product` and `customer`) through the internal ALB and eventually aggregate the response back to the client.

![](images/DualAlbFargateService.svg)

## Deploy

To deploy the sample application in you default VPC:

```sh
// install first
$ yarn install
// compile the ts to js
$ yarn build
$ npx cdk --app lib/integ.default.js -c use_default_vpc=1 diff
$ npx cdk --app lib/integ.default.js -c use_default_vpc=1 deploy
```

To deploy with HTTPS-only with existing ACM certificate in your default VPC:

```sh
$ npx cdk --app lib/integ.default.js deploy -c use_default_vpc=1 -c ACM_CERT_ARN=<YOUR_ACM_CERT_ARN>
```

On deployment complete, you will see the external ALB endpoint in the CDK output. `cURL` the external HTTP endpoint and you should be able to see the aggregated response.

```sh
$ curl http://demo-Servi-EH1OINYDWDU9-1397122594.ap-northeast-1.elb.amazonaws.com
or
$ curl https://<YOUR_CUSTOM_DOMAIN_NAME>

{"service":"order", "version":"1.0"}
{"service":"product","version":"1.0"}
{"service":"customer","version":"1.0"}
```

# `WordPress`

Use the `WordPress` construct to create a serverless **WordPress** service with AWS Fargate, Amazon EFS filesystem and Aurora serverless database. All credentials auto generated from the **AWS Secret Manager** and securely inject the credentials into the serverless container with the auto generated IAM task execution role.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
WordPress(stack, "WP",
    aurora_serverless=True,
    spot=True,
    enable_execute_command=True
)
```

# `Laravel`

The `Laravl` construct is provided as a high-level abstraction that allows you to create a modern Laravel environment running on `AWS Fargate` and `Amazon Aurora Serverless`. Here comes two variants as the reference:

**laravel-bitnami** - based on [bitnami/laravel](https://hub.docker.com/r/bitnami/laravel/) with `artisan` running as the built-in web server.

**laravel-nginx-php-fpm** - laravel with nginx and php-fpm maintained by [Ernest Chiang](https://github.com/dwchiang).

Simply point `code` to your local Laravel codebase and it takes care everything else for you.

## Samples

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
#
# laravel-bitnami
#
Laravel(stack, "LaravelBitnamiDemo",
    aurora_serverless=True,
    spot=True,
    enable_execute_command=True,
    code=path.join(__dirname, "../services/laravel-bitnami"),
    container_port=3000,
    loadbalancer={"port": 80}
)

#
# laravel-nginx-php-fpm
#
Laravel(stack, "LaravelNginxDemo",
    aurora_serverless=True,
    spot=True,
    enable_execute_command=True,
    code=path.join(__dirname, "../services/laravel-nginx-php-fpm"),
    loadbalancer={"port": 80}
)
```

See [integ.laravel.ts](src/integ.laravel.ts) for the full code sample.

# Local development and testing

The [docker-compose.yml](./services/docker-compose.yml) is provided with all sample services in the repository. To bring up all services locally, run:

```sh
$ cd services
$ docker compose up
```

Use `cURL` to test locally:

```
curl http://localhost
```

Response:

```
{"service":"order","version":"1.0"}
{"service":"product","version":"1.0"}
{"service":"customer","version":"1.0"}
```

# FAQ

Q: What is the difference between `cdk-fargate-patterns` and [aws-ecs-patterns](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-ecs-patterns)?

A: `aws-ecs-patterns` comes with a few patterns around Amazon ECS with AWS Fargate or AWS EC2 and focuses on some scenarios with single service and single ELB like `ApplicationLoadBalancedFargateService` and `NetworkLoadBalancedFargateService`. However, `cdk-fargate-patterns` is trying to explore use cases on modern application which usually comes with multiple container services grouped as a deployment with inter-service connectivity as well as ingress traffic from external internet by seperating the internal ELB from the external one.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section --><!-- prettier-ignore-start --><!-- markdownlint-disable --><table>
  <tr>
    <td align="center"><a href="https://blog.neilkuan.net"><img src="https://avatars.githubusercontent.com/u/46012524?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Neil Kuan</b></sub></a><br /><a href="#design-neilkuan" title="Design">🎨</a> <a href="https://github.com/pahud/cdk-fargate-patterns/commits?author=neilkuan" title="Code">💻</a> <a href="https://github.com/pahud/cdk-fargate-patterns/commits?author=neilkuan" title="Tests">⚠️</a> <a href="#example-neilkuan" title="Examples">💡</a></td>
    <td align="center"><a href="https://www.ernestchiang.com"><img src="https://avatars.githubusercontent.com/u/251263?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ernest Chiang</b></sub></a><br /><a href="#ideas-dwchiang" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/pahud/cdk-fargate-patterns/commits?author=dwchiang" title="Tests">⚠️</a> <a href="https://github.com/pahud/cdk-fargate-patterns/commits?author=dwchiang" title="Code">💻</a> <a href="#example-dwchiang" title="Examples">💡</a></td>
    <td align="center"><a href="https://clarence.tw"><img src="https://avatars.githubusercontent.com/u/5698291?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Clarence</b></sub></a><br /><a href="#example-clarencetw" title="Examples">💡</a> <a href="https://github.com/pahud/cdk-fargate-patterns/commits?author=clarencetw" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/paper5487"><img src="https://avatars.githubusercontent.com/u/15643225?v=4?s=100" width="100px;" alt=""/><br /><sub><b>paper5487</b></sub></a><br /><a href="https://github.com/pahud/cdk-fargate-patterns/issues?q=author%3Apaper5487" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/plarsson"><img src="https://avatars.githubusercontent.com/u/903607?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Peter Larsson</b></sub></a><br /><a href="#ideas-plarsson" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/LeoChien-SC"><img src="https://avatars.githubusercontent.com/u/81736089?v=4?s=100" width="100px;" alt=""/><br /><sub><b>LeoChien-SC</b></sub></a><br /><a href="https://github.com/pahud/cdk-fargate-patterns/issues?q=author%3ALeoChien-SC" title="Bug reports">🐛</a></td>
  </tr>
</table><!-- markdownlint-restore --><!-- prettier-ignore-end --><!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
