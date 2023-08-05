<?php
header('access-control-allow-origin: http://morss.it');
header('access-control-allow-origin: http://test.morss.it');

require 'rb.php';

if (isset($_POST['stripeEmail']) and isset($_POST['stripeToken']))
{
	if (!filter_var($_POST['stripeEmail'], FILTER_VALIDATE_EMAIL))
		return;
	
	R::setup('sqlite:/home/pictuga/userbase.db');
	
	require './stripe/Stripe.php';
	Stripe::setApiKey("sk_test_1yAI0GMfDUexIZBN6ZTTzQCb");

	$token = $_POST['stripeToken'];
	$email = $_POST['stripeEmail'];

	$amount = 20;
	$currency = "USD";

	$user = R::findOne('user', 'email = ?', [$email]);

	if ($user !== NULL)
	{
		// check encore un bill valide
		//foreach ($user->ownBillList as $bill)
	}
	else
	{
		// charge him
		$user = R::dispense('user');
		$user->email = $email;
		$user->created = R::isoDateTime();

		try
		{
			$charge = Stripe_Charge::create(array(
				"amount" => $amount*100,
				"currency" => $currency,
				"card" => $token,
				"description" => $user->email)
			);
	
			$bill = R::dispense('bill');
			$bill->charge = $charge->id;
			$bill->amount = $amount;
			$bill->currency = $currency;
			$bill->issued = R::isoDateTime();
			$bill->expires = R::isoDateTime(strtotime('+1 year'));
	
			$user->ownBillList[] = $bill;
		}
		catch(Stripe_CardError $e)
		{
			//print "Payment cancelled";
		}
	}

	header('status: 303 See Other');
	header('location: http://morss.it/');

	R::store($user);
	R::close();
}

else if (isset($_GET['email']))
{
	if (!filter_var($_GET['email'], FILTER_VALIDATE_EMAIL))
	{
		print "INVALID MAIL";
		return;
	}
	
	R::setup('sqlite:/home/pictuga/userbase.db');
	$user = R::findOne('user', 'email = ?', [$_GET['email']]);
	
	if ($user !== NULL)
		print "VALID CLIENT";
	else
		print "NOT A CLIENT";

	R::close();
}
