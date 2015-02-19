# aws-fix-emr-vis-tags
This project goal is to fix issues with amazon EMR when launched from data pipeline. 

The script deals with two issues I encountered:
1. EMR cluster is visible only to the user who have created it.
2. One can not add tags to EMR cluster.

How to use:
1. Download the script.
2. Set your access key and secret key (Make sure you have permissions for the above tasks).
3. Add it as a bootstrap action for the EMR with tags as parameters(key,value,key...)**

**I think its easier to try it on a running EMR first.

Its my first and only python code so its can probably be done better.
