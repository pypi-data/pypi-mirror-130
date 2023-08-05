[![GitHub](https://img.shields.io/github/license/pepperize/cdk-autoscaling-gitlab-runner?style=flat-square)](https://github.com/pepperize/cdk-autoscaling-gitlab-runner/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-autoscaling-gitlab-runner?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-autoscaling-gitlab-runner)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-autoscaling-gitlab-runner?style=flat-square)](https://pypi.org/project/pepperize.cdk-autoscaling-gitlab-runner/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.AutoscalingGitlabRunner?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.AutoscalingGitlabRunner/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pepperize/cdk-autoscaling-gitlab-runner/release/main?label=release&style=flat-square)](https://github.com/pepperize/cdk-autoscaling-gitlab-runner/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-autoscaling-gitlab-runner?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-autoscaling-gitlab-runner/releases)

# AWS CDK GitLab Runner autoscaling on EC2

This project provides a CDK construct to [execute jobs on auto-scaled EC2 instances](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/index.html) using the [Docker Machine](https://docs.gitlab.com/runner/executors/docker_machine.html) executor.

> Running out of [Runner minutes](https://about.gitlab.com/pricing/),
> using [Docker-in-Docker (dind)](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html),
> speed up jobs with [shared S3 Cache](https://docs.gitlab.com/runner/configuration/autoscale.html#distributed-runners-caching),
> cross compiling/building environment [multiarch](https://hub.docker.com/r/multiarch/qemu-user-static/),
> cost effective [autoscaling on EC2](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#the-runnersmachine-section),
> deploy directly from AWS accounts (without [AWS Access Key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)),
> running on [Spot instances](https://aws.amazon.com/ec2/spot/),
> having a bigger [build log size](https://docs.gitlab.com/runner/configuration/advanced-configuration.html)

*Note: it's a really simple and short README. Only basic tips are covered. Feel free to improve it.*

## Install

### TypeScript

```shell
npm install @pepperize/cdk-autoscaling-gitlab-runner
```

or

```shell
yarn add @pepperize/cdk-autoscaling-gitlab-runner
```

### Python

```shell
pip install pepperize.cdk-autoscaling-gitlab-runner
```

### C# / .Net

```
dotnet add package Pepperize.CDK.AutoscalingGitlabRunner
```

## Quickstart

1. **Create a new AWS CDK App** in TypeScript with [projen](https://github.com/projen/projen)

   ```shell
   mkdir gitlab-runner
   cd gitlab-runner
   git init
   npx projen new awscdk-app-ts
   ```
2. **Configure your project in `.projenrc.js`**

   * Add `deps: ["@pepperize/cdk-autoscaling-gitlab-runner"],`
3. **Update project files and install dependencies**

   ```shell
   npx projen
   ```
4. **Register a new runner**

   [Registering runners](https://docs.gitlab.com/runner/register/):

   * For a [shared runner](https://docs.gitlab.com/ee/ci/runners/#shared-runners), go to the GitLab Admin Area and click **Overview > Runners**
   * For a [group runner](https://docs.gitlab.com/ee/ci/runners/index.html#group-runners), go to **Settings > CI/CD** and expand the **Runners** section
   * For a [project runner](https://docs.gitlab.com/ee/ci/runners/index.html#specific-runners), go to **Settings > CI/CD** and expand the **Runners** section

   *Optionally enable: **Run untagged jobs** [x]
   Indicates whether this runner can pick jobs without tags*

   See also *[Registration token vs. Authentication token](https://docs.gitlab.com/ee/api/runners.html#registration-and-authentication-tokens)*
5. **Retrieve a new runner authentication token**

   [Register a new runner](https://docs.gitlab.com/ee/api/runners.html#register-a-new-runner)

   ```shell
   curl --request POST "https://gitlab.com/api/v4/runners" --form "token=<your register token>" --form "description=gitlab-runner" --form "tag_list=pepperize,docker,production"
   ```
6. **Add to your `main.ts`**

   ```python
   # Example automatically generated from non-compiling source. May contain errors.
   from aws_cdk.aws_ec2 import Vpc
   from aws_cdk.core import App, Stack
   from pepperize.cdk_autoscaling_gitlab_runner import GitlabRunnerAutoscaling

   app = App()
   stack = Stack(app, "GitLabRunnerStack")
   vpc = Vpc.from_lookup(app, "ExistingVpc",
       vpc_id="<your vpc id>"
   )
   GitlabRunnerAutoscaling(stack, "GitlabRunner",
       gitlab_token="<your gitlab runner auth token>",
       network={
           "vpc": vpc
       }
   )
   ```
7. **Create service linked role**

   *(If requesting spot instances, default: true)*

   ```sh
   aws iam create-service-linked-role --aws-service-name spot.amazonaws.com
   ```
8. **Configure the AWS CLI**

   * [AWSume](https://awsu.me/)
   * [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
   * [AWS Single Sign-On](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
9. **Deploy the GitLab Runner**

   ```shell
   npm run deploy
   ```

## Example

### Custom cache bucket

By default an AWS S3 is created as GitLab Runner's distributed cache.
It's encrypted with a KMS managed key and public access is blocked.
A custom S3 Bucket can be configured.

```python
# Example automatically generated from non-compiling source. May contain errors.
cache = Bucket(self, "Cache")

GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    cache={"bucket": cache}
)
```

### Configure Docker Machine

By default, docker machine is configured to run privileged with `CAP_SYS_ADMIN` to support [Docker-in-Docker using the OverlayFS driver](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-the-overlayfs-driver)
and cross compiling/building with [multiarch](https://hub.docker.com/r/multiarch/qemu-user-static/).

See [runners.docker section](https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section)
in [Advanced configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration.html)

```python
# Example automatically generated from non-compiling source. May contain errors.
from pepperize.cdk_autoscaling_gitlab_runner import GitlabRunnerAutoscaling

GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    runners={
        "environment": [],  # Reset the OverlayFS driver for every project
        "docker": {
            "cap_add": [],  # Remove the CAP_SYS_ADMIN
            "privileged": False
        },
        "machine": {
            "idle_count": 2,  # Number of idle machine
            "idle_time": 3000,  # Waiting time in idle state
            "max_builds": 1
        }
    }
)
```

### Bigger instance type

By default, t3.nano is used for the manager/coordinator and t3.micro instances will be spawned.
For bigger projects, for example with [webpack](https://webpack.js.org/), this won't be enough memory.

```python
# Example automatically generated from non-compiling source. May contain errors.
GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    manager={
        "instance_type": InstanceType.of(InstanceClass.T3, InstanceSize.NANO)
    },
    runners={
        "instance_type": InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)
    }
)
```

### Different machine image

By default, the latest [Amazon 2 Linux](https://aws.amazon.com/amazon-linux-2/) will be used for the manager/coordinator.
The manager/coordinator instance's cloud init scripts requires [yum](https://access.redhat.com/solutions/9934) is installed, any RHEL flavor should work.
The requested runner instances by default using Ubuntu 20.04, any OS implemented by the [Docker Machine provisioner](https://gitlab.com/gitlab-org/ci-cd/docker-machine/-/tree/main/libmachine/provision) should work.

```python
# Example automatically generated from non-compiling source. May contain errors.
GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    manager={
        "machine_image": MachineImage.generic_linux(manager_ami_map)
    },
    runners={
        "machine_image": MachineImage.generic_linux(runner_ami_map)
    }
)
```

### Spot instances

By default, EC2 Spot Instances are requested.

```python
# Example automatically generated from non-compiling source. May contain errors.
GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    runners={
        "machine": {
            "machine_options": {
                "request_spot_instance": False,
                "spot_price": 0.5
            }
        }
    }
)
```

### Custom runner's role

To deploy from within your GitLab Runner Instances, you may pass a Role with the IAM Policies attached.

```python
# Example automatically generated from non-compiling source. May contain errors.
role = Role(self, "RunnersRole",
    assumed_by=ServicePrincipal("ec2.amazonaws.com"),
    inline_policies={}
)

GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    runners={
        "role": role
    }
)
```

### Vpc

If no existing Vpc is passed, a [VPC that spans a whole region](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Vpc.html) on will be created.
This can become costly, because AWS CDK configured also the routing for the private subnets and creates NAT Gateways (one per AZ).

```python
# Example automatically generated from non-compiling source. May contain errors.
vpc = Vpc(self, "Vpc")

GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>",
    network={"vpc": vpc}
)
```

### Zero config

Deploys the [Autoscaling GitLab Runner on AWS EC2](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/) with the default settings mentioned above.

Happy with the presets?

```python
# Example automatically generated from non-compiling source. May contain errors.
GitlabRunnerAutoscaling(self, "Runner",
    gitlab_token="<auth token>"
)
```

## Projen

This project uses [projen](https://github.com/projen/projen) to maintain project configuration through code. Thus, the synthesized files with projen should never be manually edited (in fact, projen enforces that).

To modify the project setup, you should interact with rich strongly-typed
class [AwsCdkTypeScriptApp](https://github.com/projen/projen/blob/master/API.md#projen-awscdktypescriptapp) and
execute `npx projen` to update project configuration files.

> In simple words, developers can only modify `.projenrc.js` file for configuration/maintenance and files under `/src` directory for development.

See also [Create and Publish CDK Constructs Using projen and jsii](https://github.com/seeebiii/projen-test).
