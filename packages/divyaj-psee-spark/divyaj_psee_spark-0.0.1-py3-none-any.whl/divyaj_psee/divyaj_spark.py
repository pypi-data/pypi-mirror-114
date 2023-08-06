import subprocess
import pandas as pd
import findspark
findspark.init("/opt/cloudera/parcels/CDH/lib/spark")
from pyspark.sql import SparkSession
spark_session = (
    SparkSession.builder.master("yarn-client")
    .appName("app_name")
    .enableHiveSupport()
    .config("spark.executor.memory", "10G")
    .getOrCreate()
)

def spark_write(spark_dataframe, name):
    """
    Save an spark dataframe as csv file to HDFS from your JHUB

    Parameters:

    dataframe: spark dataframe which needs to be saved as a csv
    name: Name of the csv file you want to save (str). 
          Give the name if you want to save in the same directory as notebook or provide a full path

    Return:

    None
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    local_record_path = subprocess.check_output(["pwd"]).decode("utf-8")[:15]
    file = open(local_record_path+"files_in_hdfs.txt","a")
    
    if "/" in name:
        local_name = name.split("/")[-1]
        file_path = "/".join(name.split("/")[:-1])+"/"
        try:
            spark_dataframe.write.csv(hdfs_path+file_path+local_name)
            file.write(file_path+local_name+"\n")
            file.close()
        except:
            spark_dataframe.write.csv(hdfs_path+file_path+local_name, "overwrite")
        

        
    else:
        local_path = subprocess.check_output(["pwd"]).decode("utf-8")[7:-1]+"/"
        
        try:
            spark_dataframe.write.csv(hdfs_path+local_path+name)
            file.write(local_path+name+"\n")
            file.close()
        except:
            spark_dataframe.write.csv(hdfs_path+local_path+name, "overwrite")

    

def spark_read(name):
    """
    Read a csv file from HDFS to your JHUB as a spark dataframe

    Parameters:

    name: Name of the csv file you want to read (str). 
          Give the name if you have the file in the same directory as notebook or provide a full path

    Return:
    dataframe: Returns a spark dataframe
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    
    local_path = subprocess.check_output(["pwd"]).decode("utf-8")[:-1]+"/"
    
    if "/" in name:       

        get_df = spark_session.read.csv(hdfs_path+name)
    
    
    else:
    
        get_df = spark_session.read.csv(hdfs_path+local_path[7:]+name)
        
    return get_df