#  Resource Lister (Multi Accounts)
Resource Lister is  open source, interactive, python-based command line **NO CODE** utility. Resource Lister can generate list of AWS resources in single or multiple accounts in consumable CSV, or flatten JSON format in near real time. Resource Lister uses boto3 sessions and underlying List APIs to connect multiple configured child accounts and generate the list. Resource Lister also provides an option to output generated list to command line, file ,and s3.
Multi Account Resource Lister can be configured to run from Cloud9, EC2 or from your local laptop.

# Usage : 

Resource lister utility is open source interactive command line tool for Developers, Solution Architect, Account Owners, Cloud Ops team or anyone who wants to simply list AWS Resources (for **supported services**) in an account or multiple accounts in consumable format like .csv without writing a code 

Cloud Operation team can generate inventory of AWS resources in near real time accorss accounts and across regions for **supported services** without writing any code.

Operation team can identify which AWS accounts doesn't have budget setup.

Utility can help generate list in particular account/region and then you can filter particular type of resource like lambda function using python 2.6 version.

Resource list generated through utility is with 99% of attributes which python SDK sends back (Including configured Tags for the resource), Manually getting and formatting all the attributes and formatting in tabular/columnize format specifically .csv is tedious task utility does it for you.


# How it works?

Run the utility 
Utility will start interactive Python session.

**Step 1**:  Utility will prompt you to select the AWS Service for example S3,lambda or ec2 etc..

**Step 2** : Utility will display number of supported functions for selected AWS service . You chose a perticular function for example  **List of S3 Buckets **

**Step 3** : Utility will prompt you to select AWS Account for which you want list of AWS resources, you can select ALL accounts by entering ALL or specify comma seperated list of accounts

**Step 4** : If it's regional resource (example Lambda) you will promopt to select AWS Region ; you can select ALL for all the regions or specify comma seperated list of regions

**Step 5**: Finally, utility will generate the list of AWS Resources for selected Accounts and Regions send the output to File or S3 Bucket or Print on command prompt depending upon your configuration.

You can also run the utility in batch mode across all the services in selected AWS Account 

<p align="center">
  <img src="imgs/01_utility_interface.PNG"  title="Utility Interface">

**Output**
<p align="center">
  <img src="imgs/02_utility_output.PNG"  title="Utility Interface">

# Prerequisite
1. python3
2. boto3


# Installation



**resource-lister** is distributed on PyPI. Easiest way to install it is with pip
Create a virtual environment (optional):

```
python3 -m venv .venv

```
Activate enviornment

```
source .venv/bin/activate
```

Install resource-lister

```
pip install resource-lister
```

# Run Resource Lister Utility

Download main.py from github

https://github.com/awslabs/resource-lister/blob/main/install/main.py

Run main.py python file with below command

```
python3 main.py
```

Utility will open in command prompt

<p align="center">
  <img src="imgs/05_install_01.PNG"  title="Utility Interface">

# setup

Click on enviornment specific installation setup.

