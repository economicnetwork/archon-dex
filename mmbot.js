const mom = require('./mom.js');

const superagent = require('superagent');
var redis = require('redis');
var client = redis.createClient();


//mom.balance();

var pair = "TM-WETH";

/*
var orderPromise = mom.listorders(pair);
orderPromise.then(function(result) {
    console.log("openorders " + result);

    var key = "mom_openorders_" + pair;
    console.log("set " + key);
    client.set(key, result, redis.print); 

    client.quit();
});*/

/*var symbol = "WETH";
mom.balance(symbol).then(function(result){
    console.log(result);
})

mom.trades(pair).then(function(result){
    console.log("trades " + result);
})
*/

mom.cancelorders(pair);

/*
mom.balance();
mom.trades();
*/

//mom.list_markets();

//mom.cancelorders();

/*
var amount = 8000;
var price = 0.000033
mom.placeOrder(amount, price);

var amount = 8000;
var price = 0.000028
mom.placeOrder(amount, price);

var amount = 8000;
var price = 0.000026
mom.placeOrder(amount, price);

*/