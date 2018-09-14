# Simple deploy web application On Kubernetes using AWS Cloud 9





## Scenario
Any containerized application typically consists of multiple containers. There are containers for the application itself, a database, possibly a web server, and so on. During development, it’s normal to build and test this multi-container application on a single host. This approach works fine during early dev and test cycles but becomes a single point of failure for production, when application availability is critical.

In such cases, a multi-container application can be deployed on multiple hosts. Customers may need an external tool to manage such multi-container, multi-host deployments. Container orchestration frameworks provide the capability of cluster management, scheduling containers on different hosts, service discovery and load balancing, crash recovery, and other related functionalities. There are multiple options for container orchestration on Amazon Web Services: Amazon ECS, Docker for AWS, and DC/OS.

Another popular option for container orchestration on AWS is Kubernetes. There are multiple ways to run a Kubernetes cluster on AWS. This multi-part blog series provides a brief overview and explains some of these approaches in detail. This first post explains how to create a Kubernetes cluster on AWS using kops.


## Prerequisites

* The workshop’s region will be in ‘N.Virginia’


## Lab tutorial
### Create Cloud9 IDE Environment
1.1. First, click the below url, this is an AWS Cloudformation link. This CloudFormation template will spin up the Cloud9 IDE, as well as configure the IDE environment for the rest of the workshop.

    https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=k8s-workshop&templateURL=https://s3.amazonaws.com/aws-kubernetes-artifacts/lab-ide-novpc.template


1.2. Click **Next**.

1.3. Assign a**Subnetid** for this environment.

![1.png](/images/1.png)

1.4. Click **Next** until at review page.

1.5. Scroll down and select **confirm** option.

![2.png](/images/2.png)

1.6. Click **Create**.

1.7. When created complete, select **k8s-workshop**, click **output**, click the **url**, it will take you to cloud9 environment.

![3.png](/images/3.png)

1.8. Open the **AWS Cloud9** menu, go to **Preferences**, go to **AWS Settings**, and disable **AWS managed temporary credentials** as depicted in the diagram here.

![7.png](/images/7.png)

1.9. Copy below command and paste into terminal to get the resource which workshop needs.

     git clone https://github.com/ecloudvalley/Simple-deploy-web-application-on-Kubernetes-using-AWS-Cloud-9.git


![4.png](/images/4.png)

![5.png](/images/5.png)

1.10. Copy below command and paste into terminal.

    $ cd Simple-deploy-web-application-on-Kubernetes-using-AWS-Cloud-9
    $ git config --global credential.helper '!aws codecommit credential-helper $@'
    $ git config --global credential.UseHttpPath true
    $ chmod +x ide_build_script.sh


1.11. Copy below command and paste into terminal, this command helps you run a script.

    $ . ide_build_script.sh


1.12. The build script installs the following:

* jq
* kubectl (the Kubernetes CLI, which we’ll cover in great detail later in the workshop)
* kops (Kubernetes Operations, which we’ll also cover in detail later)
* configures the AWS CLI and stores necessary environment variables in bash_profile
* creates an SSH key

1.13. When it all finished, you can try to type **kops get nodes** in terminal, if it responded **Cluster.kops "nodes" not found**, that means your kops is installed successfully

![6.png](/images/6.png)



1.14. Now, environment settings are finished, next, we will create your first kubernetes cluster.


### Create Kubernetes Cluster

2.1. Copy below command and paste into the termianl, this command helps you to create the master and worker nodes.

    $ kops create cluster \
          --name example.cluster.k8s.local \
          --zones $AWS_AVAILABILITY_ZONES \
          --yes


2.2. When it created complete, wait for 5-8 minute, try to use **kops validate cluster** to see the cluster is working or not.

![8.png](/images/8.png)

2.3. Now, you have your own kubernetes cluster, that tries to deploy some web application on it.

>First we need to make a DockerImage for our web application.
>
>This workshop already have the sample, so you just need to build the image

### Try to Deploy web application on K8S

3.1. Go to **AWS Manage Console**, in the service menu, choose **Elastic Container Service**.

3.2. Click **Repositories**.

3.3. Create repositories named **kubernetes-ecr**.

3.4. Remember the **Repository URI**, it will be used later.

3.5. Click **Next step**.

![9.png](/images/9.png)

> We also need to give our cloud9’s ec2 a permission to push the image in our repository.

3.6. In the Service Menu, find **IAM**.

