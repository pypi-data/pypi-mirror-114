import os
COLORIZE_LOGS = os.getenv('DSO_COLORIZE_LOGS', 'Yes').lower() in ['yes', 'true']
BOLD_LOGS = os.getenv('DSO_BOLD_LOGS', 'Yes').lower() in ['yes', 'true']
TIMESTAMP_LOGS = os.getenv('DSO_TIMESTAMP_LOGS', 'Yes').lower() in ['yes', 'true']
LABEL_LOG_LEVELS = os.getenv('DSO_LABEL_LOG_LEVELS', 'Yes').lower() in ['yes', 'true']
USE_PAGER = os.getenv('DSO_USE_PAGER', 'Yes').lower() in ['yes', 'true']
ALLOW_STAGE_TEMPLATES = os.getenv('DSO_ALLOW_STAGE_TEMPLATES', 'No').lower() in ['yes', 'true']


