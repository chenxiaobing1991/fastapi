import os

config={
    "default":{
        "host":os.getenv('DB_HOST','192.168.0.137'),
        "database":os.getenv('DB_DATABASE','sales_performance'),
        "port":os.getenv('DB_PORT','3308'),
        "username":os.getenv('DB_USERNAME','chengxiaobing'),
        "password":os.getenv('DB_PASSWORD','LkAspYWOpHEAdEzGWwAm'),
        "pool":{
            "pool_pre_ping":True,
            "pool_size":10,
            "max_overflow":10
        }
    }
}