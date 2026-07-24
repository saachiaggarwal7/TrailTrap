HONEY_USERS = [
    {
        "username": "backup-admin",
        "role":"backup",
        "policy_name": "InfrastructureBackupAccess",
        "bucket": "company-backups-archive-v1-fc",
        "files": [

            {
                "key": "production/app.env",
                "template": "templates/company-backups/production/app.env"
            },

            {
                "key": "production/mysql_backup.sql",
                "template": "templates/company-backups/production/mysql_backup.sql"
            },

            {
                "key": "production/backup-config.yaml",
                "template": "templates/company-backups/production/backup-config.yaml"
            },

            {
                "key": "logs/backup-service.log",
                "template": "templates/company-backups/logs/backup-service.log"
            },

            {
                "key": "configs/backup-policy.json",
                "template": "templates/company-backups/configs/backup-policy.json"
            },

            {
                "key": "README.txt",
                "template": "templates/company-backups/README.txt"
            }

        ]
    },

    {
        "username": "legacy-service",
        "bucket": "finance-reports-storage-v1-fc",
        "roles":"finance",
        "policy_name": "FinanceReportsAccess",
        "files":[

            {
                "key":"payroll/salary_backup.csv",
                "template":"templates/finance/payroll/salary_backup.csv"
            },

            {
                "key":"reports/financial_report_Q2_2025.csv",
                "template":"templates/finance/reports/financial_report_Q2_2025.csv"
            },

            {
                "key":"tax/gst_summary.txt",
                "template":"templates/finance/tax/gst_summary.txt"
            },

            {
                "key":"audit/internal_audit.log",
                "template":"templates/finance/audit/internal_audit.log"
            },

            {
                "key":"README.txt",
                "template":"templates/finance/README.txt"
            }

        ]
    },

    {
        "username":"old-deployment-user",
        "role":"devops",
        "policy_name": "LegacyDeploymentReadOnly",
        "bucket":None,

        "files":[]
    }

]
HONEY_USERNAME=["backup-admin","old-deployment-user","legacy-service"]