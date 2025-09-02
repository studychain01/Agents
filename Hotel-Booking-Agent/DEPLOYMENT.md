# AWS Deployment Guide

## Option 1: AWS App Runner (Recommended)

### Prerequisites
1. AWS CLI installed and configured
2. GitHub repository with your code
3. OpenAI and Browserbase API keys

### Step-by-Step Deployment

#### 1. Prepare Environment Variables
Your app needs these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `BROWSERBASE_API_KEY`: Your Browserbase API key

#### 2. Deploy via AWS Console

1. **Go to AWS App Runner Console**
   - Navigate to https://console.aws.amazon.com/apprunner/
   - Click "Create service"

2. **Source Configuration**
   - Repository type: "Source code repository"
   - Provider: "GitHub"
   - Connect to your GitHub account
   - Repository: `studychain01/Agents`
   - Branch: `main`
   - Deployment trigger: "Automatic"

3. **Build Configuration**
   - Configuration file: "Use configuration file"
   - This will use the `apprunner.yaml` file we created

4. **Service Configuration**
   - Service name: `hotel-booking-agent`
   - Virtual CPU: 1 vCPU
   - Memory: 2 GB

5. **Environment Variables**
   - Add your API keys as environment variables:
     - `OPENAI_API_KEY`: [Your OpenAI key]
     - `BROWSERBASE_API_KEY`: [Your Browserbase key]

6. **Security**
   - Auto scaling: Min 1, Max 3 instances
   - Health check: Default

7. **Review and Create**
   - Review all settings
   - Click "Create & deploy"

#### 3. Wait for Deployment
- Initial deployment takes 5-10 minutes
- You'll get a unique URL like: `https://xxx.us-east-1.awsapprunner.com`

### Alternative: Deploy via AWS CLI

```bash
# Create apprunner service
aws apprunner create-service \
  --service-name hotel-booking-agent \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "python:3.12-slim",
      "ImageConfiguration": {
        "Port": "8501"
      }
    },
    "AutoDeploymentsEnabled": true,
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/studychain01/Agents",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY"
      }
    }
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }'
```

## Option 2: AWS ECS with Fargate

### 1. Build and Push Docker Image

```bash
# Build image
docker build -t hotel-booking-agent .

# Test locally
docker run -p 8501:8501 hotel-booking-agent

# Tag for ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name hotel-booking-agent

# Tag and push
docker tag hotel-booking-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/hotel-booking-agent:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/hotel-booking-agent:latest
```

### 2. Create ECS Service
Use the AWS Console or CloudFormation to create:
- ECS Cluster
- Task Definition
- Service with Application Load Balancer

## Option 3: AWS EC2

### 1. Launch EC2 Instance
- AMI: Amazon Linux 2
- Instance type: t3.medium or larger
- Security group: Allow HTTP (80), HTTPS (443), SSH (22)

### 2. Install Dependencies
```bash
# Connect via SSH
sudo yum update -y
sudo yum install -y docker git

# Start Docker
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Clone repository
git clone https://github.com/studychain01/Agents.git
cd Agents/Hotel-Booking-Agent

# Build and run
docker build -t hotel-booking-agent .
docker run -d -p 80:8501 --env-file .env hotel-booking-agent
```

## Security Best Practices

1. **Use AWS Secrets Manager** for API keys
2. **Enable HTTPS** with AWS Certificate Manager
3. **Use AWS WAF** for web application firewall
4. **Enable CloudWatch** logging
5. **Set up AWS Backup** for data protection

## Cost Estimation

### App Runner
- ~$25-50/month for low traffic
- Auto-scales based on usage

### ECS Fargate
- ~$30-60/month for 1 task running 24/7
- More control over resources

### EC2
- ~$20-40/month for t3.medium
- Plus data transfer costs

## Monitoring

- **CloudWatch**: Logs and metrics
- **AWS X-Ray**: Distributed tracing
- **Health checks**: Built-in with App Runner/ECS

## Troubleshooting

1. **App not starting**: Check CloudWatch logs
2. **API errors**: Verify environment variables
3. **Performance issues**: Scale up instance size
4. **Playwright issues**: Ensure proper dependencies in Dockerfile
