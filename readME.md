



This App is a very Large App in My opinion So i created A guid Below For You! to Follow When Deploying The app..


<h1>Steps To Before deployment</h1>

    Check the cron jobs if the functions are commented ..(you have to go to the admin admindashboard to start it)
        go to this link to activate it 'websitename/user/adminDashboard/startCron/'(u must be an admin)


    check the setting down below for variables
    like(paystack key,RAFFLE_DRAW_PAYMENT_CALLBACK_URL,EMAIL_HOST_USER) see if they are correct



<br> 

<hr> 

<hr> 
<h1>Steps To deployment</h1>

A)Working On the RaffleBatch
    1)Create A super User if U have not
        any time u are ready log in to your admin dashboard and activate it
<br>

<p>b)</p>

<h3>Create Membership</h3>
<p>There will be a defualt Free mebership You have to set it to like 100 months Just for a free member to use the app but he cant earn</p>
Now u have to create the paid membership They as follow
<hr> 
<ol>
    <li><h3>Bronze</h3></li>
    <p>Duration- 30</p>
    <p>duration period - days</p>
    <p>price - 3000.00</p>
    <p>EaarningLimit - 13000.00</p>
<br>
    <li><h3>Silver</h3></li>
    <p>Duration- 30</p>
    <p>duration period - days</p>
    <p>price - 7000.00</p>
    <p>EaarningLimit - 20000.00</p>
<br>
    <li><h3>Gold</h3></li>
    <p>Duration- 30</p>
    <p>duration period - days</p>
    <p>price - 14000.00</p>
    <p>EaarningLimit - 27000.00</p>
<br>
</ol>

<h3>
Before you Countinue Go to the url Below To Start the Cron Job
</h3>
'websitename/user/adminDashboard/startCron/'

<p>The Cron Job Task consist of</p>

    
    "every 19 hours  Check if the user Sub Has Expired"

    "every 23 hours  if user has logged in for that day and pay them"

    "every 24 hours  Get News Articles So Users can Earn"

