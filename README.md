<h1>Little_lemon_restaurant API</h1>
This is a Google Capstone project from the online course provided by Coursera. The goal is to build an API project for the Little Lemon restaurant.

This project involves three types of users: managers, customers, and the delivery crew. Each user type has different roles. There is user registration and authentication process that each user will use,
then  API endpoints that can be used to assign users to a group like manager or a delivery person. 
<ol>
  <li>Manager Role:</li>
  <ul>
    <li>Managers can use specific API endpoints to add, edit, and remove menu items.</li>
    <li>They can update any user to a delivery person.</li>
    <li>Managers should also be able to browse and filter orders by status, such as delivered or not delivered.</li>
  </ul>
  <li>Customer Role:</li>
   <ul>
    <li>If a user doesn't belong to any specific group, they are considered a customer</li>
    <li>Customers can browse menu items, filter them by categories and price ranges, and search for specific items.</li>
    <li>Customers can add menu items to their cart and place orders.</li>
     <li>When an order is successfully created, the cart must be emptied.</li>
     <li>Each customer can only have one cart at a time, but a cart can contain multiple menu items.</li>
  </ul>
  <li>Delivery Crew Role:<li>
    <ul>
      <li>Delivery personnel can browse orders assigned to them via API endpoints after successful authentication.</li>
      <li>They can mark orders as delivered.</li>
    </ul>
</ol>
This project contains  three types of users: managers, customers, and the delivery crew . Every users have different roles. First is the manager role. Only managers can use some API endpoints to add, edit, and remove menu items. Managers should also be able to update any user to a delivery person. Next up is the customer rule, if a user doesn't belong to any specific group you should consider them a customer. Customers should be able to browse menu items, filter them by categories,and price ranges, and search menu items. There is also API allowing customers to add menu items to their cart and place an order. But  the cart must be emptied when the order is successfully created.One customer should only be able to have one cart at a time, and one cart should be able to contain multiple menu items.>
Last, there are APIs related to the delivery process. First, there is  API endpoints for the managers to browse the orders and assign them to a delivery person. Managers should also be able to filter orders by their status, like delivered and not delivered.  After successful authentication, delivery people should be able to browse orders assigned to them by using  API endpoints and mark them as delivered. Customers can always come to the orders endpoint to see their orders, including the status of that order and the total price

And finally, there is  throttling  implementation  to limit to five API calls per minute.

<h2>API endpoints </h2>
- User registration and token generation endpoints 

![image](https://github.com/user-attachments/assets/4335e0e4-f5fc-40e4-b8c3-e8686e427f4b)


- Menu item endpoints:

  ![image](https://github.com/user-attachments/assets/79277db4-5914-419d-a021-b8eab7c03786)

- User group management endpoints:

  ![image](https://github.com/user-attachments/assets/bd3da58d-0e04-4f8a-9ef7-707d2114ae3c)

- Cart management endpoints

  ![image](https://github.com/user-attachments/assets/b43415c9-85ac-47b7-8951-c71b0357ded3)

- Order management endpoints

  ![image](https://github.com/user-attachments/assets/c5de3504-f186-4cc1-b75c-a4e109955b2e)




  

 


