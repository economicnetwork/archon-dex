/*
trading on mom

https://docs.tokenmom.com/

set privatekey with
export PRIVATEKEY=0x1xxxx

*/
const superagent = require('superagent');

base_url = "https://api.tokenmom.com/";
var ethereumjs_util = require("ethereumjs-util");

"use strict";
exports.__esModule = true;

function getAuth (){    
    var privateKey = process.env.PRIVATEKEY;
    //console.log("=> " + privateKey);
    var Address = '0x' + ethereumjs_util.privateToAddress(privateKey).toString("hex");
    var Timestamp = Date.now().toString();
    var sha = ethereumjs_util.hashPersonalMessage(ethereumjs_util.toBuffer(Timestamp));
    var ecdsaSignature = ethereumjs_util.ecsign(sha, ethereumjs_util.toBuffer(privateKey));
    var Signature = ethereumjs_util.toRpcSig(ecdsaSignature.v, ecdsaSignature.r, ecdsaSignature.s);
    var Auth = Timestamp + "#" + Signature;
    //console.log("\"wallet-addr: " + Address + "\"");
    //console.log("\"tm-auth: " + Auth + "\"");
    return [Auth, Address];
}

 function placeOrder(amount, price){
   [Auth, Address] = getAuth();
      
   var pair = "TM-WETH";
   var trade_type = "buy";

   superagent
   .post(base_url + "order/build_order") 
   .send({ "market_id": pair, "trade": trade_type, "price": price,"amount": amount})
   .set("wallet-addr", Address)
   .set("tm-auth",Auth)
   .set('Accept', 'application/json')
   .then(res => {
      var r = res.text;
      var j = JSON.parse(r);
      var orderhash = j.result.orderHash;      
      //console.log('order hash: ' + orderhash);
      
      [NewAuth, Address] = mom.getAuth();
      superagent
      .post(base_url + "order/place_order") 
      .send({ "order_hash" : orderhash, "signature": Auth})
      .set("wallet-addr", Address)
      .set("tm-auth",NewAuth)
      .set('Accept', 'application/json')
      .then(res => {
         console.log(res);
      })
   
   });   
}

function balance(symbol){
    [Auth, Address] = getAuth();
    
    return new Promise(function(resolve, reject) {
        superagent
        .get(base_url + "account/get_balance?token_symbol=" + symbol)   
        .set("wallet-addr", Address)
        .set("tm-auth",Auth)
        .set('Accept', 'application/json')
        .then(res => {
            var j = res.body;            
            var key = 'mom_balance_' + symbol;
            console.log("set key " + key + " " + j["amount"]);
            //TODO float
            var b = j["amount"];
            resolve(b);
        });
    });
}


function listorders(pair){
    [Auth, Address] = getAuth();
    
    return new Promise(function(resolve, reject) {
        superagent
        .get(base_url + "order/get_orders?market_id=" + pair)   
        .set("wallet-addr", Address)
        .set("tm-auth",Auth)
        .set('Accept', 'application/json')
        .then(res => {
            var j = res.body;
            var oo = JSON.stringify(j.orders);
            resolve(oo);         
        });
        });
}

function trades(pair){   
    [Auth, Address] = getAuth();
    
    return new Promise(function(resolve, reject) {
        superagent
        .get(base_url + "market/get_trades?market_id=" + pair)   
        .set("wallet-addr", Address)
        .set("tm-auth",Auth)
        .set('Accept', 'application/json')
        .then(res => {
            var j = res.body;
            //TODO
            console.log(res.body);
            console.log(res.status);
            console.log(res.body.status);
            resolve(j.trades);
            
        });
    });
}


function list_markets(){
    superagent
    .get(base_url + "market/get_markets")   
    .set('Accept', 'application/json')
    .then(res => {
        console.log('markets : ' + JSON.stringify(res.body));
    });
}

function cancel_order(oid){   
    [Auth, Address] = getAuth();
    
    return new Promise(function(resolve, reject) {
        superagent
        .post(base_url + "order/delete_order") 
        .send({ "order_id": oid })
        .set("wallet-addr", Address)
        .set("tm-auth",Auth)
        .set('Accept', 'application/json')
        .then(res => {
            var j = res.body;
            //TODO
            console.log(res.body);
            console.log(res.status);
            console.log(res.body.status);
            //resolve(j.trades);
            
        });
    });
}


function cancelorders(pair){
    console.log("cancel orders");
    [Auth, Address] = getAuth();

    var orderPromise = this.listorders(pair);
    orderPromise.then(function(result) {
        //console.log('open orders: ' + JSON.stringify(result));
        console.log('open orders: ' + result);

        var oo = JSON.parse(result);
        console.log('open orders: ' + oo);

        for (var i = 0; i <oo.length; i++){
            var o = oo[i];
            console.log("order " + o);
            var oid = o["id"];
            console.log("cancel " + oid);

            cancel_order(oid);
                       
        }
    });          
}


module.exports.cancel_order = cancel_order;
module.exports.trades = trades;
module.exports.listorders = listorders;
module.exports.cancelorders = cancelorders;
module.exports.balance = balance;
module.exports.placeOrder = placeOrder;
module.exports.list_markets = list_markets;


/*
WETH wrap
//import BigNumber from "bignumber.js"
const BigNumber = require("bignumber.js");
const Web3 = require("web3");

const web3 = new Web3(Web3.givenProvider || "http://localhost:8545");
web3.eth.getAccounts().then(console.log);

const wethAddress = "0xE....."
const value = 0.1 * (10**18) // 1 ETH in Wei
web3.eth.contract(
  [
    {
      "constant": false,
      "inputs": [],
      "name": "deposit",
      "outputs": [],
      "payable": true,
      "stateMutability": "payable",
      "type": "function"
    }
  ]
).at(wethAddress).deposit(
  {
    value: value,
    // You can optionally pass in the gas price and gas limit you would like to use
    gasLimit: 80000,
    gasPrice: new BigNumber(10**10),
  },
  (err, res) => {
    console.log(res) // Transaction id
  }
)
*/