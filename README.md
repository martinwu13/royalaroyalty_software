# royalty_software
執行前必須確定電腦上有mysql server和以下條件
mysql的帳號必須使用root，沒有密碼  
執行以下sql指令以建立環境：
```sql
  CREATE DATABASE `royalty_db`;  
  CREATE TABLE `contract`(`cid` int(11),  
                          `bookname` varchar(100),  
                          `bookname` varchar(100),  
                          `unit` varchar(100),  
                          `authorized_area` varchar(100),  
                          `agent` varchar(100),  
                          `author` varchar(100),  
                          `calc_interval` int(11),  
                          `start_date` date,  
                          `end_date` date,  
                          `royalty1` float,  
                          `royalty2` float,  
                          `royalty3` float,  
                          `royalty4` varchar(100));
```
你的python環境要安裝mysql.connector套件  

