create domain str as varchar(100);

create domain bstr as varchar(1000);

create domain bbstr as varchar(5000);

create domain CP as int;

create domain tel as int;

create domain age as int
check (value between 0 and 122);

create domain dateCB as int;

create domain mail as str;
