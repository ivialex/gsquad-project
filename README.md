
# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## Dockerfile
The first thing we need to do is define from what image we want to build from. Here we will use the latest LTS (long term support) version 14 of node available from the Docker Hu
```
FROM node:14
```

Environmet Variables
```
ENV NODE_ENV=dev
ENV PORT=3000
```

Bundle app source
To bundle your app's source code inside the Docker image, use the COPY instruction
```
COPY . /app
```
create a directory to hold the application code inside the image, this will be the working directory for your application:
```
WORKDIR /app
```

Install app dependencies
```
RUN npm install
```

Your app binds to port $PORT so you'll use the EXPOSE instruction to have it mapped by the docker daemon
```
EXPOSE $PORT
```
Last but not least, define the command to run your app using CMD which defines your runtime.  Here we will use npm start to start app
```
ENTRYPOINT ["npm", "start"]
```

#Kubernetes Manifest
Here is kubernetes manifest that we are using in CDK EKS. You must change the name of your image and port for your containter if necessary.

```
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
                                "ports": [{"containerPort": 3000
                                
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
```

# Steps

1. Run command to build the image for your Docker file. For example:
   ```
   docker build . -t ivisilva/node-app:latest
   ```
2. Run command to push the image for your Docker Registry Repository. For example:
   ```
   docker push ivisilva/node-app:latest
   ```
3. Run `cdk deploy` to create all infrastructure and deploy kubernetes manifest
4. After finalize command `cdk deploy`, run `kubectl get deploy` to verify the deployments.
5. Run `kubectl get pods` to verify the pods.
6. Run `kubectl get svc` to get URL/port for load balancer.
7. And, finally, go to your browser and put in URL/port of the Load Balancer

Enjoy!
