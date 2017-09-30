#!/bin/bash
./createTransforms.sh
/data/spark15/bin/spark-sql -f transforms.sql
/data/spark15/bin/spark-sql -f secondtransforms.sql
