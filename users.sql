grant insert on employee to admin;

grant all on Employee, Customer, Transaction, Orders, Model, Inventory to admin with grant option; 

grant select on revenue_report to admin; 
grant select on frequency_report to admin; 
grant select on order_report to admin; 
grant select on employee_expense to admin; 
grant select on model_expense to admin; 

grant select, update on customer to sales; 
grant insert,select on orders to sales;

grant update on Model to engineer;
grant update on Inventory to engineer; 

create view engineer_view as select employee."firstName", employee."lastName", employee."employeeID", employee."jobType" from Employee; 
Grant select on engineer_view to engineer; 

grant select, update on Employee to HR;
create view employee_sales as select count(transaction."orderNumber"),transaction."employeeID" from Transaction group by transaction."employeeID";
Grant select on employee_sales to HR;

grant insert,update on orders to customer;
grant select on model to customer;


create user Mark1263 with password 'pass';
create user Ismael4557 with password 'pass';
create user Louis8989 with password 'pass';
create user Bryan8585 with password 'pass';
create user Jose8908 with password 'pass';

grant customer to Mark1263;
grant customer to Ismael4557;
grant customer to Louis8989;
grant customer to Bryan8585;
grant customer to Jose8908;

create user Drew5655 with password 'pass';
create user Yeslin9984 with password 'pass';
create user Arieni2344 with password 'pass';
create user Darryl2989 with password 'pass';
create user Victor6643 with password 'pass';

grant engineer to Drew5655;
grant engineer to Yeslin9984;
grant HR to Arieni2344;
grant HR to Darryl2989;
grant sales to Victor6643;


create user admin1 with password 'pass';
grant admin to admin1;
