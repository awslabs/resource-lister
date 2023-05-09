#  Resource Lister (Multi Accounts)
Resource Lister is an open source, **NO CODE**, interactive, python-based command line utility. Resource Lister can generate list of AWS resources (for **supported services**) in single or multiple accounts in consumable CSV, or flatten JSON format. Resource Lister uses AWS SDK for Python(Boto3) sessions and underlying Boto3 List APIs to connect multiple configured child accounts and generate the  resource list. It essentially **simplifies** accessing of Boto3 list APIs. Resource Lister also provides an option to send generated list to  file,  s3, or print on command line.
Resource Lister can be configured to run from Cloud9, Cloudshell, EC2 or from your machine.

# Usage: 

Resource Lister Utility can be helpful to addresses following usecase

* Resource Lister is handy utility for Developers, Solution Architect, Account Owners, Cloud Ops team or anyone who simply wants to generate list of AWS Resources (for **supported services**) across accounts and across regions without writing any custom code. 

* Utility can help generate list of inventory of AWS resources across region and across accounts in near real time. For example, operation team wants to verify there is no lambda function created in restricted regions in near real time. You can also run the utility in batch mode across all the configured AWS services and create inventory.

* Utility can help enforce budgetary constraints. For example, utility can help Account owners to identify which AWS accounts doesn't have AWS budget setup.

* Utility can help identify particular type of list of resources.
for example, you can generate list of lambda function and filter lambda function using python 2.6 version.

* Utility flattens the response in consumable csv format.






# How it works?

<p align="center">
  <img src="imgs/0_utility_interface.PNG"  title="Utility Interface">

After you install and configure the Resource Lister you can run the Resource lister utility using pipx run.

```
pipx run resource_lister
```



**1** .  **Select AWS Service** : Resource Lister Utility will prompt you to select the AWS Service: You can select any of 27 services example S3, lambda or ec2

**2** .  **Select Function**: Resource Lister Utility will display number of supported functions for selected AWS service: Example List of S3 buckets or List of Aurora DB clusters or List of Lambda functions depending upon service you selected.

**3** . **Select Account(s)**: Resource Lister Utility will prompt you to select AWS Account for which you want to generate list of AWS resources:  You can enter ALL to select all the accounts or you can enter single account or comma separated list of accounts. If you don’t know the account number you just press ENTER and utility will prompt you with list of configured accounts. 

**4** . **Select Region(s) for Regional services**: If it's regional resource (example Lambda) you will prompt to select AWS Region; you can select ALL for all the regions or specify comma separated list of regions

**5** . **Result**: Resource lister utility will then generates the list of AWS Resources for selected accounts and regions send the output to file or S3 Bucket or print on command prompt depending upon your configuration.

<p align="center">
  <img src="imgs/01_utility_interface.PNG"  title="Utility Interface">

**Output**
<p align="center">
  <img src="imgs/02_utility_output.PNG"  title="Utility Interface">



**Note** : You can also run the utility in batch mode across all the services in selected AWS Account by going to help --> option # 6