3.7. Click **Roles** at the left panel.

3.8. Find **k8s-workshop-LabIdeRole-XXXXXXXXXXXX**.

3.9. Click **Attach Policy**.

3.10. In the filter, type **AmazonEC2ContainerRegistryPowerUser**, and select it.

3.11. Click **Attach policy**.

3.12. Go back to cloud9, Copy below command and paste into terminal.

    $ aws ecr get-login --no-include-email

3.13. It will respond you a long command, copy it and paste it into terminal again.

![10.png](/images/10.png)

3.14. Copy below command and paste into terminal, these docker commands help you build the docker image and push it to AWS ECR.

    $ docker build -t <your-repository>:latest .
    $ docker tag <your-repository>:latest <your-repository>:first
    $ docker push <your-repository>:latest
    $ docker push <your-repository>:first
    
> Now go back to the AWS ECR, then you will see the image you have builded and pushed previously

3.15. Go back Cloud9 and open the **Deployment.yaml** at the left panel. Remember to change the image.

![11.png](/images/11.png)

3.16. Save it, back to terminal, copy below command and paste it into terminal, this command helps you create a deployment using kubernetes cli.

    $ kubectl create -f Deployment.yaml --record
    $ kubectl describe deployment/testwebapp-deployment
    
3.17. You will see the deployment detail if you deploy successfully.

![12.png](/images/12.png)

> Now we have the pods, we need a Service to connect our Web application

3.18. Copy below command and paste into terminal, this command help you create a service.

    $ kubectl create -f Service.yaml --record
    $ kubectl describe svc/testwebapp-service
> You can open Service.yaml to see the structure.

3.19. You will see the deployment detail if you deploy successfully, and please note the **Loadbalancer ingress**.
    
![13.png](/images/13.png)

3.20. Open a web page and type **http://your-loadbalacer-ingress**, you will see a website that deploys on kubernetes, try to reload it, and you will see it hosted in a different pod

![14.png](/images/14.png)
![15.png](/images/15.png)

### Scale the Pod

4.1. Copy below command and paste into terminal.

    $ kubectl scale --replicas=5 deployment/testwebapp-deployment
    $ kubectl get pods
    
4.2. You will see the pods had been scale up.

![16.png](/images/16.png)

4.3. And we can see the deployment history by using below command.

    $ kubectl rollout history deployment/testwebapp-deployment
    
### Try to Update Our Web Application

5.1. Go to **app.py** and change **First version kubernetes** to **Second version kubernetes**.

5.2. Save and build the image.

5.3. Use below code to build and push.

    docker build -t <your-repository>:latest .
    docker tag <your-repository>:latest <your-repository>:second
    docker push <your-repository>:latest
    docker push <your-repository>:second

5.4. Copy and Paste below code.

    $ kubectl edit deployment/testwebapp-deployment
    
5.5. Change the image URL.

![17.png](/images/17.png)

5.6. Save it and reload the Web page, and you will see the content had changed.

![18.png](/images/18.png)

### Limit Pods Memory and CPU Resource

6.1. Execute below command and add **resource** code in the testwebapp-deployment.

    $ kubectl edit deployment/testwebapp-deployment

6.2. Copy resource code and add in **Deployment.template.spec.container**.

    resources:
      limits:
        memory: "200Mi"
        cpu: 2
      requests:
        memory: "100Mi"
        cpu: 1

>You can use **kubectl describe pods** to see all pods detail, and you can see, it really behave the limit and request. If we don’t give it limit and request, the default is allocated no memory request/limit and 100m CPU request and no limit, that try to prove it.
First, we need to rollback the previous revision, use **kubectl rollout history deployment/testwebapp-deployment** can see the revision id.

6.3. Copy below command and paste into terminal, this command helps you to rollback the specify revision

    $ kubectl rollout undo deployment/testwebapp-deployment --to-revision=1
    
>You can use kubectl describe pods to see the resource limit/request are disappear or not.

6.4. Now you can use below command to see the resource limit and request.

    $ kubectl get pod/<pod-name> -o jsonpath={.spec.containers[].resources}

### Clean Resource

7.1. That all, now clean the clusters, use below command to clean up.

    $ kops delete cluster example.cluster.k8s.local --yes


## Conclusion

Congratulations! You now have learned how to:
* Use Cloud9 to Deploy web application on k8s.
* Using kubectl to deploy and service.



