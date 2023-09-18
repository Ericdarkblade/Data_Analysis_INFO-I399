  ### Customer:
- CustomerID
- Email* 
- Name (first,middle,last)
- Phone_Number* 
- Address(Street, City, Zip) [optional, in case we want to offer shipping as an extra option to our customers]
- 
### Employee:
- EmployeeID
- Name (first, middle, last)
- DOB (MM,DD,YYYY)
- Phone_Number*
- Email*
- Start_Date
- End_Date
- 
    ### Suppliers:
- Company_Name
- Company_Address(Street, City, Zip, State)
- Company_Phone
- Company_Email
  #### [If applicable] Representative:
- Name (F,L)
- Title
- Work Phone
- Work Email
- 
    ### Inventory:
- Item__ID
- Item_Name
- Repair  ### Supplies:
- Item_Cost
- {Suppliers}: will be using supplier id foreign key
- Refurbished-    ### Inventory:
- Invested_Cost
- Sale_Price
- {common_devices} //There could  be a MISC 0000 common device.
- Graveyard: (This would be super helpful for a repair shop)
- {Device_Model}
- {Item IDS}* //Would be functioning supplies that can be used from donated devices, or theoretical functioning supplies.
     ### models:
- Manufacturer
- Model
- Documentation
- Common_Parts*
- {Services available}*
     ### Shifts:
- Date(MM,DD,YYYY)
- {Scheduled Employees}
- Start Time
- End Time
     ### Hours:
- {Shift}
- Clock_In_Time
- Clock_Out_Time
- Repair  ### Services:
- ServiceID
- Service_Name (Example, screen repair, battery replacement, virus cleaning)
- Flat-Fee
- 
     ### Device_Ticket:
- Ticket_ID
- Device Name
- {Device_Model}
- {Customer}
- {Services offered}*
- {Parts Used}
- 
    ### Ticket_Log:
- Date (MM,DD,YY)
- {Employee}
- Time (HH:MM:SS)
- Message
### Invoices:
- Date
- Price
### Customer Receipts:
- {Customer}
- {Ticket ID}
- Payment Information
### Supplier Orders:
- {Supplier}
- {Parts Ordered}*
- {Quantities Ordered}*
### Employee Invoices:
- {Employee ID}
- {Hours}
- 