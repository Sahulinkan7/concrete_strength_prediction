import logging
from datetime import datetime
import os


log_dir = "logs"
log_filename = f"log_{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(name)s %(levelname)s ] : %(message)s",
    filename=log_file_path,
)
