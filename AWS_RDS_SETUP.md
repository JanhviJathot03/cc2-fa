# AWS RDS Setup Guide for Expense Tracker

## Step 1: Create RDS Instance

1. **Login to AWS Console**
   - Go to AWS Management Console
   - Navigate to RDS service

2. **Create Database**
   - Click "Create database"
   - Choose "Standard create"
   - Select "MySQL" as engine type
   - Version: MySQL 8.0 (latest)

3. **Instance Configuration**
   - Choose "Free tier" template for testing
   - DB instance identifier: `expense-tracker-db`
   - Master username: `admin`
   - Set a strong master password

4. **Connectivity**
   - VPC: Default VPC
   - Public access: Yes (for development)
   - VPC security group: Create new
   - Availability Zone: No preference

5. **Additional Configuration**
   - Initial database name: `expense_tracker`
   - Enable automated backups (optional)

## Step 2: Configure Security Group

1. **Find your RDS Security Group**
   - Go to EC2 → Security Groups
   - Find the security group created for your RDS instance

2. **Add Inbound Rule**
   - Type: MySQL/Aurora
   - Protocol: TCP
   - Port: 3306
   - Source: Your IP address (or 0.0.0.0/0 for testing)

## Step 3: Get Connection Details

After RDS instance is created:

1. **Find Endpoint**
   - Go to RDS → Databases
   - Click your database instance
   - Copy the "Endpoint" (e.g., `expense-tracker-db.xyz.region.rds.amazonaws.com`)

2. **Note the Details**
   - Endpoint: `your-endpoint.region.rds.amazonaws.com`
   - Port: `3306`
   - Username: `admin`
   - Password: `your-password`
   - Database: `expense_tracker`

## Step 4: Test Connection

You can test the connection using MySQL client:

```bash
mysql -h your-endpoint.region.rds.amazonaws.com -u admin -p expense_tracker
```

## Step 5: Update Environment Variables

Create a `.env` file in your project directory:

```
RDS_HOST=your-endpoint.region.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=your-password
RDS_DATABASE=expense_tracker
RDS_PORT=3306
```

## Cost Optimization

- Use **Free Tier** for development (750 hours/month)
- **Stop** the instance when not in use
- **Delete** snapshots if not needed
- Consider **Reserved Instances** for production

## Security Best Practices

1. **Use Strong Passwords**
2. **Enable SSL/TLS** encryption
3. **Restrict Security Groups** to specific IPs
4. **Enable Backup** and point-in-time recovery
5. **Use IAM Database Authentication** for production

## Troubleshooting

### Connection Timeout
- Check security group inbound rules
- Verify your IP address is whitelisted
- Ensure RDS instance is in "Available" state

### Access Denied
- Verify username/password
- Check if database name exists
- Ensure user has proper permissions

### DNS Resolution
- Use the full RDS endpoint
- Check if endpoint is accessible from your network
