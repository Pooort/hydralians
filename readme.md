sudo mongoexport --db hydralians --collection products --type=csv --fields _id,url,codag,description,price,product_brand,product_name,ref,seq,spec,tax --out /mnt/Ubuntu_1/data.csv

sudo cp -a /home/ubuntu_1/hydralians/files /mnt/Ubuntu_1/