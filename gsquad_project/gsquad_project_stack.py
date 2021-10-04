from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_eks as eks
)

from aws_cdk import core as cdk


class GsquadProjectStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 vpc_id: str,
                 account_id: str,
                 availability_zones,
                 private_subnet_ids,
                 public_subnet_ids,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_vpc_attributes(self,
                                          "EKSVPC",
                                          vpc_id=vpc_id,
                                          availability_zones=availability_zones,
                                          private_subnet_ids=private_subnet_ids,
                                          public_subnet_ids=public_subnet_ids)

        eks_cluster_role = iam.Role(self,
                                    "EKSCLUSTERADMIN",
                                    assumed_by=iam.CompositePrincipal(iam.ServicePrincipal(service='eks.amazonaws.com'),
                                                                      iam.ServicePrincipal(service='arn:aws:iam::{}:root'.format(account_id))),
                                    role_name='EKS-CLUSTER-DEV-GSQUAD-ROLE-ADMIN',
                                    managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess'),
                                                      iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSClusterPolicy')])

        eks_node_role = iam.Role(self,
                                    "EKSNODEROLE",
                                    assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
                                    role_name='EKS-NODEGROUP-DEV-GSQUAD-ROLE',
                                    managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSWorkerNodePolicy'),
                                                      iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEC2ContainerRegistryReadOnly'),
                                                      iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKS_CNI_Policy')])

        eks_cluster_instance_profile = iam.CfnInstanceProfile(self,
                                                              'EKSCLUSTERINSTANCEPROFILE',
                                                              roles=[eks_cluster_role.role_name],
                                                              instance_profile_name='EKS-CLUSTER-DEV-GSQUAD-ROLE-ADMIN')

        eks_cluster = eks.Cluster(self,
                                  'development',
                                  cluster_name='EKS-CLUSTER-DEV-GSQUAD',
                                  default_capacity=0,
                                  vpc=vpc,
                                  version=eks.KubernetesVersion.V1_19,
                                  vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)],
                                  masters_role=eks_cluster_role
                                  )

        eks_nodegroup = eks_cluster.add_nodegroup_capacity('EKS-NODEGROUP-DEV-GSQUAD',
                                                           instance_types=[ec2.InstanceType('t3.medium'),
                                                                           ec2.InstanceType('t3.large'),
                                                                           ec2.InstanceType('t3.xlarge')],
                                                           disk_size=50,
                                                           min_size=2,
                                                           max_size=4,
                                                           desired_size=3,
                                                           subnets=ec2.SubnetSelection(
                                                               subnet_type=ec2.SubnetType.PRIVATE),
                                                           node_role=eks_node_role
                                                           )

        appLabel = {"app": "gsquad-k8s"}

        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "gsquad-kubernetes"},
            "spec": {
                "replicas": 3,
                "selector": {"matchLabels": appLabel},
                "template": {
                    "metadata": {"labels": appLabel},
                    "spec": {
                        "containers": [
                            {
                                "name": "gsquad-kubernetes",
                                "image": "ivisilva/node-app:latest",
                                "ports": [{"containerPort": 3000}]
                            }
                        ]
                    }
                }
            }
        }

        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "gsquad-kubernetes"},
            "spec": {
                "type": "LoadBalancer",
                "ports": [{"port": 8080, "targetPort": 3000}],
                "selector": appLabel
            }
        }

        eks_cluster.add_manifest('k8s-manifest', service, deployment)