- [Cloud9 setup](https://github.com/awslabs/resource-lister/blob/main/docs/cloud_9_setup.md)

- [Cloudshell setup](https://github.com/awslabs/resource-lister/blob/main/docs/cloud_9_setup.md)

- [Desktop setup](https://github.com/awslabs/resource-lister/blob/main/docs/cloud_9_setup.md)



# Help
[General help](https://github.com/awslabs/resource-lister/blob/main/docs/help_guide.md)


# Supported Services and Functionality 
<table>
<tbody>
<tr>
<th>Service</th>
<th>Functions</th>
</tr>
<tr>
<td> accessanalyzer</td>
<td>
<ul>
<li>1.List of IAM Analyzers</li>
<li>2.List of findings for specified  IAM Analyzer</li>
</ul>
</td>
</tr>
<tr>
<td> budgets</td>
<td>
<ul>
<li>3.List of budgets</li>
</ul>
</td>
</tr>
<tr>
<td> cloudformation</td>
<td>
<ul>
<li>4.List of Cloudformation Stacks</li>
</ul>
</td>
</tr>
<tr>
<td> cloudfront</td>
<td>
<ul>
<li>5.List of CloudFront distributions</li>
<li>6.List of CloudFront functions</li>
</ul>
</td>
</tr>
<tr>
<td> cloudtrail</td>
<td>
<ul>
<li>7.List of  Cloud Trails</li>
</ul>
</td>
</tr>
<tr>
<td> cloudwatch</td>
<td>
<ul>
<li>8.List of Cloudwatch Dashboards</li>
<li>9.List of Cloudwatch Metrics</li>
</ul>
</td>
</tr>
<tr>
<td> codecommit</td>
<td>
<ul>
<li>10.List of Code commit Repositories</li>
</ul>
</td>
</tr>
<tr>
<td> dynamodb</td>
<td>
<ul>
<li>11.List of DynamoDB tables</li>
</ul>
</td>
</tr>
<tr>
<td> ec2</td>
<td>
<ul>
<li>12.List of EC2 instances </li>
<li>13.List of VPCs</li>
<li>14.List of EBS volumes</li>
<li>15.List of flow logs </li>
<li>16.List of Network ACLs</li>
<li>17.List of Route tables</li>
<li>18.List of Security Groups</li>
<li>19.List of Security Group Rules</li>
<li>20.List of all the snapshots (self taken)</li>
<li>21.List of Subnets</li>
<li>22.List of Transit Gateways (TGW)</li>
<li>23.List of VPC endpoints</li>
<li>24.List of all the VPC Peering connections</li>
<li>25.List of VPN connections</li>
</ul>
</td>
</tr>
<tr>
<td> ecs</td>
<td>
<ul>
<li>26.List of ECS clusters</li>
<li>27.List of  ECS Services in specified ECS Cluster</li>
<li>28.List ECS Tasks in specified ECS Cluster</li>
</ul>
</td>
</tr>
<tr>
<td> efs</td>
<td>
<ul>
<li>29.List of EFS</li>
</ul>
</td>
</tr>
<tr>
<td> eks</td>
<td>
<ul>
<li>30.Describe details of specified EKS Cluster</li>
<li>31.List of EKS Clusters</li>
<li>32.List EKS Fargate profiles in specified EKS Cluster</li>
</ul>
</td>
</tr>
<tr>
<td> elbv2</td>
<td>
<ul>
<li>33.List of load balancers (Application, Network) </li>
</ul>
</td>
</tr>
<tr>
<td> emr</td>
<td>
<ul>
<li>34.List of Provisioned EMR Clusters</li>
<li>35.List of notebook executions.</li>
<li>36.List of all the EMR Studios </li>
<li>37.List of Instance fleets for specific EMR cluster</li>
</ul>
</td>
</tr>
<tr>
<td> emr-serverless</td>
<td>
<ul>
<li>38.List of EMR Serverless applications</li>
<li>39.List of EMR Serverless Job runs for specified EMR serverless application</li>
</ul>
</td>
</tr>
<tr>
<td> iam</td>
<td>
<ul>
<li>40.List of IAM Roles</li>
<li>41. List of Managed policies (AWS and Your owned)</li>
<li>42. List of IAM users</li>
</ul>
</td>
</tr>
<tr>
<td> kms</td>
<td>
<ul>
<li>43.List of KMS keys</li>
</ul>
</td>
</tr>
<tr>
<td> lambda</td>
<td>
<ul>
<li>44.List of Lambda functions</li>
<li>45.List of  Lambda layers </li>
</ul>
</td>
</tr>
<tr>
<td> organizations</td>
<td>
<ul>
<li>46. List of accounts in the organization </li>
<li>47. List of Service Control Policies (SCP) in an organization </li>
</ul>
</td>
</tr>
<tr>
<td> rds</td>
<td>
<ul>
<li>48.List of Aurora DB clusters</li>
<li>49.List of provisioned RDS instances </li>
<li>50.List  of DB Security Groups</li>
<li>51.List of Database Sanpshots</li>
<li>52.List of Global aurora clusters</li>
</ul>
</td>
</tr>
<tr>
<td> redshift</td>
<td>
<ul>
<li>53.List of Redshift clusters</li>
</ul>
</td>
</tr>
<tr>
<td> redshift-serverless</td>
<td>
<ul>
<li>54.List of Redshift serverless namespaces</li>
<li>55.List of Redshift serverless workgroups</li>
</ul>
</td>
</tr>
<tr>
<td> route53</td>
<td>
<ul>
<li>56.List of all the Route53 CIDRs </li>
<li>57.List of hosted zones(public and private)</li>
<li>58.List of  private hosted zones associated with specified VPC</li>
</ul>
</td>
</tr>
<tr>
<td> route53domains</td>
<td>
<ul>
<li>59.List of Route53 Domains</li>
<li>60.Info of Route53 Domain pricing</li>
</ul>
</td>
</tr>
<tr>
<td> s3</td>
<td>
<ul>
<li>61.List of S3 buckets</li>
<li>62.List of the objects in a S3 Bucket</li>
</ul>
</td>
</tr>
<tr>
<td> sagemaker</td>
<td>
<ul>
<li>63.List of SageMaker Domains</li>
<li>64.List of SageMaker Images</li>
<li>65.List of SageMaker Models</li>
<li>66.List of SageMaker Projects</li>
<li>67.List of SageMaker User Profiles</li>
</ul>
</td>
</tr>
<tr>
<td> sns</td>
<td>
<ul>
<li>68.List of SNS subscriptions</li>
<li>69.List of SNS topics</li>
</ul>
</td>
</tr>
<tr>
<td> sqs</td>
<td>
<ul>
<li>70.List of SQS queues</li>
</ul>
</td>
</tr>
</tbody>
<table>

## Pricing
Cloud9 Pricing: If you are using Cloud9 based setup.


## License
This library is licensed under the Apache-2.0. See the LICENSE file.

## Considerations
Resource-Lister creates boto3 sessions (master and child accounts) and invokes list APIs for the service you selected to list resources. These API calls will be applied to your account API Quotas. 
If you configured Resource-lister for multiple accoutns.You can use existing master and child account roles or create new roles.
If you decided to create new roles, You need to run cloudformation template in child account , cloudformation template will create IAM role in child account with read only permissions,this role will be assumed by master account.   
Utility currrenlty supports only 70 functions. If you are interested in addtional functions /features, Please raise issue.

# Know issues
Improvements in error handling messages


