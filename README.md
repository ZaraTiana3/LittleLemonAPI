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
  <li>Delivery Crew Role:</li>
    <ul>
      <li>Delivery personnel can browse orders assigned to them via API endpoints after successful authentication.</li>
      <li>They can mark orders as delivered.</li>
    </ul>
</ol>

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




  

 


