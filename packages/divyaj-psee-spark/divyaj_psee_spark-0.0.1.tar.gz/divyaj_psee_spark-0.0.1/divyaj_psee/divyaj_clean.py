import subprocess

def delete_files(names):
    """
    Delete files from HDFS

    Parameters:

    names: list of file names with paths from the "files_in_hdfs" text file.

    Return:

    None
    """    
    
    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    local_record_path = subprocess.check_output(["pwd"]).decode("utf-8")[:15]

    for name in names:
        try:
            command = ['hdfs', 'dfs', '-rm', '-r', '-f', hdfs_path+name]
            subprocess.check_output(command)

        except:
            continue

    with open(local_record_path+"files_in_hdfs.txt","r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if line[:-1] not in names:
                f.write(line)
        f.truncate()