# Prerequisite
1. [Python](https://www.python.org/)
2. [AWS CLI](https://aws.amazon.com/cli/)

# Installation

You can install and run **Resource lister** using [pipx](https://pypa.github.io/pipx/)

**On macOS, Linux, install via pip (requires pip 19.0 or later)**
```
python3 -m pip install  pipx
python3 -m pip install  boto3
python3 -m pipx install resource-lister
```
**On Windows, install via pip (requires pip 19.0 or later)**

If you installed python using the app-store, replace `python` with `python3` in the next line.
```
python -m pip install pipx
python -m pip install boto3
python -m pipx install resource-lister
```

**Run the Resource Lister Utility using pipx**

**On macOS, Linux, install via pip (requires pip 19.0 or later)**
```
python3 -m pipx run resource_lister
```
**On Windows, install via pip (requires pip 19.0 or later)**

```
python -m pipx run resource_lister
```

Resource lister utility will open in command prompt

<p align="center">
  <img src="imgs/05_install_01.PNG"  title="Utility Interface">

# Setup
<details>

  <summary>
  <b>Express setup for single account using default credentials. </b>
  </summary>
You will use default IAM credentials for this setup. Ensure your current default credentials should have <b>read only permissions</b> 


<b>Step1 : Navigate to  "Add Master Account"  </b>

Type <b>help</b>--><b>1</b> [Manage AWS Account]--><b>1</b> [Add Master Account.]

<p align="center">
  <img src="imgs/express_setup_01.PNG"  title="Utility Interface">



<b>Step2 : Configure Master account with dummy values </b>

Since express setup we are using default credentials. Use dummy values for Master Account ARN like **arn:aws:iam::<Your 12 Digit Account>:role/dummy_role** and for child account role name enter **dummy_role**


<p align="center">
  <img src="imgs/express_setup_02.PNG"  title="Utility Interface">

<b>Congratulations! AWS Account is successfully configured. </b>

<b>Step3: Navigate back to main search </b>


Type 0 to exit
<b>0</b>--><b>0</b>

<p align="center">
  <img src="imgs/express_setup_03.PNG"  title="Utility Interface">


<b>Step4 : Test Utility by generating list of s3 buckets .csv file  </b>

Enter AWS service for help (help) for Exit (0) :--><b>s3</b>

Please select any of following options:
1. [List of S3 buckets]
2. [List of the objects in a S3 Bucket]
Please enter option HERE--><b>1</b>

Please enter comma separated account id(s) or ALL  HERE--><b>ALL</b>


<p align="center">
  <img src="imgs/01_utility_interface.PNG"  title="Utility Interface">

Utility will create output folder and generate the .csv file with list of s3 buckets in your account.

<p align="center">
  <img src="imgs/02_utility_output.PNG"  title="Utility Interface">



  </details>



<details> 
<summary>
<b>Multi Account configurations.
</b>
</summary>



- [Cloud9 setup](https://github.com/awslabs/resource-lister/blob/main/docs/cloud_9_setup.md)

- [Cloudshell setup](https://github.com/awslabs/resource-lister/blob/main/docs/cloudshell_setup.md)



</details>

# Help
[General help](https://github.com/awslabs/resource-lister/blob/main/docs/help_guide.md)

# Supported Services and Functionality
<details> 
<summary>
<b> Supported Services and Functionality  </b>
</summary>
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
<li>13.Describes the specified Elastic IP addresses </li>
<li>14.List of VPCs</li>
<li>15.List of EBS volumes</li>
<li>16.List of flow logs </li>
<li>17.List of Network ACLs</li>
<li>18.List of Route tables</li>
<li>19.List of Security Groups</li>
<li>20.List of Security Group Rules</li>
<li>21.List of all the snapshots (self taken)</li>
<li>22.List of Subnets</li>
<li>23.List of Transit Gateways (TGW)</li>
<li>24.List of VPC endpoints</li>
<li>25.List of all the VPC Peering connections</li>
<li>26.List of VPN connections</li>
</ul>
</td>
</tr>
<tr>
<td> ecs</td>
<td>
<ul>
<li>27.List of ECS clusters</li>
<li>28.List of  ECS Services in specified ECS Cluster</li>
<li>29.List ECS Tasks in specified ECS Cluster</li>
</ul>
</td>
</tr>
<tr>
<td> efs</td>
<td>
<ul>
<li>30.List of EFS</li>
</ul>
</td>
</tr>
<tr>
<td> eks</td>
<td>
<ul>
<li>31.Describe details of specified EKS Cluster</li>
<li>32.List of EKS Clusters</li>
<li>33.List EKS Fargate profiles in specified EKS Cluster</li>
</ul>
</td>
</tr>
<tr>
<td> elbv2</td>
<td>
<ul>
<li>34.List of load balancers (Application, Network) </li>
</ul>
</td>
</tr>
<tr>
<td> emr</td>
<td>
<ul>
<li>35.List of Provisioned EMR Clusters</li>
<li>36.List of notebook executions.</li>
<li>37.List of all the EMR Studios </li>
<li>38.List of Instance fleets for specific EMR cluster</li>
</ul>
</td>
</tr>
<tr>
<td> emr-serverless</td>
<td>
<ul>
<li>39.List of EMR Serverless applications</li>
<li>40.List of EMR Serverless Job runs for specified EMR serverless application</li>
</ul>
</td>
</tr>
<tr>
<td> iam</td>
<td>
<ul>
<li>41.List of IAM Roles</li>
<li>42. List of Managed policies (AWS and Your owned)</li>
<li>43. List of IAM users</li>
</ul>
</td>
</tr>
<tr>
<td> kms</td>
<td>
<ul>
<li>44.List of KMS keys</li>
</ul>
</td>
</tr>
<tr>
<td> lambda</td>
<td>
<ul>
<li>45.List of Lambda functions</li>
<li>46.List of  Lambda layers </li>
</ul>
</td>
</tr>
<tr>
<td> organizations</td>
<td>
<ul>
<li>47. List of accounts in the organization </li>
<li>48. List of Service Control Policies (SCP) in an organization </li>
</ul>
</td>
</tr>
<tr>
<td> rds</td>
<td>
<ul>
<li>49.List of Aurora DB clusters</li>
<li>50.List of provisioned RDS instances </li>
<li>51.List  of DB Security Groups</li>
<li>52.List of Database Sanpshots</li>
<li>53.List of Global aurora clusters</li>
</ul>
</td>
</tr>
<tr>
<td> redshift</td>
<td>
<ul>
<li>54.List of Redshift clusters</li>
</ul>
</td>
</tr>
<tr>
<td> redshift-serverless</td>
<td>
<ul>
<li>55.List of Redshift serverless namespaces</li>
<li>56.List of Redshift serverless workgroups</li>
</ul>
</td>
</tr>
<tr>
<td> route53</td>
<td>
<ul>
<li>57.List of all the Route53 CIDRs </li>
<li>58.List of hosted zones(public and private)</li>
<li>59.List of  private hosted zones associated with specified VPC</li>
</ul>
</td>
</tr>
<tr>
<td> route53domains</td>
<td>
<ul>
<li>60.List of Route53 Domains</li>
<li>61.Info of Route53 Domain pricing</li>
</ul>
</td>
</tr>
<tr>
<td> s3</td>
<td>
<ul>
<li>62.List of S3 buckets</li>
<li>63.List of the objects in a S3 Bucket</li>
</ul>
</td>
</tr>
<tr>
<td> sagemaker</td>
<td>
<ul>
<li>64.List of SageMaker Domains</li>
<li>65.List of SageMaker Images</li>
<li>66.List of SageMaker Models</li>
<li>67.List of SageMaker Projects</li>
<li>68.List of SageMaker User Profiles</li>
</ul>
</td>
</tr>
<tr>
<td> sns</td>
<td>
<ul>
<li>69.List of SNS subscriptions</li>
<li>70.List of SNS topics</li>
</ul>
</td>
</tr>
<tr>
<td> sqs</td>
<td>
<ul>
<li>71.List of SQS queues</li>
</ul>
</td>
</tr>
<tr>
<td> ssm</td>
<td>
<ul>
<li>72.Describe Instance Information (OS version)</li>
</ul>
</td>
</tr>
</tbody>
</table>
</details> 




## License
This library is licensed under the Apache-2.0. See the LICENSE file.

## Considerations
* Resource-Lister makes list API calls using AWS SDK for Python(Boto3).These   list API calls will be applied to your [AWS Account List API Quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html). 

* Utiliy provide options to use existing IAM roles or to create new roles using utility provided cloudformation templates. If you decided to use utility provided cloudformation templates.  Master account cloudformation template will create **ReadonlyAccess** IAM role in master account .Child account cloudformation template will create **ReadOnlyAccess** IAM role in child account.   


* Most of the cases list generated by utility will have 99% of the attributes send back by Boto3 .Utility doesn't assure 100% attributes are covered. 

* When running utility more than 5 accounts,to avoid **memory issues**,It's recommended to generate Account wise file. Account wise file can be generated by changing configuration settting in help section . 
Help --> 6. [Manage Configurations (example : format_type, output_type)]-->5.[Modify  Seperate file for each AWS Account]-->change to **yes**

* Utility currently supports only 27 services and 70 functions. Utility is configuration driven so adding new function is easy. If you are interested in additional functions /features, please raise issue.

# Know issues/Pending items
* Improvements in error handling messages
* Help section is work in progress



